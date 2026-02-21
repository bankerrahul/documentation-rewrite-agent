#!/usr/bin/env python3
"""
Converts markdown+gutenberg files to proper Gutenberg HTML blocks
and outputs a JSON file for WordPress REST API batch import.
"""
import os
import re
import json

DOCS_DIR = os.path.join(os.path.dirname(__file__), 'new_docs')

# Category mapping: filename prefix -> WP category IDs
# Based on existing ht_kb_category taxonomy
CATEGORY_MAP = {
    '1-': [34177],   # Getting Started
    '2-': [34070],   # Thrive Apprentice Settings (closest to Course Setup)
    '3-': [34057],   # Products
    '4-': [34064],   # Designing Courses
    '5-': [34066],   # Drip
    '6-': [34062],   # Integrations
    '7-': [34071],   # Thrive Apprentice and Thrive Automator
    '8-': [34059],   # Course Completion and Certificates
    '9-': [34094],   # Translation
    '10-': [34106],  # Working with SendOwl
}

# Override for specific files
CATEGORY_OVERRIDES = {
    '7-02-using-quizzes.md': [34063],           # Quiz Builder
    '7-03-enabling-assessments.md': [34179],     # Assessments
    '7-04-assessment-upload-settings.md': [34179],
    '7-05-refreshing-templates-after-assessments.md': [34179],
    '6-04-connecting-thrivecart.md': [34140],    # ThriveCart
    '8-04-using-the-reports-section.md': [34065], # Reporting Section
    '8-05-viewing-member-data.md': [34065],
    '8-06-sorting-students-enrollment-date.md': [34065],
}


def get_categories(filename):
    """Get category IDs for a filename."""
    if filename in CATEGORY_OVERRIDES:
        return CATEGORY_OVERRIDES[filename]
    for prefix, cats in CATEGORY_MAP.items():
        if filename.startswith(prefix):
            return cats
    return []


def md_to_gutenberg_html(md_content):
    """Convert markdown-with-gutenberg-comments to proper Gutenberg HTML blocks."""
    # Remove the H1 title block (first heading level 1) - title goes in post title
    md_content = re.sub(
        r'<!-- wp:heading \{"level":1\} -->\s*#\s+.*?\s*<!-- /wp:heading -->\s*',
        '',
        md_content,
        count=1
    )

    lines = md_content.strip().split('\n')
    result = []
    i = 0
    in_block = False
    block_type = None
    block_attrs = ''
    block_content = []

    while i < len(lines):
        line = lines[i]

        # Opening block comment
        open_match = re.match(r'^<!-- wp:(\w+)(?:\s+(\{.*?\}))?\s*-->\s*$', line)
        close_match = re.match(r'^<!-- /wp:(\w+)\s*-->\s*$', line)

        # Special case: wp:embed blocks - pass through as-is
        embed_match = re.match(r'^<!-- wp:embed\s+', line)
        if embed_match:
            # Collect everything until <!-- /wp:embed -->
            embed_lines = [line]
            i += 1
            while i < len(lines):
                embed_lines.append(lines[i])
                if '<!-- /wp:embed -->' in lines[i]:
                    i += 1
                    break
                i += 1
            result.append('\n'.join(embed_lines))
            continue

        # Special case: wp:html blocks - pass through as-is
        html_match = re.match(r'^<!-- wp:html\s*-->', line)
        if html_match:
            html_lines = [line]
            i += 1
            while i < len(lines):
                html_lines.append(lines[i])
                if '<!-- /wp:html -->' in lines[i]:
                    i += 1
                    break
                i += 1
            result.append('\n'.join(html_lines))
            continue

        if open_match and not in_block:
            block_type = open_match.group(1)
            block_attrs = open_match.group(2) or ''
            block_content = []
            in_block = True
            i += 1
            continue

        if close_match and in_block:
            # Process the block
            content_text = '\n'.join(block_content).strip()
            html_block = convert_block(block_type, block_attrs, content_text)
            result.append(html_block)
            in_block = False
            block_type = None
            block_content = []
            i += 1
            continue

        if in_block:
            block_content.append(line)
        else:
            # Pass through non-block content
            if line.strip():
                result.append(line)

        i += 1

    return '\n\n'.join(result)


