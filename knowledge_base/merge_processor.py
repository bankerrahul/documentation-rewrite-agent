"""Parse reorganization plans and generate batch states with merge instructions.

Reorganization plan markdown files (e.g. THRIVE_LEADS_DOCS_REORGANIZATION.md)
follow a consistent structure:
  - Section 1: Full list of docs (tables with #, Title, URL per category)
  - Section 2: Merge Ideas (table: Merge group | Target article | Source articles | Rationale)
  - Section 3: Delete or Prune Ideas (table: Action | Article(s) | Rationale)
  - Section 4: Category Reorganization (proposed structure table)
  - Section 5: Final Proposed Doc List (numbered lists grouped by category)

This module parses those sections and produces structured data for batch processing.
"""

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from lib.state import BatchState


@dataclass
class SourceArticle:
    """An article from the source documentation."""
    title: str
    url: str = ""
    category: str = ""


@dataclass
class MergeGroup:
    """A group of source articles to be merged into one target article."""
    name: str
    target_title: str
    source_titles: List[str] = field(default_factory=list)
    rationale: str = ""


@dataclass
class PruneItem:
    """An article flagged for deletion, pruning, or relocation."""
    action: str  # "Prune", "Merge then prune", "Evaluate", "Consider relocating"
    articles: str
    rationale: str = ""


@dataclass
class ProposedCategory:
    """A category in the proposed new structure."""
    name: str
    articles: List[str] = field(default_factory=list)


@dataclass
class ReorgPlan:
    """Parsed reorganization plan."""
    product: str
    source_articles: List[SourceArticle] = field(default_factory=list)
    merge_groups: List[MergeGroup] = field(default_factory=list)
    prune_items: List[PruneItem] = field(default_factory=list)
    proposed_categories: List[ProposedCategory] = field(default_factory=list)
    final_doc_list: List[ProposedCategory] = field(default_factory=list)


