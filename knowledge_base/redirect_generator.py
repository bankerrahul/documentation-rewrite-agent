"""Generate redirect maps from reorganization plans.

Reads a parsed ReorgPlan and produces:
- CSV redirect maps (matching existing format)
- .htaccess redirect rules (for manual server config)
"""

import csv
import os
import re
from typing import Dict, List, Optional

from merge_processor import ReorgPlan, parse_reorganization_plan


def generate_redirect_map(
    plan: ReorgPlan,
    base_url: str = "https://thrivethemes.com/docs/",
) -> List[Dict[str, str]]:
    """Build redirect entries from a reorganization plan.

    For each merge group, creates redirects from source article URLs to the
    new merged target URL. For prune items with "Merge then prune" action,
    finds the appropriate target.

    Args:
        plan: Parsed reorganization plan.
        base_url: Base URL for documentation (used for slug-based redirects).

    Returns:
        List of dicts with 'old_url', 'new_url', and 'new_title' keys.
    """
    redirects = []

    # Build a title -> URL mapping from source articles
    title_to_url = {}
    for art in plan.source_articles:
        if art.url:
            title_to_url[art.title.lower()] = art.url

    for group in plan.merge_groups:
        target_slug = _title_to_slug(group.target_title)
        new_url = f"/{target_slug}/"

        for src_title in group.source_titles:
            old_url = title_to_url.get(src_title.lower(), "")
            if not old_url:
                # Try partial match
                old_url = _find_url_for_title(src_title, title_to_url)

            if old_url:
                # Extract just the path portion
                old_slug = _extract_slug(old_url)
                redirects.append({
                    "old_url": old_slug,
                    "new_url": new_url,
                    "new_title": group.target_title,
                })

    # Handle prune items that imply redirects
    for item in plan.prune_items:
        if "merge" in item.action.lower():
            # "Merge then prune" — find where it should redirect
            old_url = title_to_url.get(item.articles.lower(), "")
            if not old_url:
                old_url = _find_url_for_title(item.articles, title_to_url)
            # We don't know the exact target; leave new_url empty for manual review
            if old_url:
                redirects.append({
                    "old_url": _extract_slug(old_url),
                    "new_url": "# NEEDS_REVIEW",
                    "new_title": f"(Pruned: {item.articles})",
                })

    return redirects


def _title_to_slug(title: str) -> str:
    """Convert a document title to a URL slug."""
    slug = title.lower()
    # Prefix with "how-to-" if not already present
    if not slug.startswith("how to"):
        slug = f"how-to-{slug}"
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def _extract_slug(url: str) -> str:
    """Extract the slug portion from a full URL or path."""
    # Remove base URL
    url = url.rstrip("/")
    parts = url.split("/")
    slug = parts[-1] if parts else url
    return f"/{slug}/"


def _find_url_for_title(title: str, title_to_url: Dict[str, str]) -> str:
    """Fuzzy match a title to find its URL."""
    title_lower = title.lower()
    for key, url in title_to_url.items():
        if title_lower in key or key in title_lower:
            return url
    # Word overlap
    title_words = set(re.findall(r"\w+", title_lower))
    best_url = ""
    best_score = 0
    for key, url in title_to_url.items():
        key_words = set(re.findall(r"\w+", key))
        overlap = len(title_words & key_words)
        if overlap > best_score and overlap >= 2:
            best_score = overlap
            best_url = url
    return best_url


def write_redirect_csv(
    redirects: List[Dict[str, str]],
    output_path: str,
) -> None:
    """Write redirects to CSV matching the existing format.

    Format: Old URL Slug, New Canonical Slug, New Guide Title
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Old URL Slug", "New Canonical Slug", "New Guide Title"])
        for r in redirects:
            writer.writerow([r["old_url"], r["new_url"], r["new_title"]])
    print(f"Redirect map written to: {output_path} ({len(redirects)} entries)")


def generate_htaccess_rules(redirects: List[Dict[str, str]], docs_path: str = "/docs") -> str:
    """Generate Apache .htaccess redirect rules.

    Args:
        redirects: List of redirect dicts.
        docs_path: Base path for docs on the server.
    """
    lines = ["# Documentation redirects (auto-generated)", "# Add to .htaccess or server config", ""]
    for r in redirects:
        old = r["old_url"]
        new = r["new_url"]
        if new.startswith("#"):
            lines.append(f"# NEEDS REVIEW: {old} -> ???")
            continue
        lines.append(f"RedirectPermanent {docs_path}{old} {docs_path}{new}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate redirect maps from reorganization plans.")
    parser.add_argument("plan_file", help="Path to the reorganization plan markdown file.")
    parser.add_argument("--output", default=None, help="Output CSV path (default: <product>_redirect_map.csv).")
    parser.add_argument("--htaccess", action="store_true", help="Also output .htaccess rules.")
    parser.add_argument("--base-url", default="https://thrivethemes.com/docs/", help="Base URL for docs.")
    args = parser.parse_args()

    plan = parse_reorganization_plan(args.plan_file)
    redirects = generate_redirect_map(plan, base_url=args.base_url)

    print(f"Generated {len(redirects)} redirect(s) for {plan.product}")
    for r in redirects:
        print(f"  {r['old_url']} -> {r['new_url']}")

    output_path = args.output or f"{plan.product}_redirect_map.csv"
    write_redirect_csv(redirects, output_path)

    if args.htaccess:
        rules = generate_htaccess_rules(redirects)
        htaccess_path = f"{plan.product}_redirects.htaccess"
        with open(htaccess_path, "w", encoding="utf-8") as f:
            f.write(rules)
        print(f".htaccess rules written to: {htaccess_path}")


if __name__ == "__main__":
    main()
