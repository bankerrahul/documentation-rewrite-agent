#!/usr/bin/env python3
"""
WebSocket server to upload screenshots and inject per-step images
for ALL Getting Started articles.

Phase 1: Upload new screenshots (skips already-uploaded ones)
Phase 2: Inject images per-step into Gutenberg content and update drafts

Usage:
    1. Run: python3 ws_publish_all.py
    2. Inject the WebSocket client JS into Chrome (on thrivethemes.com/wp-admin)
    3. Screenshots are uploaded and injected automatically
"""
import asyncio
import base64
import json
import os
import re
import sys

try:
    import websockets
except ImportError:
    os.system(f"{sys.executable} -m pip install websockets -q")
    import websockets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
WP_POSTS_JSON = os.path.join(BASE_DIR, "wp_posts.json")
PORT = 9876

# All Getting Started articles
ARTICLES = [
    "1-01-creating-your-first-course",
    "1-02-course-content-types-navigation-structure",
    "1-03-creating-course-bundles",
    "1-04-creating-a-free-course-funnel",
    "1-05-creating-a-student-profile-page",
    "1-06-ai-powered-course-generation",
    "1-07-using-dynamic-text",
    "1-08-switching-to-thrive-apprentice-from-another-lms",
]


def load_wp_posts():
    with open(WP_POSTS_JSON, "r", encoding="utf-8") as f:
        return {p["filename"]: p for p in json.load(f)}


