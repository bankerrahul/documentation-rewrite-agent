"""
Step parser for documentation markdown files.
Extracts ordered-list steps with bold UI element targets from Gutenberg-compatible markdown.

This module is product-agnostic — it works with any markdown documentation
that uses Gutenberg ordered-list blocks with bold UI element targets.
"""

import json
import os
import re
from typing import Dict, List, Optional


def slugify(text: str) -> str:
    """Convert heading text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def extract_title(content: str) -> str:
    """Extract the H1 title from the markdown content."""
    # Try Gutenberg H1 heading
    m = re.search(r'<!-- wp:heading\s*\{"level"\s*:\s*1\}\s*-->\s*#\s*(.+)', content)
    if m:
        return m.group(1).strip()
    # Try plain H1
    m = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "Untitled"


def infer_target_from_text(clean_text: str, action: str) -> str:
    """Try to infer a UI target from non-bold step text.

    For steps without bold UI elements, we try to extract something
    useful for element_finder to search for. Returns empty string if
    no target can be inferred.
    """
    text_lower = clean_text.lower().strip()

    # 1. Quoted text (e.g., 'Click "Add Course"', 'Select "My Plugin"')
    quoted = re.findall(r'"([^"]+)"', clean_text) + re.findall(r"'([^']+)'", clean_text)
    # Also match text in single backtick-like quotes
    quoted += re.findall(r'\u201c([^\u201d]+)\u201d', clean_text)  # curly quotes
    if quoted:
        # Use the first quoted string as the target
        return quoted[0]

    # 2. Known UI keywords that map to specific elements
    ui_keyword_map = {
        "course overview": "Course Overview",
        "cover image": "Cover Image",
        "course summary": "Course summary",
        "course description": "Course Description",
        "course title": "Course Title",
        "module title": "Module Title",
        "lesson title": "Lesson Title",
        "chapter title": "Chapter Title",
        "add course": "Add Course",
        "add lesson": "Add Lesson",
        "add module": "Add Module",
        "add chapter": "Add Chapter",
        "payment gateway": "Payments",
        "branding": "Design",
        "typography": "Design",
        "school design": "Design",
        "template": "Design",
        "layout": "Design",
        "drip schedule": "Drip",
        "access restrictions": "Access restrictions",
        "student profile": "Student Profile",
        "save": "Save",
        "publish": "Publish",
    }
    for keyword, target in ui_keyword_map.items():
        if keyword in text_lower:
            return target

    # 3. Extract noun phrase after action verb
    # E.g., "Configure the layout for your course pages" → "layout"
    # E.g., "Set up your branding" → "branding"
    action_noun_patterns = [
        r"(?:click|select|choose|open|navigate to|go to)\s+(?:the\s+|a\s+|an\s+)?(.+?)(?:\s+(?:to|for|from|in|on|and|or)\b|[.,;]|$)",
        r"(?:configure|set up|customize|adjust|modify|update)\s+(?:the\s+|your\s+|a\s+)?(.+?)(?:\s+(?:to|for|from|in|on|and|or)\b|[.,;]|$)",
        r"(?:create|add|enable|disable|connect|associate)\s+(?:the\s+|your\s+|a\s+|an\s+)?(.+?)(?:\s+(?:to|for|from|in|on|and|or|with)\b|[.,;]|$)",
    ]
    for pattern in action_noun_patterns:
        m = re.search(pattern, text_lower)
        if m:
            noun = m.group(1).strip()
            # Filter out very long or generic phrases
            if noun and len(noun) < 40 and noun not in (
                "it", "this", "that", "them", "one", "each",
                "your", "the", "a", "an", "own",
            ):
                return noun.title()

    return ""


def parse_action_and_target(step_text: str) -> Dict:
    """Parse a single step's raw text to extract action, target, and context.

    Returns:
        {
            'action': str,         # click, hover, navigate, type, locate, toggle, drag
            'target': str,         # The bold UI element name
            'target_bold': bool,   # Whether target came from bold text
            'context': str,        # Surrounding descriptive context
        }
    """
    # Extract all bold text segments
    bold_matches = re.findall(r"\*\*(.+?)\*\*", step_text)
    # Also handle HTML bold from wp_posts content
    bold_matches += re.findall(r"<strong>(.+?)</strong>", step_text)

    # Clean the text for action detection
    clean = re.sub(r"\*\*(.+?)\*\*", r"\1", step_text)
    clean = re.sub(r"<strong>(.+?)</strong>", r"\1", clean)
    clean_lower = clean.lower().strip()

    # Detect action verb
    action = "locate"  # default: just find and screenshot, no action
    action_patterns = [
        (r"^click\b", "click"),
        (r"^press\b", "click"),
        (r"^select\b", "click"),
        (r"^choose\b", "click"),
        (r"^check\b", "toggle"),
        (r"^uncheck\b", "toggle"),
        (r"^enable\b", "toggle"),
        (r"^disable\b", "toggle"),
        (r"^toggle\b", "toggle"),
        (r"^switch\b", "toggle"),
        (r"^turn\s+on\b", "toggle"),
        (r"^turn\s+off\b", "toggle"),
        (r"^hover\s+over\b", "hover"),
        (r"^hover\b", "hover"),
        (r"^navigate\s+to\b", "navigate"),
        (r"^go\s+to\b", "navigate"),
        (r"^open\b", "navigate"),
        (r"^visit\b", "navigate"),
        (r"^enter\b", "type"),
        (r"^type\b", "type"),
        (r"^fill\s+in\b", "type"),
        (r"^input\b", "type"),
        (r"^scroll\s+to\b", "scroll"),
        (r"^scroll\b", "scroll"),
        (r"^locate\b", "locate"),
        (r"^find\b", "locate"),
        (r"^look\s+for\b", "locate"),
        (r"^drag\b", "drag"),
        (r"^change\b", "click"),
        (r"^set\b", "click"),
        (r"^update\b", "click"),
    ]

    for pattern, act in action_patterns:
        if re.search(pattern, clean_lower):
            action = act
            break

    # Pick the primary target (first bold item, or first meaningful bold)
    target = ""
    target_bold = False

    # Filter out non-UI bold items (like "Tip:", "Note:", "Important:", "or")
    ui_bolds = [
        b for b in bold_matches
        if b.lower() not in ("tip:", "note:", "important:", "or", "and")
        and not b.endswith(":")
    ]

    if ui_bolds:
        target = ui_bolds[0]
        target_bold = True
    elif bold_matches:
        target = bold_matches[0]
        target_bold = True

    # Extract context: everything after the action verb and target
    context = ""
    if target:
        # Get text after the target mention
        idx = clean.find(target)
        if idx >= 0:
            after = clean[idx + len(target):].strip(" .,;\u2014-")
            # Clean up common prefixes
            after = re.sub(r"^(in|on|at|from|to|of)\s+the\s+", "", after, flags=re.I)
            after = re.sub(r"^(in|on|at|from|to|of)\s+", "", after, flags=re.I)
            context = after.strip(" .,;\u2014-")[:80]  # Trim to reasonable length

    # --- Post-processing for toggle steps with generic On/Off targets ---
    if action == "toggle" and target.lower() in ("on", "off"):
        toggle_state = target  # "On" or "Off"
        # Look for a better target in the other bold items
        other_bolds = [b for b in ui_bolds if b.lower() not in ("on", "off")]
        if other_bolds:
            target = other_bolds[0]
            context = f"toggle {toggle_state}, {context}" if context else f"toggle {toggle_state}"
        else:
            feature_match = re.search(
                r"to\s+(?:enable|disable|activate|deactivate)\s+(.+?)(?:\s+for\b|\s+on\b|\s+in\b|\.|$)",
                clean_lower
            )
            if feature_match:
                feature = feature_match.group(1).strip(" .,")
                if feature and feature.lower() not in ("it", "this", "the"):
                    target = feature.title()
                    context = f"toggle {toggle_state}, {context}" if context else f"toggle {toggle_state}"

    # --- Infer target from text for non-bold steps ---
    has_target = bool(target)
    if not target:
        target = infer_target_from_text(clean, action)
        has_target = bool(target)

    return {
        "action": action,
        "target": target,
        "target_bold": target_bold,
        "has_target": has_target,
        "context": context,
    }


def parse_ordered_list_block(block_text: str) -> List[Dict]:
    """Parse an ordered list block into individual steps.

    Handles both markdown syntax (1. 2. 3.) and HTML (<ol><li>...</li></ol>).
    """
    steps = []

    # Try HTML format first (from wp_posts.json content)
    li_matches = re.findall(r"<li>(.*?)</li>", block_text, re.DOTALL)
    if li_matches:
        for i, li_text in enumerate(li_matches):
            # Strip nested HTML tags except <strong>
            clean_li = re.sub(r"<(?!/?strong\b)[^>]+>", "", li_text).strip()
            parsed = parse_action_and_target(clean_li)
            steps.append({
                "step_num": i + 1,
                "raw_text": clean_li,
                **parsed,
            })
        return steps

    # Try markdown numbered list format
    lines = block_text.strip().split("\n")
    for line in lines:
        m = re.match(r"^\s*(\d+)\.\s+(.+)", line.strip())
        if m:
            step_num = int(m.group(1))
            text = m.group(2).strip()
            parsed = parse_action_and_target(text)
            steps.append({
                "step_num": step_num,
                "raw_text": text,
                **parsed,
            })

    return steps


def parse_article(filepath: str) -> Dict:
    """Parse a documentation markdown file into a structured spec.

    Returns:
        {
            'filename': str,
            'title': str,
            'sections': [
                {
                    'heading': str,
                    'heading_slug': str,
                    'steps': [
                        {
                            'step_num': int,
                            'raw_text': str,
                            'action': str,
                            'target': str,
                            'target_bold': bool,
                            'context': str,
                        }
                    ]
                }
            ]
        }
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    filename = os.path.basename(filepath)
    title = extract_title(content)

    sections = []
    current_heading = "Introduction"

    # Split by heading blocks
    # Match both: <!-- wp:heading --> ## Heading and plain ## Heading
    parts = re.split(r"(<!-- wp:heading[^>]*-->\s*#{1,3}\s+.+?\n)", content)

    for part in parts:
        # Check if this is a heading line
        heading_match = re.search(r"#{1,3}\s+(.+)", part)
        if heading_match and "wp:heading" in part:
            current_heading = heading_match.group(1).strip()
            continue

        # Look for ordered list blocks in this section
        # Pattern 1: Gutenberg ordered list blocks
        ordered_blocks = re.findall(
            r'<!-- wp:list\s*\{[^}]*"ordered"\s*:\s*true[^}]*\}\s*-->\s*(.*?)<!-- /wp:list -->',
            part,
            re.DOTALL,
        )

        for block in ordered_blocks:
            steps = parse_ordered_list_block(block)
            if steps:
                # Include ALL steps — bold targets get annotated screenshots,
                # non-bold steps get plain screenshots of the current page state
                sections.append({
                    "heading": current_heading,
                    "heading_slug": slugify(current_heading),
                    "steps": steps,
                })

    return {
        "filename": filename,
        "title": title,
        "sections": sections,
    }


