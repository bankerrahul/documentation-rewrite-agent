#!/usr/bin/env python3
"""
SEO metadata generator for the Universal Screenshot Agent.

Uses an LLM to generate SEO-optimized metadata (title, description, keyphrases)
for each article in a product. Output is written to seo_meta.json in the product
directory, which is then consumed by seo_publisher.py to update WordPress via
the AIOSEO REST API.

Usage:
    # Generate SEO for all articles
    python -m universal_screenshot_agent.run -p my_product generate-seo

    # Generate for a single article
    python -m universal_screenshot_agent.run -p my_product generate-seo --article 1-01-...
"""

import json
import os
import re
from typing import Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import anthropic as _anthropic_mod
except ImportError:
    _anthropic_mod = None


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

DEFAULT_MODELS = {
    "openai": "gpt-4o",
    "anthropic": "claude-sonnet-4-5-20250929",
    "ollama": OLLAMA_MODEL,
}

SEO_SYSTEM_PROMPT = """You are an expert SEO specialist for WordPress knowledge base articles.

Given an article's title and content, generate optimized SEO metadata.

RULES:
- SEO Title: Under 60 characters. Include the primary keyphrase naturally. Do NOT add a brand suffix (that's handled separately).
- Meta Description: 140-160 characters. Compelling, action-oriented summary that includes the primary keyphrase. Should entice clicks from search results.
- Focus Keyphrase: 1-3 words that best represent the article's main topic. This is the primary search term.
- Additional Keyphrases: 2-3 secondary keyphrases (each 1-4 words) that represent related search queries.

OUTPUT FORMAT — respond with ONLY valid JSON, no markdown fences:
{
  "seo_title": "...",
  "meta_description": "...",
  "focus_keyphrase": "...",
  "additional_keyphrases": ["...", "..."]
}
"""


def _resolve_provider(provider: str) -> str:
    """Determine LLM provider from environment."""
    if provider != "auto":
        return provider
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    return "ollama"


def _call_llm(provider: str, model: str, system_prompt: str, user_message: str) -> str:
    """Send a request to the configured LLM and return text response."""
    if provider == "anthropic":
        key = os.getenv("ANTHROPIC_API_KEY", "")
        if not _anthropic_mod or not key:
            raise RuntimeError("Anthropic API key not set or anthropic package not installed.")
        client = _anthropic_mod.Anthropic(api_key=key)
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
            temperature=0.3,
        )
        return response.content[0].text

    elif provider == "openai":
        key = os.getenv("OPENAI_API_KEY", "")
        if not OpenAI or not key:
            raise RuntimeError("OpenAI API key not set or openai package not installed.")
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    elif provider == "ollama":
        url = os.getenv("OLLAMA_BASE_URL", OLLAMA_BASE_URL)
        if not OpenAI:
            raise RuntimeError("openai package not installed (needed for Ollama compatibility).")
        client = OpenAI(api_key="ollama", base_url=url.rstrip("/"))
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    raise RuntimeError(f"Unknown provider: {provider}")


