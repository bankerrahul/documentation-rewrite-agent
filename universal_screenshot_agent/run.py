#!/usr/bin/env python3
"""
CLI runner for the Universal Screenshot Agent.

Usage:
    # Parse all docs for a product
    python -m universal_screenshot_agent.run -p thrive_apprentice parse

    # Parse a single doc
    python -m universal_screenshot_agent.run -p thrive_apprentice parse --article 1-01-creating-your-first-course

    # Capture screenshots for a specific article
    python -m universal_screenshot_agent.run -p thrive_apprentice capture 1-01-creating-your-first-course

    # Capture with visible browser (for debugging)
    python -m universal_screenshot_agent.run -p thrive_apprentice capture 1-01-creating-your-first-course --headed

    # Capture all articles
    python -m universal_screenshot_agent.run -p thrive_apprentice capture-all

    # Publish screenshots to production
    python -m universal_screenshot_agent.run -p thrive_apprentice publish

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


def main():
    parser = argparse.ArgumentParser(
        description="Universal Screenshot Agent — product-agnostic documentation screenshot pipeline"
    )
    parser.add_argument(
        "--product", "-p",
        help="Product slug (e.g., thrive_apprentice). Required for most commands.",
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
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