def parse_all_articles(docs_dir: str, output_dir: str) -> List[Dict]:
    """Parse all markdown files in docs_dir and write JSON specs to output_dir.

    Returns list of all parsed specs.
    """
    os.makedirs(output_dir, exist_ok=True)

    all_specs = []
    md_files = sorted(
        f for f in os.listdir(docs_dir) if f.endswith(".md")
    )

    for md_file in md_files:
        filepath = os.path.join(docs_dir, md_file)
        spec = parse_article(filepath)

        # Count total screenshottable steps
        total_steps = sum(len(s["steps"]) for s in spec["sections"])

        if total_steps > 0:
            # Write spec JSON
            spec_filename = md_file.replace(".md", ".json")
            spec_path = os.path.join(output_dir, spec_filename)
            with open(spec_path, "w", encoding="utf-8") as f:
                json.dump(spec, f, indent=2, ensure_ascii=False)

            all_specs.append(spec)
            print(f"  {md_file}: {len(spec['sections'])} sections, {total_steps} steps")
        else:
            print(f"  {md_file}: no screenshottable steps (skipped)")

    return all_specs


if __name__ == "__main__":
    import sys

    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "specs"

    print(f"Parsing articles from {docs_dir}...")
    specs = parse_all_articles(docs_dir, output_dir)
    total_steps = sum(sum(len(s["steps"]) for s in spec["sections"]) for spec in specs)
    print(f"\nDone: {len(specs)} articles, {total_steps} total screenshottable steps")
