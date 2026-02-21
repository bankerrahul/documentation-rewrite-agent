#!/usr/bin/env python3
"""
CLI runner for the Universal Screenshot Agent.

Usage:
    # Parse all docs for a product
    python -m universal_screenshot_agent.run -p my_product parse

    # Parse a single doc
    python -m universal_screenshot_agent.run -p my_product parse --article getting-started

    # Capture screenshots for a specific article
    python -m universal_screenshot_agent.run -p my_product capture getting-started

    # Capture with visible browser (for debugging)
    python -m universal_screenshot_agent.run -p my_product capture getting-started --headed

    # Capture all articles
    python -m universal_screenshot_agent.run -p my_product capture-all

    # Publish screenshots to production
    python -m universal_screenshot_agent.run -p my_product publish

    # List available products
    python -m universal_screenshot_agent.run list-products
"""

import argparse
import glob
import json
import os
import sys

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from universal_screenshot_agent.config_loader import (
    load_product_config, get_product_paths, load_adapter, _get_products_dir,
)


def cmd_list_products(args):
    """List available products."""
    products_dir = _get_products_dir()
    if not os.path.exists(products_dir):
        print("No products directory found.")
        return

    print(f"Available products in {products_dir}:\n")
    for name in sorted(os.listdir(products_dir)):
        if name.startswith("_") or name.startswith("."):
            continue
        config_path = os.path.join(products_dir, name, "config.yaml")
        if os.path.exists(config_path):
            try:
                config = load_product_config(name)
                product_name = config["product"]["name"]
                print(f"  {name:30s} — {product_name}")
            except Exception as e:
                print(f"  {name:30s} — ERROR: {str(e)[:60]}")
        else:
            print(f"  {name:30s} — (no config.yaml)")


def cmd_parse(args, config, paths):
    """Parse markdown docs into screenshot specs."""
    from universal_screenshot_agent.step_parser import parse_all_articles, parse_article

    docs_dir = paths["docs"]
    specs_dir = paths["specs"]

    if not os.path.exists(docs_dir):
        print(f"Error: Docs directory not found: {docs_dir}")
        sys.exit(1)

    if args.article:
        # Parse single article
        md_file = args.article if args.article.endswith(".md") else f"{args.article}.md"
        filepath = os.path.join(docs_dir, md_file)
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            sys.exit(1)

        spec = parse_article(filepath)
        os.makedirs(specs_dir, exist_ok=True)
        spec_file = os.path.join(specs_dir, md_file.replace(".md", ".json"))
        with open(spec_file, "w") as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)

        total_steps = sum(len(s["steps"]) for s in spec["sections"])
        print(f"Parsed: {md_file}")
        print(f"  Sections: {len(spec['sections'])}")
        print(f"  Steps: {total_steps}")
        print(f"  Spec: {spec_file}")

        for section in spec["sections"]:
            print(f"\n  [{section['heading']}]")
            for step in section["steps"]:
                print(f"    {step['step_num']}. [{step['action']}] \"{step['target']}\" ({step['context'][:40]})")
    else:
        # Parse all articles
        print(f"Parsing all articles from {docs_dir}...")
        specs = parse_all_articles(docs_dir, specs_dir)
        total_steps = sum(sum(len(s["steps"]) for s in spec["sections"]) for spec in specs)
        print(f"\nTotal: {len(specs)} articles, {total_steps} screenshottable steps")
        print(f"Specs written to: {specs_dir}")


def cmd_capture(args, config, paths, adapter):
    """Capture screenshots for an article."""
    from universal_screenshot_agent.capture import capture_articles

    article = args.article
    if not article:
        print("Error: Please specify an article name (e.g., 1-01-creating-your-first-course)")
        sys.exit(1)

    specs_dir = paths["specs"]
    screenshots_dir = paths["screenshots"]

    spec_name = article if article.endswith(".json") else f"{article}.json"
    spec_path = os.path.join(specs_dir, spec_name)

    if not os.path.exists(spec_path):
        print(f"Spec not found: {spec_path}")
        print("Run 'parse' first to generate specs.")
        sys.exit(1)

    print(f"Capturing screenshots for: {article}")
    print(f"Product: {config['product']['name']}")
    print(f"Spec: {spec_path}")
    print(f"Output: {screenshots_dir}")
    print(f"Headed mode: {args.headed}")
    print()

    capture_articles(
        spec_files=[spec_path],
        output_dir=screenshots_dir,
        adapter=adapter,
        headed=args.headed,
    )


def cmd_capture_all(args, config, paths, adapter):
    """Capture screenshots for all articles with specs."""
    from universal_screenshot_agent.capture import capture_articles

    specs_dir = paths["specs"]
    screenshots_dir = paths["screenshots"]

    spec_files = sorted(glob.glob(os.path.join(specs_dir, "*.json")))
    if not spec_files:
        print(f"No spec files found in {specs_dir}. Run 'parse' first.")
        sys.exit(1)

    print(f"Capturing screenshots for {len(spec_files)} articles...")
    print(f"Product: {config['product']['name']}")
    print(f"Output: {screenshots_dir}")
    print()

    capture_articles(
        spec_files=spec_files,
        output_dir=screenshots_dir,
        adapter=adapter,
        headed=args.headed,
    )