def parse_reorganization_plan(plan_path: str, product: str = "") -> ReorgPlan:
    """Parse a reorganization plan markdown file into structured data.

    Args:
        plan_path: Path to the reorganization plan .md file.
        product: Product slug (auto-detected from filename if not given).
    """
    with open(plan_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not product:
        basename = os.path.basename(plan_path).upper()
        # Extract product from filename like THRIVE_LEADS_DOCS_REORGANIZATION.md
        m = re.search(r"(THRIVE_\w+?)_(?:DOCS_)?REORGANIZATION", basename)
        product = m.group(1).lower() if m else "unknown"

    plan = ReorgPlan(product=product)

    # Split into sections by ## headings
    sections = _split_sections(content)

    # Parse each section
    for heading, body in sections:
        heading_lower = heading.lower()
        if "full list" in heading_lower or "all docs" in heading_lower:
            plan.source_articles = _parse_source_articles(body)
        elif "merge idea" in heading_lower:
            plan.merge_groups = _parse_merge_groups(body)
        elif "delete" in heading_lower or "prune" in heading_lower:
            plan.prune_items = _parse_prune_items(body)
        elif "category reorganization" in heading_lower:
            plan.proposed_categories = _parse_proposed_categories(body)
        elif "final proposed" in heading_lower:
            plan.final_doc_list = _parse_final_doc_list(body)

    return plan


def _split_sections(content: str) -> List[Tuple[str, str]]:
    """Split markdown by ## headings, returning (heading, body) pairs."""
    parts = re.split(r"^## (.+)$", content, flags=re.MULTILINE)
    sections = []
    # parts[0] is content before first ## heading
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((heading, body))
    return sections


def _parse_markdown_table(text: str) -> List[Dict[str, str]]:
    """Parse a pipe-delimited markdown table into a list of dicts."""
    rows = []
    lines = text.strip().split("\n")
    headers = None
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if not cells:
            continue
        # Skip separator rows
        if all(re.match(r"^[-:]+$", c) for c in cells):
            continue
        if headers is None:
            headers = [_clean_bold(h) for h in cells]
        else:
            row = {}
            for j, h in enumerate(headers):
                row[h] = _clean_bold(cells[j]) if j < len(cells) else ""
            rows.append(row)
    return rows


def _clean_bold(text: str) -> str:
    """Remove markdown bold markers and extra whitespace."""
    return re.sub(r"\*\*", "", text).strip()


def _parse_source_articles(body: str) -> List[SourceArticle]:
    """Parse the full docs listing by category."""
    articles = []
    current_category = ""

    for line in body.split("\n"):
        line = line.strip()
        # Detect category headings (### Category Name)
        cat_match = re.match(r"^###\s+(.+?)(?:\s*\(.*\))?$", line)
        if cat_match:
            current_category = _clean_bold(cat_match.group(1))
            continue

        # Parse table rows (skip headers/separators handled by _parse_markdown_table)
        if line.startswith("|") and not line.startswith("|--") and not line.startswith("| #"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 3 and not re.match(r"^[-:]+$", cells[0]):
                title = _clean_bold(cells[1])
                url = ""
                url_match = re.search(r"(https?://\S+)", cells[2] if len(cells) > 2 else "")
                if url_match:
                    url = url_match.group(1).rstrip(")")
                articles.append(SourceArticle(title=title, url=url, category=current_category))

    return articles


def _parse_merge_groups(body: str) -> List[MergeGroup]:
    """Parse the Merge Ideas table."""
    rows = _parse_markdown_table(body)
    groups = []
    for row in rows:
        name = row.get("Merge group", "")
        target = row.get("Target article (new or existing)", "")
        sources_raw = row.get("Source articles", "")
        rationale = row.get("Rationale", "")

        # Remove (new) or (existing) markers from target
        target = re.sub(r"\s*\((?:new|existing)\)\s*", "", target).strip()

        # Split source articles by comma
        source_titles = [s.strip() for s in sources_raw.split(",") if s.strip()]

        groups.append(MergeGroup(
            name=name,
            target_title=target,
            source_titles=source_titles,
            rationale=rationale,
        ))
    return groups


def _parse_prune_items(body: str) -> List[PruneItem]:
    """Parse the Delete or Prune Ideas table."""
    rows = _parse_markdown_table(body)
    items = []
    for row in rows:
        items.append(PruneItem(
            action=row.get("Action", ""),
            articles=row.get("Article(s)", ""),
            rationale=row.get("Rationale", ""),
        ))
    return items


def _parse_proposed_categories(body: str) -> List[ProposedCategory]:
    """Parse the Proposed structure table."""
    # Look for the "Proposed structure" table
    # Table format: Category | Contents | Article count
    table_section = body
    proposed_match = re.search(r"### Proposed structure.*?\n((?:\|.*\n)+)", body, re.IGNORECASE)
    if proposed_match:
        table_section = proposed_match.group(1)

    rows = _parse_markdown_table(table_section)
    categories = []
    for row in rows:
        name = row.get("Category", "")
        contents = row.get("Contents", "")
        articles = [a.strip() for a in contents.split(",") if a.strip()]
        categories.append(ProposedCategory(name=name, articles=articles))
    return categories


def _parse_final_doc_list(body: str) -> List[ProposedCategory]:
    """Parse the Final Proposed Doc List (numbered lists by category)."""
    categories = []
    current_cat = None

    for line in body.split("\n"):
        line = line.strip()
        # Category heading
        cat_match = re.match(r"^###\s+(.+?)(?:\s*\(.*\))?$", line)
        if cat_match:
            current_cat = ProposedCategory(name=_clean_bold(cat_match.group(1)))
            categories.append(current_cat)
            continue

        # Numbered list items
        item_match = re.match(r"^\d+\.\s+(.+)", line)
        if item_match and current_cat is not None:
            title = _clean_bold(item_match.group(1))
            # Remove italic notes like *(move here—...)*
            title = re.sub(r"\s*\*\(.*?\)\*\s*", "", title).strip()
            # Remove merge notes like (merge: ...)
            title = re.sub(r"\s*\(merge:.*?\)\s*", "", title).strip()
            current_cat.articles.append(title)

    return categories


def generate_batch_from_plan(
    plan: ReorgPlan,
    product_dir: str,
    source_file_map: Optional[Dict[str, str]] = None,
) -> List[dict]:
    """Convert a ReorgPlan into article entries suitable for BatchState.initialize().

    Args:
        plan: The parsed reorganization plan.
        product_dir: Path to the product's directory containing source files.
        source_file_map: Optional mapping of article titles to file paths.
            If not provided, tries to match by searching product_dir.
    """
    articles = []
    file_map = source_file_map or _build_file_map(product_dir)

    # Process merge groups first
    merged_source_titles = set()
    for group in plan.merge_groups:
        merge_sources = []
        for src_title in group.source_titles:
            src_path = _find_source_file(src_title, file_map)
            merge_sources.append({
                "title": src_title,
                "source_file": src_path or "",
            })
            merged_source_titles.add(src_title.lower())

        article_id = _slugify(group.target_title)
        articles.append({
            "id": article_id,
            "title": group.target_title,
            "source_file": "",
            "source_urls": [],
            "merge_sources": merge_sources,
            "merge_instructions": group.rationale,
        })

    # Process standalone articles from the final doc list
    for cat in plan.final_doc_list:
        for title in cat.articles:
            if title.lower() in merged_source_titles:
                continue
            # Check if this title is already covered by a merge group target
            if any(title.lower() == _clean_bold(g.target_title).lower() for g in plan.merge_groups):
                continue

            src_path = _find_source_file(title, file_map)
            article_id = _slugify(title)

            # Skip if already added
            if any(a["id"] == article_id for a in articles):
                continue

            articles.append({
                "id": article_id,
                "title": title,
                "source_file": src_path or "",
                "source_urls": [],
                "merge_sources": [],
                "merge_instructions": "",
            })

    return articles


def _build_file_map(product_dir: str) -> Dict[str, str]:
    """Build a mapping of lowercase title fragments to file paths."""
    file_map = {}
    import glob as _glob
    for fpath in _glob.glob(os.path.join(product_dir, "*.md")):
        basename = os.path.splitext(os.path.basename(fpath))[0]
        # Remove leading number prefix (e.g. "1_getting_started...")
        clean = re.sub(r"^\d+_", "", basename).replace("_", " ").lower()
        file_map[clean] = fpath

        # Also index by H1 title
        with open(fpath, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):
                    h1 = line[2:].strip().lower()
                    file_map[h1] = fpath
                    break
    return file_map


def _find_source_file(title: str, file_map: Dict[str, str]) -> Optional[str]:
    """Find a source file path matching a title using fuzzy matching."""
    title_lower = title.lower()

    # Exact match
    if title_lower in file_map:
        return file_map[title_lower]

    # Substring match
    for key, path in file_map.items():
        if title_lower in key or key in title_lower:
            return path

    # Word overlap match (find best match)
    title_words = set(re.findall(r"\w+", title_lower))
    best_match = None
    best_score = 0
    for key, path in file_map.items():
        key_words = set(re.findall(r"\w+", key))
        overlap = len(title_words & key_words)
        if overlap > best_score and overlap >= 2:
            best_score = overlap
            best_match = path

    return best_match


def _slugify(text: str) -> str:
    """Convert a title to a filesystem-safe slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s-]+", "_", text)
    return text.strip("_")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Parse reorganization plans and generate batch states.")
    parser.add_argument("plan_file", help="Path to the reorganization plan markdown file.")
    parser.add_argument("--product-dir", default=None, help="Product directory with source files.")
    parser.add_argument("--output", default=None, help="Output path for batch_state.json.")
    parser.add_argument("--dry-run", action="store_true", help="Print plan summary without writing state.")
    args = parser.parse_args()

    plan = parse_reorganization_plan(args.plan_file)

    print(f"Product: {plan.product}")
    print(f"Source articles: {len(plan.source_articles)}")
    print(f"Merge groups: {len(plan.merge_groups)}")
    print(f"Prune items: {len(plan.prune_items)}")
    print(f"Proposed categories: {len(plan.proposed_categories)}")
    print(f"Final doc list categories: {len(plan.final_doc_list)}")

    for mg in plan.merge_groups:
        print(f"\n  Merge: {mg.name}")
        print(f"    Target: {mg.target_title}")
        print(f"    Sources: {', '.join(mg.source_titles)}")

    if args.dry_run:
        return

    product_dir = args.product_dir
    if not product_dir:
        # Try to find product dir in knowledge_base/
        kb_dir = os.path.dirname(os.path.abspath(args.plan_file))
        candidate = os.path.join(kb_dir, plan.product)
        if os.path.isdir(candidate):
            product_dir = candidate
        else:
            print(f"Warning: Could not find product directory for '{plan.product}'")
            product_dir = kb_dir

    articles = generate_batch_from_plan(plan, product_dir)

    print(f"\nGenerated {len(articles)} batch articles:")
    for art in articles:
        merge_label = f" (merge: {len(art['merge_sources'])} sources)" if art["merge_sources"] else ""
        print(f"  {art['id']}: {art['title']}{merge_label}")

    if args.output:
        state = BatchState(args.output)
        state.initialize(plan.product, articles)
        print(f"\nBatch state written to: {args.output}")


if __name__ == "__main__":
    main()