def convert_block(block_type, attrs_str, content):
    """Convert a single block from markdown to Gutenberg HTML."""
    attrs = json.loads(attrs_str) if attrs_str else {}

    if block_type == 'heading':
        level = attrs.get('level', 2)
        # Strip markdown heading markers
        text = re.sub(r'^#{1,6}\s+', '', content)
        text = md_inline_to_html(text)
        attrs_comment = f' {json.dumps(attrs)}' if attrs else ''
        return f'<!-- wp:heading{attrs_comment} -->\n<h{level}>{text}</h{level}>\n<!-- /wp:heading -->'

    elif block_type == 'paragraph':
        text = md_inline_to_html(content)
        return f'<!-- wp:paragraph -->\n<p>{text}</p>\n<!-- /wp:paragraph -->'

    elif block_type == 'list':
        ordered = attrs.get('ordered', False)
        attrs_comment = f' {json.dumps(attrs)}' if attrs else ''
        items = parse_list_items(content)
        tag = 'ol' if ordered else 'ul'
        items_html = ''.join(f'<li>{md_inline_to_html(item)}</li>' for item in items)
        return f'<!-- wp:list{attrs_comment} -->\n<{tag}>{items_html}</{tag}>\n<!-- /wp:list -->'

    elif block_type == 'embed':
        # Should be handled before this, but fallback
        return f'<!-- wp:embed {attrs_str} -->\n{content}\n<!-- /wp:embed -->'

    else:
        # Unknown block type - pass through
        return f'<!-- wp:{block_type} {attrs_str} -->\n{content}\n<!-- /wp:{block_type} -->'


def md_inline_to_html(text):
    """Convert markdown inline formatting to HTML."""
    # Bold: **text** -> <strong>text</strong>
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text* -> <em>text</em>
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Code: `text` -> <code>text</code>
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Links: [text](url) -> <a href="url">text</a>
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Escape angle brackets for HTML attributes (> in navigation paths)
    text = text.replace(' > ', ' &gt; ')
    # HTML entities for & in text (but not in existing HTML entities)
    text = re.sub(r'&(?!amp;|gt;|lt;|quot;|#\d+;|#x[0-9a-fA-F]+;)', '&amp;', text)
    return text


def parse_list_items(content):
    """Parse markdown list items."""
    items = []
    current_item = None

    for line in content.split('\n'):
        # Ordered list item
        ol_match = re.match(r'^\d+\.\s+(.+)', line)
        # Unordered list item
        ul_match = re.match(r'^[-*]\s+(.+)', line)

        if ol_match:
            if current_item is not None:
                items.append(current_item)
            current_item = ol_match.group(1)
        elif ul_match:
            if current_item is not None:
                items.append(current_item)
            current_item = ul_match.group(1)
        elif line.strip() and current_item is not None:
            # Continuation of previous item
            current_item += ' ' + line.strip()

    if current_item is not None:
        items.append(current_item)

    return items


def extract_title(md_content):
    """Extract the H1 title from markdown content."""
    match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def main():
    posts = []

    for filename in sorted(os.listdir(DOCS_DIR)):
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(DOCS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()

        title = extract_title(md_content)
        if not title:
            print(f"WARNING: No title found in {filename}")
            continue

        gutenberg_html = md_to_gutenberg_html(md_content)
        categories = get_categories(filename)

        posts.append({
            'filename': filename,
            'title': title,
            'content': gutenberg_html,
            'categories': categories,
            'status': 'draft'
        })

    output_path = os.path.join(os.path.dirname(__file__), 'wp_posts.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(posts)} posts -> {output_path}")

    # Print category summary
    cat_counts = {}
    for p in posts:
        for c in p['categories']:
            cat_counts[c] = cat_counts.get(c, 0) + 1
    print("\nCategory distribution:")
    for cat_id, count in sorted(cat_counts.items()):
        print(f"  Category {cat_id}: {count} articles")


if __name__ == '__main__':
    main()