def cmd_publish(args, config, paths, adapter):
    """Publish screenshots to production."""
    from universal_screenshot_agent.publisher import ScreenshotPublisher

    screenshots_dir = paths["screenshots"]
    wp_posts_path = paths["wp_posts"]

    if not os.path.exists(wp_posts_path):
        print(f"Error: wp_posts.json not found: {wp_posts_path}")
        sys.exit(1)

    publisher = ScreenshotPublisher(config, adapter, screenshots_dir, wp_posts_path)
    publisher.run()


def cmd_generate_seo(args, config, paths, adapter):
    """Generate SEO metadata for articles using LLM."""
    from universal_screenshot_agent.seo_generator import generate_seo_for_product

    wp_posts_path = getattr(args, "wp_posts", None) or paths["wp_posts"]
    docs_dir = paths["docs"]
    seo_meta_path = getattr(args, "output", None) or paths["seo_meta"]

    print(f"Generating SEO metadata...")
    print(f"Source: {wp_posts_path}")
    print(f"Output: {seo_meta_path}")
    if getattr(args, "force", False):
        print(f"Force mode: regenerating all entries")
    print()

    generate_seo_for_product(
        config=config,
        adapter=adapter,
        wp_posts_path=wp_posts_path,
        docs_dir=docs_dir,
        output_path=seo_meta_path,
        provider=getattr(args, "provider", "auto"),
        model=getattr(args, "model", None),
        article_filter=getattr(args, "article", None),
        force=getattr(args, "force", False),
    )


def cmd_publish_seo(args, config, paths, adapter):
    """Publish SEO metadata to WordPress via AIOSEO REST API."""
    from universal_screenshot_agent.seo_publisher import SeoPublisher, get_chrome_client_js

    seo_meta_path = paths["seo_meta"]

    if not os.path.exists(seo_meta_path):
        print(f"Error: seo_meta.json not found: {seo_meta_path}")
        print("Run 'generate-seo' first to create it.")
        sys.exit(1)

    # Print the Chrome client JS for the user to inject
    post_type = adapter.get_post_type()
    client_js = get_chrome_client_js(post_type)
    print("=" * 60)
    print("Inject this JS into Chrome console on wp-admin:")
    print("=" * 60)
    print(client_js)
    print("=" * 60)
    print()

    publisher = SeoPublisher(config, adapter, seo_meta_path)
    publisher.run()


def main():
    parser = argparse.ArgumentParser(
        description="Universal Screenshot Agent — product-agnostic documentation screenshot pipeline"
    )
    parser.add_argument(
        "--product", "-p",
        help="Product slug (e.g., my_product). Required for most commands.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list-products
    subparsers.add_parser("list-products", help="List available products")

    # parse
    parse_parser = subparsers.add_parser("parse", help="Parse docs into screenshot specs")
    parse_parser.add_argument("--article", "-a", help="Specific article slug (without .md)")

    # capture
    cap_parser = subparsers.add_parser("capture", help="Capture screenshots for an article")
    cap_parser.add_argument("article", help="Article slug (e.g., 1-01-creating-your-first-course)")
    cap_parser.add_argument("--headed", action="store_true", help="Show browser window")

    # capture-all
    capall_parser = subparsers.add_parser("capture-all", help="Capture screenshots for all articles")
    capall_parser.add_argument("--headed", action="store_true", help="Show browser window")

    # publish
    pub_parser = subparsers.add_parser("publish", help="Publish screenshots to production")

    # generate-seo
    seo_gen_parser = subparsers.add_parser("generate-seo", help="Generate SEO metadata for articles")
    seo_gen_parser.add_argument("--article", "-a", help="Specific article slug (without .md)")
    seo_gen_parser.add_argument(
        "--provider", choices=["auto", "anthropic", "openai", "ollama"],
        default="auto", help="LLM provider (default: auto-detect)"
    )
    seo_gen_parser.add_argument("--model", default=None, help="Override LLM model name")
    seo_gen_parser.add_argument("--wp-posts", default=None,
        help="Path to wp_posts.json (default: product directory)")
    seo_gen_parser.add_argument("--output", "-o", default=None,
        help="Output path for seo_meta.json (default: product directory)")
    seo_gen_parser.add_argument("--force", action="store_true",
        help="Regenerate SEO for all articles, even those with existing data")

    # publish-seo
    seo_pub_parser = subparsers.add_parser("publish-seo", help="Publish SEO metadata to WordPress (AIOSEO)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # list-products doesn't need a product
    if args.command == "list-products":
        cmd_list_products(args)
        return

    # All other commands need a product
    if not args.product:
        print("Error: --product / -p is required. Use 'list-products' to see available products.")
        sys.exit(1)

    # Load product config and adapter
    try:
        config = load_product_config(args.product)
        paths = get_product_paths(args.product)
        adapter = load_adapter(args.product, config)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Product: {config['product']['name']} ({args.product})")
    print(f"Adapter: {type(adapter).__name__}")
    print()

    if args.command == "parse":
        cmd_parse(args, config, paths)
    elif args.command == "capture":
        cmd_capture(args, config, paths, adapter)
    elif args.command == "capture-all":
        cmd_capture_all(args, config, paths, adapter)
    elif args.command == "publish":
        cmd_publish(args, config, paths, adapter)
    elif args.command == "generate-seo":
        cmd_generate_seo(args, config, paths, adapter)
    elif args.command == "publish-seo":
        cmd_publish_seo(args, config, paths, adapter)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