def load_manifest(article_slug):
    path = os.path.join(SCREENSHOTS_DIR, article_slug, "_manifest.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def inject_images_per_step(content, section_groups, file_to_media):
    """
    For each section, find the ordered list after the heading,
    then for each screenshot, find the Nth <li> and insert
    <br><br><img> before </li>.
    """
    for section_name, screenshots in section_groups.items():
        # Find the section heading
        escaped = re.escape(section_name)
        heading_re = re.compile(r'<h[23][^>]*>' + escaped + r'</h[23]>', re.IGNORECASE)
        match = heading_re.search(content)

        if not match:
            # Fuzzy match: first and last word
            words = section_name.split()
            if len(words) >= 2:
                first = re.escape(words[0])
                last = re.escape(words[-1])
                heading_re = re.compile(
                    r'<h[23][^>]*>[^<]*' + first + r'[^<]*' + last + r'[^<]*</h[23]>',
                    re.IGNORECASE
                )
                match = heading_re.search(content)

        if not match:
            # Try matching just key words from the heading
            words = [w for w in section_name.split() if len(w) > 3]
            if len(words) >= 2:
                pattern = r'<h[23][^>]*>[^<]*'
                for w in words[:3]:
                    pattern += re.escape(w) + r'[^<]*'
                pattern += r'</h[23]>'
                heading_re = re.compile(pattern, re.IGNORECASE)
                match = heading_re.search(content)

        if not match:
            print(f"  WARNING: Heading not found: {section_name}")
            continue

        # Find the first ordered list after this heading
        after_heading = content[match.end():]
        ol_match = re.search(r'<ol[^>]*>(.*?)</ol>', after_heading, re.DOTALL)
        if not ol_match:
            print(f"  WARNING: No <ol> found after: {section_name}")
            continue

        ol_content = ol_match.group(1)

        # Find all <li> tags in this ordered list
        li_pattern = re.compile(r'(<li>)(.*?)(</li>)', re.DOTALL)
        li_matches = list(li_pattern.finditer(ol_content))

        if not li_matches:
            print(f"  WARNING: No <li> items in list for: {section_name}")
            continue

        # Sort screenshots by step number descending (process in reverse so indices don't shift)
        sorted_screenshots = sorted(screenshots, key=lambda s: s["step"], reverse=True)

        modified_ol = ol_content
        for s in sorted_screenshots:
            step_idx = s["step"] - 1  # 0-indexed
            if step_idx >= len(li_matches):
                print(f"  WARNING: Step {s['step']} exceeds list items ({len(li_matches)}) in {section_name}")
                continue

            file_key = s["file"]
            if file_key not in file_to_media:
                print(f"  WARNING: No media for {file_key}")
                continue

            media = file_to_media[file_key]
            img_html = f'<br><br><img src="{media["url"]}" alt="{media["alt"]}">'

            li_m = li_matches[step_idx]
            insert_pos = li_m.end(2)  # end of the content group, before </li>
            modified_ol = modified_ol[:insert_pos] + img_html + modified_ol[insert_pos:]

            # Re-find all li_matches since we modified the string
            li_matches = list(li_pattern.finditer(modified_ol))

            print(f"    Injected {file_key} into step {s['step']} of '{section_name}'")

        # Replace the old ol content with the modified one
        full_ol_start = match.end() + ol_match.start(1)
        full_ol_end = match.end() + ol_match.end(1)
        content = content[:full_ol_start] + modified_ol + content[full_ol_end:]

    return content


async def publish_handler(websocket):
    """Handle Chrome client connection."""
    print("Chrome connected!")
    await websocket.send(json.dumps({"type": "hello", "msg": "Connected to publish server (all Getting Started)"}))

    # Get existing upload results from Chrome (from previous session)
    print("Requesting existing upload results from Chrome...")
    await websocket.send(json.dumps({"type": "request_uploads"}))
    response = await websocket.recv()
    upload_data = json.loads(response)
    file_to_media = upload_data.get("uploads", {})
    print(f"Chrome has {len(file_to_media)} existing media mappings")

    wp_posts = load_wp_posts()

    # ─── Phase 1: Upload new screenshots ───
    print("\n" + "=" * 60)
    print("PHASE 1: Upload new screenshots")
    print("=" * 60)

    all_uploads = []
    seen = set(file_to_media.keys())  # Skip already-uploaded files

    for article in ARTICLES:
        manifest = load_manifest(article)
        if not manifest:
            print(f"  No manifest for {article}, skipping")
            continue

        for s in manifest["screenshots"]:
            if s["file"] in seen:
                continue
            seen.add(s["file"])
            fpath = os.path.join(SCREENSHOTS_DIR, article, s["file"])
            if not os.path.exists(fpath):
                print(f"  File not found: {fpath}")
                continue
            all_uploads.append({
                "file": s["file"],
                "path": fpath,
                "article": article,
                "alt": f"{s['section']} - {s['target']} in Thrive Apprentice",
            })

    print(f"\nNeed to upload {len(all_uploads)} new images (skipping {len(file_to_media)} already uploaded)")

    for i, u in enumerate(all_uploads):
        with open(u["path"], "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")

        print(f"  [{i+1}/{len(all_uploads)}] Sending {u['file']} ({len(b64)//1024}KB)...")

        await websocket.send(json.dumps({
            "type": "upload",
            "filename": u["file"],
            "b64": b64,
            "alt": u["alt"],
            "index": i,
            "total": len(all_uploads),
        }))

        response = await websocket.recv()
        result = json.loads(response)
        if result.get("status") == "ok":
            file_to_media[u["file"]] = {
                "id": result["id"],
                "url": result["url"],
                "alt": u["alt"],
            }
            print(f"    -> OK: ID={result['id']}")
        else:
            print(f"    -> ERROR: {result.get('error', 'unknown')}")

    print(f"\nTotal media: {len(file_to_media)} images")

    # ─── Phase 2: Inject images and update posts ───
    print("\n" + "=" * 60)
    print("PHASE 2: Inject per-step images and update posts")
    print("=" * 60)

    for article_slug in ARTICLES:
        filename = article_slug + ".md"
        if filename not in wp_posts:
            print(f"\n  Skipping {article_slug}: not in wp_posts.json")
            continue

        manifest = load_manifest(article_slug)
        if not manifest:
            print(f"\n  Skipping {article_slug}: no manifest")
            continue

        all_screenshots = manifest["screenshots"]
        if not all_screenshots:
            print(f"\n  Skipping {article_slug}: no screenshots")
            continue

        # Group by section, include step numbers (include ALL steps)
        section_groups = {}
        for s in all_screenshots:
            sec = s["section"]
            if sec not in section_groups:
                section_groups[sec] = []
            section_groups[sec].append({
                "file": s["file"],
                "section": s["section"],
                "target": s["target"],
                "step": s["step"],
            })

        original = wp_posts[filename]
        print(f"\n  Processing: {original['title'][:60]}...")
        print(f"  Sections: {list(section_groups.keys())}")
        print(f"  Screenshots: {len(all_screenshots)}")

        # Inject images per-step into the original content
        new_content = inject_images_per_step(
            original["content"],
            section_groups,
            file_to_media
        )

        added = len(new_content) - len(original["content"])
        print(f"  Content: {len(original['content'])} -> {len(new_content)} (+{added} chars)")

        if added == 0:
            print(f"  WARNING: No images injected for {article_slug}")
            continue

        # Send update command to Chrome
        await websocket.send(json.dumps({
            "type": "update_post",
            "title": original["title"],
            "content": new_content,
        }))

        response = await websocket.recv()
        result = json.loads(response)
        if result.get("status") == "ok":
            print(f"  -> OK: Post {result.get('post_id')} updated")
        else:
            print(f"  -> ERROR: {result.get('error', 'unknown')}")

    await websocket.send(json.dumps({"type": "done"}))
    print("\n" + "=" * 60)
    print("✅ All Getting Started articles published!")
    print("=" * 60)


async def main():
    print(f"Starting publish server on ws://localhost:{PORT}")
    print(f"Articles: {len(ARTICLES)}")
    print(f"Waiting for Chrome to connect...\n")

    async with websockets.serve(
        publish_handler,
        "localhost",
        PORT,
        max_size=50 * 1024 * 1024,  # 50MB max message size
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
