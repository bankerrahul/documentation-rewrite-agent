#!/usr/bin/env python3
"""
CLI runner for the Screenshot Annotation Agent.

Usage:
    # Parse all docs into screenshot specs
    python -m screenshot_agent.run parse

    # Parse a single doc
    python -m screenshot_agent.run parse --article 1-01-creating-your-first-course

    # Capture screenshots for a specific article
    python -m screenshot_agent.run capture 1-01-creating-your-first-course

    # Capture with visible browser (for debugging)
    python -m screenshot_agent.run capture 1-01-creating-your-first-course --headed

    # Run setup wizard + create sample data on local site
    python -m screenshot_agent.run setup
"""

import argparse
import glob
import os
import sys

# Add parent dir to path so we can import screenshot_agent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "thrive_apprentice", "new_docs")
SPECS_DIR = os.path.join(BASE_DIR, "thrive_apprentice", "screenshot_specs")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "thrive_apprentice", "screenshots")


def cmd_parse(args):
    """Parse markdown docs into screenshot specs."""
    from screenshot_agent.step_parser import parse_all_articles, parse_article
    import json

    if args.article:
        # Parse single article
        md_file = args.article if args.article.endswith(".md") else f"{args.article}.md"
        filepath = os.path.join(DOCS_DIR, md_file)
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            sys.exit(1)

        spec = parse_article(filepath)
        os.makedirs(SPECS_DIR, exist_ok=True)
        spec_file = os.path.join(SPECS_DIR, md_file.replace(".md", ".json"))
        with open(spec_file, "w") as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)

        total_steps = sum(len(s["steps"]) for s in spec["sections"])
        print(f"Parsed: {md_file}")
        print(f"  Sections: {len(spec['sections'])}")
        print(f"  Steps: {total_steps}")
        print(f"  Spec: {spec_file}")

        # Print step details
        for section in spec["sections"]:
            print(f"\n  [{section['heading']}]")
            for step in section["steps"]:
                print(f"    {step['step_num']}. [{step['action']}] \"{step['target']}\" ({step['context'][:40]})")
    else:
        # Parse all articles
        print(f"Parsing all articles from {DOCS_DIR}...")
        specs = parse_all_articles(DOCS_DIR, SPECS_DIR)
        total_steps = sum(sum(len(s["steps"]) for s in spec["sections"]) for spec in specs)
        print(f"\nTotal: {len(specs)} articles, {total_steps} screenshottable steps")
        print(f"Specs written to: {SPECS_DIR}")


def cmd_capture(args):
    """Capture screenshots for article(s)."""
    from screenshot_agent.capture import capture_articles

    article = args.article
    if not article:
        print("Error: Please specify an article name (e.g., 1-01-creating-your-first-course)")
        sys.exit(1)

    # Find the spec file
    spec_name = article if article.endswith(".json") else f"{article}.json"
    spec_path = os.path.join(SPECS_DIR, spec_name)

    if not os.path.exists(spec_path):
        print(f"Spec not found: {spec_path}")
        print("Run 'parse' first to generate specs.")
        sys.exit(1)

    print(f"Capturing screenshots for: {article}")
    print(f"Spec: {spec_path}")
    print(f"Output: {SCREENSHOTS_DIR}")
    print(f"Headed mode: {args.headed}")
    print()

    capture_articles(
        spec_files=[spec_path],
        output_dir=SCREENSHOTS_DIR,
        headed=args.headed,
    )


def cmd_capture_all(args):
    """Capture screenshots for all articles with specs."""
    from screenshot_agent.capture import capture_articles

    spec_files = sorted(glob.glob(os.path.join(SPECS_DIR, "*.json")))
    if not spec_files:
        print(f"No spec files found in {SPECS_DIR}. Run 'parse' first.")
        sys.exit(1)

    print(f"Capturing screenshots for {len(spec_files)} articles...")
    print(f"Output: {SCREENSHOTS_DIR}")
    print()

    capture_articles(
        spec_files=spec_files,
        output_dir=SCREENSHOTS_DIR,
        headed=args.headed,
    )


def cmd_setup(args):
    """Run the setup wizard and create sample data."""
    from screenshot_agent.setup_sample_data import main as setup_main
    setup_main()


def main():
    parser = argparse.ArgumentParser(
        description="Screenshot Annotation Agent for Thrive Apprentice Docs"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # parse command
    parse_parser = subparsers.add_parser("parse", help="Parse docs into screenshot specs")
    parse_parser.add_argument("--article", "-a", help="Specific article slug (without .md)")

    # capture command
    cap_parser = subparsers.add_parser("capture", help="Capture screenshots for an article")
    cap_parser.add_argument("article", help="Article slug (e.g., 1-01-creating-your-first-course)")
    cap_parser.add_argument("--headed", action="store_true", help="Show browser window")

    # capture-all command
    capall_parser = subparsers.add_parser("capture-all", help="Capture screenshots for all articles")
    capall_parser.add_argument("--headed", action="store_true", help="Show browser window")

    # setup command
    setup_parser = subparsers.add_parser("setup", help="Setup wizard + sample data on local site")

    args = parser.parse_args()

    if args.command == "parse":
        cmd_parse(args)
    elif args.command == "capture":
        cmd_capture(args)
    elif args.command == "capture-all":
        cmd_capture_all(args)
    elif args.command == "setup":
        cmd_setup(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
