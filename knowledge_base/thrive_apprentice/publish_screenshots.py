#!/usr/bin/env python3
"""
Upload annotated screenshots to WordPress media library and update
draft posts with Gutenberg image blocks on thrivethemes.com.

APPROACH: Takes the ORIGINAL Gutenberg HTML from wp_posts.json (preserving
all typography exactly) and injects wp:image blocks after each section's
ordered list, based on the screenshot manifest.

Usage:
    python3 publish_screenshots.py [--article SLUG] [--all] [--local]
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from wordpress_client import WordPressClient

BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(BASE_DIR, "new_docs")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
WP_POSTS_JSON = os.path.join(BASE_DIR, "wp_posts.json")

# Production defaults (thrivethemes.com)
PROD_URL = "https://thrivethemes.com"
PROD_POST_TYPE = "ht-kb"
PROD_CATEGORY_KEY = "ht-kb-category"

# Local defaults (for --local flag)
LOCAL_URL = "http://thrive-themes.local"
LOCAL_POST_TYPE = "posts"


def load_wp_posts() -> dict:
    """Load wp_posts.json and return filename->post mapping."""
    with open(WP_POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)
    return {p["filename"]: p for p in posts}


def load_manifest(article_slug: str) -> dict:
    """Load the screenshot manifest for an article."""
    manifest_path = os.path.join(SCREENSHOTS_DIR, article_slug, "_manifest.json")
    if not os.path.exists(manifest_path):
        return None
    with open(manifest_path, "r") as f:
        return json.load(f)


def get_annotated_screenshots(manifest: dict) -> list:
    """Get only the screenshots that have arrows (found=true)."""
    return [s for s in manifest.get("screenshots", []) if s.get("found")]


def group_screenshots_by_section(screenshots: list) -> dict:
    """Group screenshots by section heading."""
    groups = {}
    for s in screenshots:
        section = s["section"]
        if section not in groups:
            groups[section] = []
        groups[section].append(s)
    return groups


def upload_article_screenshots(
    client: WordPressClient, article_slug: str, screenshots: list
) -> dict:
    """Upload screenshots and return file->media mapping."""
    file_to_media = {}
    article_dir = os.path.join(SCREENSHOTS_DIR, article_slug)

    for s in screenshots:
        filename = s["file"]
        abs_path = os.path.join(article_dir, filename)

        if not os.path.exists(abs_path):
            print(f"  WARNING: {abs_path} not found, skipping.")
            continue

        if filename in file_to_media:
            continue

        alt_text = f"{s['section']} - {s['target']} in Thrive Apprentice"
        print(f"  Uploading: {filename}...")
        try:
            media = client.upload_media(abs_path, alt_text=alt_text)
            file_to_media[filename] = {
                "id": media.id,
                "url": media.source_url,
                "alt": alt_text,
            }
            print(f"    -> {media.source_url} (ID: {media.id})")
        except Exception as e:
            print(f"    ERROR: {e}")

    return file_to_media


def make_image_block(media_info: dict) -> str:
    """Create a Gutenberg wp:image block string."""
    mid = media_info["id"]
    url = media_info["url"]
    alt = media_info["alt"]
    return (
        f'<!-- wp:image {{"id":{mid},"sizeSlug":"large"}} -->\n'
        f'<figure class="wp-block-image size-large">'
        f'<img src="{url}" alt="{alt}" class="wp-image-{mid}"/>'
        f'</figure>\n'
        f'<!-- /wp:image -->'
    )


def inject_images_into_content(
    original_content: str,
    section_screenshots: dict,
    file_to_media: dict,
) -> str:
    """Inject wp:image blocks into the original Gutenberg HTML content.

    Strategy: For each section that has screenshots, find the <!-- /wp:list -->
    that closes the ordered list in that section, and insert the image blocks
    right after it.

    We locate sections by finding their <!-- wp:heading --> blocks with <h2>
    or <h3> tags, then finding the next <!-- /wp:list --> after each heading.
    """
    content = original_content

    for section_name, screenshots in section_screenshots.items():
        # Build the image blocks HTML for this section
        image_blocks = []
        for s in screenshots:
            if s["file"] in file_to_media:
                image_blocks.append(make_image_block(file_to_media[s["file"]]))

        if not image_blocks:
            continue

        images_html = "\n\n".join(image_blocks)

        # Find the section heading in the content
        # Match <h2>Section Name</h2> or <h3>Section Name</h3>
        # Account for possible inline HTML like <strong>
        heading_pattern = re.escape(section_name)
        # Try to find the heading
        heading_match = re.search(
            rf'<h[23]>{heading_pattern}</h[23]>',
            content,
            re.IGNORECASE,
        )

        if not heading_match:
            # Try with less strict matching (partial match)
            heading_match = re.search(
                rf'<h[23]>[^<]*{re.escape(section_name.split()[0])}[^<]*{re.escape(section_name.split()[-1])}[^<]*</h[23]>',
                content,
                re.IGNORECASE,
            )

        if not heading_match:
            print(f"  WARNING: Could not find heading '{section_name}' in content.")
            continue

        # From the heading position, find the next <!-- /wp:list --> block
        search_start = heading_match.end()
        list_close_match = re.search(
            r'<!-- /wp:list -->',
            content[search_start:],
        )

        if not list_close_match:
            print(f"  WARNING: No list found after heading '{section_name}'.")
            continue

        # Insert image blocks right after <!-- /wp:list -->
        insert_pos = search_start + list_close_match.end()
        content = content[:insert_pos] + "\n\n" + images_html + content[insert_pos:]

    return content


def find_draft_post(client: WordPressClient, title: str):
    """Find a draft post by title search.

    Searches across draft/publish/any statuses. For ht-kb posts on
    thrivethemes.com the title is matched against rendered output.
    """
    endpoint = f"{client.api_base}/{client.post_type}"
    for status in ["draft", "publish", "any"]:
        try:
            resp = client.session.get(
                endpoint,
                params={"search": title, "status": status, "per_page": 20},
            )
            if resp.status_code == 200:
                posts = resp.json()
                for post in posts:
                    rendered_title = post.get("title", {}).get("rendered", "")
                    if rendered_title.strip() == title.strip():
                        return post
        except Exception:
            continue
    return None


def process_article(client: WordPressClient, filename: str):
    """Process a single article: upload screenshots, inject into original content, publish."""
    article_slug = filename.replace(".md", "")

    print(f"\n{'='*60}")
    print(f"Processing: {filename}")
    print(f"{'='*60}")

    # Load the original content from wp_posts.json (preserves exact typography)
    wp_posts = load_wp_posts()
    if filename not in wp_posts:
        print(f"  ERROR: {filename} not found in wp_posts.json")
        return

    original = wp_posts[filename]
    title = original["title"]
    original_content = original["content"]
    categories = original.get("categories", [])
    print(f"  Title: {title}")
    print(f"  Original content: {len(original_content)} chars")

    # Load screenshot manifest
    manifest = load_manifest(article_slug)
    if not manifest:
        print(f"  No screenshot manifest found for {article_slug}")
        return

    # Get only annotated screenshots
    annotated = get_annotated_screenshots(manifest)
    if not annotated:
        print(f"  No annotated screenshots found.")
        return

    print(f"  Annotated screenshots: {len(annotated)}")

    # Group by section
    section_groups = group_screenshots_by_section(annotated)
    print(f"  Sections with screenshots: {list(section_groups.keys())}")

    # Step 1: Upload screenshots
    print("\n  Step 1: Uploading screenshots...")
    file_to_media = upload_article_screenshots(client, article_slug, annotated)
    print(f"  Uploaded {len(file_to_media)} images.")

    # Step 2: Inject image blocks into original content
    print("\n  Step 2: Injecting image blocks into original content...")
    new_content = inject_images_into_content(
        original_content, section_groups, file_to_media
    )
    print(f"  New content: {len(new_content)} chars (+{len(new_content) - len(original_content)} from images)")

    # Step 3: Find or create the draft post
    print("\n  Step 3: Finding/creating draft post...")
    post = find_draft_post(client, title)

    wp_url = client.base_url

    if post:
        post_id = post["id"]
        print(f"  Found existing: ID={post_id}")
        endpoint = f"{client.api_base}/{client.post_type}/{post_id}"
        resp = client.session.post(endpoint, json={"content": new_content})
        resp.raise_for_status()
        updated = resp.json()
        link = updated.get("link", "")
        print(f"  Updated successfully!")
        print(f"  Edit:    {wp_url}/wp-admin/post.php?post={post_id}&action=edit")
        print(f"  Preview: {link}?preview=true" if link else f"  Preview: {wp_url}/?p={post_id}&preview=true")
    else:
        print(f"  Creating new draft...")
        new_post = client.create_post(
            title=title,
            content=new_content,
            status="draft",
            categories=categories,
            post_type=client.post_type,
        )
        post_id = new_post.id
        print(f"  Created: ID={post_id}")
        print(f"  Edit:    {wp_url}/wp-admin/post.php?post={post_id}&action=edit")
        print(f"  Preview: {new_post.link}?preview=true" if new_post.link else f"  Preview: {wp_url}/?p={post_id}&preview=true")


def main():
    import argparse
    from dotenv import load_dotenv

    load_dotenv(os.path.join(BASE_DIR, "..", ".env"))

    parser = argparse.ArgumentParser(description="Upload screenshots and update WP drafts.")
    parser.add_argument(
        "--article",
        help="Process a specific article (filename without .md)",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Process all articles that have screenshot manifests",
    )
    parser.add_argument(
        "--local", action="store_true",
        help="Target local dev site (thrive-themes.local) instead of production",
    )
    args = parser.parse_args()

    if args.local:
        # Local dev site
        wp_url = os.getenv("WP_URL", LOCAL_URL).rstrip("/")
        wp_user = os.getenv("WP_USERNAME", "rahul")
        wp_pass = os.getenv("WP_PASSWORD", "baroda")
        post_type = LOCAL_POST_TYPE
        headless = True
        print(f"Mode: LOCAL ({wp_url})")
    else:
        # Production (thrivethemes.com)
        wp_url = os.getenv("PROD_WP_URL", PROD_URL).rstrip("/")
        wp_user = os.getenv("PROD_WP_USERNAME", os.getenv("WP_USERNAME", "rahul"))
        wp_pass = os.getenv("PROD_WP_PASSWORD", os.getenv("WP_PASSWORD", "baroda"))
        post_type = PROD_POST_TYPE
        headless = False  # Need visible browser for 2FA
        print(f"Mode: PRODUCTION ({wp_url})")

    print(f"Post type: {post_type}")

    with WordPressClient(
        base_url=wp_url,
        username=wp_user,
        password=wp_pass,
        headless=headless,
        post_type=post_type,
    ) as client:
        if args.article:
            filename = args.article
            if not filename.endswith(".md"):
                filename += ".md"
            process_article(client, filename)
        elif args.all:
            for d in sorted(os.listdir(SCREENSHOTS_DIR)):
                manifest_path = os.path.join(SCREENSHOTS_DIR, d, "_manifest.json")
                if os.path.exists(manifest_path):
                    process_article(client, d + ".md")
        else:
            process_article(client, "1-01-creating-your-first-course.md")
            process_article(client, "2-01-settings-guide.md")


if __name__ == "__main__":
    main()
