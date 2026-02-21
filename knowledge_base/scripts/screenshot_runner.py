#!/usr/bin/env python3
"""
Headless screenshot runner for documentation.

Reads a machine-readable screenshot spec (JSON), logs into WordPress if configured,
then for each capture: navigate, run steps, take screenshot, save as {image_id}.png.

Schema: see docs/screenshot_spec_schema.md.
Env: WP_URL (overrides base_url), WP_USERNAME, WP_PASSWORD (for login).
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List

# Allow running from repo root or from knowledge_base
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


def get_base_url(spec: Dict[str, Any]) -> str:
    """Resolve base URL: env WP_URL overrides spec base_url."""
    base = os.getenv("WP_URL") or spec.get("base_url")
    if not base:
        raise ValueError("Spec must have base_url or set WP_URL in environment.")
    return base.rstrip("/")


def get_login(spec: Dict[str, Any]) -> tuple:
    """Return (username, password) from spec login or env."""
    login = spec.get("login") or {}
    user = login.get("user") or os.getenv("WP_USERNAME")
    password = login.get("password") or os.getenv("WP_PASSWORD")
    return user, password


def login_wordpress(page: Page, base_url: str, username: str, password: str) -> None:
    """Log into WordPress at base_url."""
    if not username or not password:
        raise ValueError("Login required: set WP_USERNAME and WP_PASSWORD or spec.login.")
    login_url = f"{base_url}/wp-login.php"
    page.goto(login_url)
    page.fill("#user_login", username)
    page.fill("#user_pass", password)
    page.click("#wp-submit")
    page.wait_for_load_state("networkidle")
    if "wp-admin" not in page.url and "admin.php" not in page.url:
        print(f"Warning: Login may have failed. Current URL: {page.url}")
    else:
        print("Login successful.")


def resolve_url(base_url: str, url: str) -> str:
    """Return full URL; if url is path-only, prepend base_url."""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return f"{base_url}/{url.lstrip('/')}"


def run_steps(page: Page, steps: List[Dict[str, Any]]) -> None:
    """Execute a list of step objects: click, wait, fill."""
    for step in steps:
        if "click" in step:
            page.click(step["click"])
        elif "wait" in step:
            page.wait_for_timeout(int(step["wait"]))
        elif "fill" in step:
            f = step["fill"]
            page.fill(f.get("selector", ""), f.get("text", ""))
        page.wait_for_timeout(200)


def run_capture(
    page: Page,
    base_url: str,
    capture: Dict[str, Any],
    output_dir: str,
) -> None:
    """Navigate, run steps, take screenshot; save as {image_id}.png."""
    image_id = capture.get("image_id")
    if not image_id:
        raise ValueError("Capture missing image_id.")
    url = resolve_url(base_url, capture.get("url", "/"))
    steps = capture.get("steps") or []
    selector = capture.get("selector")
    full_page = capture.get("full_page", False)

    print(f"Capture: {image_id}")
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")
    run_steps(page, steps)

    output_path = os.path.join(output_dir, f"{image_id}.png")
    os.makedirs(output_dir, exist_ok=True)

    if selector:
        page.locator(selector).first.screenshot(path=output_path)
    else:
        page.screenshot(path=output_path, full_page=full_page)
    print(f"  Saved: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capture documentation screenshots from a screenshot spec (JSON)."
    )
    parser.add_argument(
        "spec",
        help="Path to screenshot spec JSON (e.g. screenshot_spec.json).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="assets",
        help="Directory to save screenshots (default: assets).",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser in headed mode (visible).",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only load and validate the spec; do not launch browser.",
    )
    args = parser.parse_args()

    if not os.path.exists(args.spec):
        print(f"Error: Spec file not found: {args.spec}")
        sys.exit(1)

    with open(args.spec, "r", encoding="utf-8") as f:
        spec = json.load(f)

    base_url = get_base_url(spec)
    username, password = get_login(spec)
    captures = spec.get("captures") or []
    if not captures:
        print("No captures in spec.")
        sys.exit(0)

    if args.validate_only:
        print(f"Spec valid: base_url={base_url}, captures={len(captures)}")
        for c in captures:
            print(f"  - {c.get('image_id')}: {c.get('url')}")
        sys.exit(0)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        try:
            if username and password:
                login_wordpress(page, base_url, username, password)
            for capture in captures:
                try:
                    run_capture(page, base_url, capture, args.output)
                except Exception as e:
                    print(f"  Error: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