def _strip_html(html: str) -> str:
    """Strip HTML tags and Gutenberg comments to get plain text."""
    text = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _parse_json_response(raw: str) -> Optional[Dict]:
    """Parse LLM response as JSON, handling markdown fences."""
    text = raw.strip()
    # Strip markdown code fences
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON object in the response
        match = re.search(r'\{[^{}]*"seo_title"[^{}]*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return None


def generate_seo_for_article(
    title: str,
    content: str,
    provider: str = "auto",
    model: str = None,
    product_name: str = "",
) -> Optional[Dict]:
    """Generate SEO metadata for a single article.

    Args:
        title: Article title
        content: Article HTML content (from wp_posts.json or markdown)
        provider: LLM provider
        model: LLM model name
        product_name: Product name for context

    Returns:
        Dict with seo_title, meta_description, focus_keyphrase, additional_keyphrases
    """
    resolved_provider = _resolve_provider(provider)
    resolved_model = model or DEFAULT_MODELS.get(resolved_provider, "gpt-4o")

    plain_text = _strip_html(content)
    # Truncate to avoid token limits — first ~2000 chars is enough for SEO
    if len(plain_text) > 2000:
        plain_text = plain_text[:2000] + "..."

    context_note = f" for {product_name}" if product_name else ""
    user_msg = (
        f"Generate SEO metadata{context_note} for this article:\n\n"
        f"Title: {title}\n\n"
        f"Content:\n{plain_text}"
    )

    print(f"  Generating SEO with {resolved_provider}/{resolved_model}...")
    raw = _call_llm(resolved_provider, resolved_model, SEO_SYSTEM_PROMPT, user_msg)
    result = _parse_json_response(raw)

    if not result:
        print(f"  WARNING: Failed to parse LLM response as JSON")
        print(f"  Raw response: {raw[:200]}...")
        return None

    # Validate required fields
    required = ["seo_title", "meta_description", "focus_keyphrase"]
    for field in required:
        if field not in result:
            print(f"  WARNING: Missing field '{field}' in LLM response")
            return None

    if "additional_keyphrases" not in result:
        result["additional_keyphrases"] = []

    return result


def generate_seo_for_product(
    config: dict,
    adapter,
    wp_posts_path: str,
    docs_dir: str,
    output_path: str,
    provider: str = "auto",
    model: str = None,
    article_filter: str = None,
):
    """Generate SEO metadata for all articles in a product.

    Args:
        config: Product config dict
        adapter: ProductAdapter instance
        wp_posts_path: Path to wp_posts.json
        docs_dir: Path to markdown docs directory
        output_path: Where to write seo_meta.json
        provider: LLM provider
        model: LLM model name
        article_filter: Optional slug to filter to a single article
    """
    product_name = config["product"]["name"]
    articles = adapter.get_articles()
    seo_config = config.get("seo", {})
    default_keyphrases = seo_config.get("default_keyphrases", [])

    # Load existing seo_meta.json to preserve manual edits
    existing = {}
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            for item in json.load(f):
                existing[item["filename"]] = item
        print(f"Loaded {len(existing)} existing SEO entries (will preserve manual edits)")

    # Load content source — prefer wp_posts.json, fall back to markdown docs
    content_source = {}
    if os.path.exists(wp_posts_path):
        with open(wp_posts_path, "r", encoding="utf-8") as f:
            for post in json.load(f):
                content_source[post["filename"]] = {
                    "title": post["title"],
                    "content": post["content"],
                }
        print(f"Using content from wp_posts.json ({len(content_source)} articles)")
    else:
        # Fall back to markdown docs
        for article_info in articles:
            slug = article_info["slug"]
            md_path = os.path.join(docs_dir, f"{slug}.md")
            if os.path.exists(md_path):
                with open(md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Extract title from first H1
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else slug
                content_source[f"{slug}.md"] = {"title": title, "content": content}
        print(f"Using content from markdown docs ({len(content_source)} articles)")

    results = []
    for article_info in articles:
        slug = article_info["slug"]
        filename = f"{slug}.md"
        post_id = article_info.get("post_id")

        if article_filter and slug != article_filter:
            continue

        # Skip if already in existing and has all fields
        if filename in existing:
            entry = existing[filename]
            if all(entry.get(f) for f in ["seo_title", "meta_description", "focus_keyphrase"]):
                print(f"  Skipping {slug} (already has SEO data, use --force to regenerate)")
                results.append(entry)
                continue

        if filename not in content_source:
            print(f"  Skipping {slug}: no content found")
            continue

        source = content_source[filename]
        seo = generate_seo_for_article(
            title=source["title"],
            content=source["content"],
            provider=provider,
            model=model,
            product_name=product_name,
        )

        if seo:
            # Merge default keyphrases
            if default_keyphrases:
                existing_kps = [seo.get("focus_keyphrase", "")] + seo.get("additional_keyphrases", [])
                existing_kps_lower = [kp.lower() for kp in existing_kps]
                for dkp in default_keyphrases:
                    if dkp.lower() not in existing_kps_lower:
                        seo.setdefault("additional_keyphrases", []).append(dkp)

            entry = {
                "filename": filename,
                "post_id": post_id,
                "seo_title": seo["seo_title"],
                "meta_description": seo["meta_description"],
                "focus_keyphrase": seo["focus_keyphrase"],
                "additional_keyphrases": seo.get("additional_keyphrases", []),
            }
            results.append(entry)
            print(f"  OK: {slug}")
            print(f"    Title ({len(entry['seo_title'])} chars): {entry['seo_title']}")
            print(f"    Desc ({len(entry['meta_description'])} chars): {entry['meta_description'][:80]}...")
            print(f"    Focus: {entry['focus_keyphrase']}")
            print(f"    Additional: {entry['additional_keyphrases']}")
        else:
            print(f"  FAILED: {slug}")
            # Keep existing entry if we had one
            if filename in existing:
                results.append(existing[filename])

    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {len(results)} entries to {output_path}")
    return results
