"""Batch processing engine for documentation rewrites.

Usage:
    python batch_runner.py <product> [options]

Examples:
    python batch_runner.py thrive_leads --init
    python batch_runner.py thrive_leads --resume
    python batch_runner.py thrive_leads --article 1_getting_started
    python batch_runner.py thrive_leads --status
    python batch_runner.py thrive_leads --retry-failed
"""

import argparse
import glob
import os
import re
import sys
import time

from agent import DocumentationAgent
from lib.config import AgentConfig
from lib.state import BatchState


def discover_articles(product_dir: str) -> list:
    """Scan a product directory for source markdown files and build article list.

    Expects files named like: 1_getting_started_with_thrive_leads.md
    """
    pattern = os.path.join(product_dir, "*.md")
    files = sorted(glob.glob(pattern))
    articles = []
    for fpath in files:
        basename = os.path.basename(fpath)
        # Skip metadata, redirect maps, and non-article files
        if basename.startswith(("redirect_map", "thrive_", "batch_state")):
            continue
        if basename.endswith("_metadata.md"):
            continue

        # Extract article id from filename (e.g. "1_getting_started_with_thrive_leads")
        article_id = os.path.splitext(basename)[0]
        # Try to extract a human-readable title from the first heading
        title = _extract_title(fpath) or article_id.replace("_", " ").title()

        articles.append({
            "id": article_id,
            "title": title,
            "source_file": fpath,
            "source_urls": [],
            "merge_sources": [],
            "merge_instructions": "",
        })
    return articles


def _extract_title(filepath: str) -> str:
    """Read the first H1 heading from a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    return ""


def process_single_article(agent: DocumentationAgent, article: dict, output_dir: str) -> dict:
    """Process a single article (rewrite or merge) and write outputs.

    Returns dict of output file paths keyed by output type.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Determine if this is a merge task
    if article.get("merge_sources"):
        source_contents = []
        for src in article["merge_sources"]:
            src_path = src.get("source_file", "")
            if os.path.exists(src_path):
                with open(src_path, "r", encoding="utf-8") as f:
                    source_contents.append({
                        "title": src.get("title", os.path.basename(src_path)),
                        "content": f.read(),
                    })
        if not source_contents:
            raise ValueError(f"No valid source files found for merge: {article['id']}")

        outputs = agent.process_merge(
            source_contents=source_contents,
            target_title=article["title"],
            merge_instructions=article.get("merge_instructions", ""),
        )
    else:
        # Single file rewrite
        src_path = article["source_file"]
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source file not found: {src_path}")
        with open(src_path, "r", encoding="utf-8") as f:
            source_content = f.read()
        outputs = agent.process_document(source_content)

    if "error" in outputs:
        raise RuntimeError(outputs["error"])

    # Write output files
    output_paths = {}
    for filename, content in outputs.items():
        if content:
            out_path = os.path.join(output_dir, filename)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            output_paths[filename] = out_path

    return output_paths


def run_batch(config: AgentConfig, product: str, article_id: str = None, retry_failed: bool = False) -> None:
    """Run batch processing for a product."""
    kb_dir = config.knowledge_base_dir
    product_dir = os.path.join(kb_dir, product)
    state_path = os.path.join(product_dir, "batch_state.json")

    state = BatchState(state_path).load()
    if not state.data:
        print(f"Error: No batch state found at {state_path}. Run with --init first.")
        sys.exit(1)

    if retry_failed:
        count = state.reset_failed_to_pending()
        print(f"Reset {count} failed article(s) to pending.")

    # Create the agent
    agent = DocumentationAgent(
        knowledge_base_dir=kb_dir,
        api_key=config.api_key,
        model=config.model,
        provider=config.provider,
    )

    # Process articles
    processed = 0
    while True:
        if article_id:
            art = state.get_article(article_id)
            if not art:
                print(f"Error: Article '{article_id}' not found in batch state.")
                return
            if art["status"] == "completed":
                print(f"Article '{article_id}' already completed. Use --retry-failed or edit batch_state.json.")
                return
        else:
            art = state.get_next_pending()
            if not art:
                break

        art_id = art["id"]
        print(f"\n--- Processing: {art_id} ({art['title']}) ---")
        state.mark_in_progress(art_id)

        output_dir = os.path.join(product_dir, "output", art_id)

        try:
            output_paths = process_single_article(agent, art, output_dir)
            state.mark_completed(art_id, output_paths)
            print(f"  Completed: {art_id} -> {output_dir}")
            processed += 1
        except Exception as e:
            state.mark_failed(art_id, str(e))
            print(f"  FAILED: {art_id} — {e}")

        # If processing a specific article, stop after one
        if article_id:
            break

        # Rate limiting delay
        if config.batch_delay_seconds > 0:
            time.sleep(config.batch_delay_seconds)

    state.print_status()
    print(f"Processed {processed} article(s) this run.")


def init_batch(config: AgentConfig, product: str) -> None:
    """Initialize a batch state file from a product directory."""
    product_dir = os.path.join(config.knowledge_base_dir, product)
    if not os.path.isdir(product_dir):
        print(f"Error: Product directory not found: {product_dir}")
        sys.exit(1)

    state_path = os.path.join(product_dir, "batch_state.json")
    if os.path.exists(state_path):
        print(f"Warning: batch_state.json already exists at {state_path}")
        resp = input("Overwrite? [y/N] ").strip().lower()
        if resp != "y":
            print("Aborted.")
            return

    articles = discover_articles(product_dir)
    if not articles:
        print(f"No article files found in {product_dir}")
        return

    state = BatchState(state_path)
    state.initialize(product, articles)
    print(f"Initialized batch state with {len(articles)} articles:")
    for art in articles:
        print(f"  {art['id']}: {art['title']}")
    state.print_status()


def main():
    parser = argparse.ArgumentParser(description="Batch documentation processing engine.")
    parser.add_argument("product", help="Product slug (e.g. thrive_leads, thrive_quiz_builder)")
    parser.add_argument("--init", action="store_true", help="Initialize batch state from product directory")
    parser.add_argument("--resume", action="store_true", help="Resume processing from last pending article")
    parser.add_argument("--article", default=None, help="Process a specific article by ID")
    parser.add_argument("--status", action="store_true", help="Show batch progress only")
    parser.add_argument("--retry-failed", action="store_true", help="Reset failed articles to pending and reprocess")
    parser.add_argument("--provider", default=None, help="Override LLM provider")
    parser.add_argument("--model", default=None, help="Override LLM model")

    args = parser.parse_args()
    config = AgentConfig.from_env()

    if args.provider:
        config.provider = args.provider
    if args.model:
        config.model = args.model

    if args.init:
        init_batch(config, args.product)
    elif args.status:
        product_dir = os.path.join(config.knowledge_base_dir, args.product)
        state_path = os.path.join(product_dir, "batch_state.json")
        state = BatchState(state_path).load()
        if state.data:
            state.print_status()
        else:
            print(f"No batch state found at {state_path}")
    elif args.resume or args.article or args.retry_failed:
        run_batch(config, args.product, article_id=args.article, retry_failed=args.retry_failed)
    else:
        # Default: resume processing
        run_batch(config, args.product)


if __name__ == "__main__":
    main()
