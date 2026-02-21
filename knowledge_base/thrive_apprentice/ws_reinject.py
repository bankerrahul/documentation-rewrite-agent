#!/usr/bin/env python3
"""
WebSocket server to re-inject images with per-step placement.

Instead of inserting all images after <!-- /wp:list -->, this version
inserts each image INSIDE its corresponding <li> tag using <br><br><img>.

This preserves the ordered list structure while placing screenshots
right after each step, matching Rahul's manual workflow.
"""
import asyncio
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
            print(f"  WARNING: Heading not found: {section_name}")
            continue

        # Find the first ordered list after this heading
        after_heading = content[match.end():]
        ol_match = re.search(r'<ol[^>]*>(.*?)</ol>', after_heading, re.DOTALL)
        if not ol_match:
            print(f"  WARNING: No <ol> found after: {section_name}")
            continue

        ol_start_in_content = match.end() + ol_match.start()
        ol_content = ol_match.group(1)

        # Find all <li> tags in this ordered list
        li_pattern = re.compile(r'(<li>)(.*?)(</li>)', re.DOTALL)
        li_matches = list(li_pattern.finditer(ol_content))

        if not li_matches:
            print(f"  WARNING: No <li> items in list for: {section_name}")
            continue

        # Sort screenshots by step number
        sorted_screenshots = sorted(screenshots, key=lambda s: s["step"], reverse=True)

        # Process in reverse order so indices don't shift
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
            # Insert img before </li>
            insert_pos = li_m.end(2)  # end of the content group, before </li>
            modified_ol = modified_ol[:insert_pos] + img_html + modified_ol[insert_pos:]

            # Re-find all li_matches since we modified the string
            li_matches = list(li_pattern.finditer(modified_ol))

            print(f"    Injected {file_key} into step {s['step']} of '{section_name}'")

        # Replace the old ol content with the modified one
        full_ol_start = match.end() + ol_match.start(1)  # start of ol inner content
        full_ol_end = match.end() + ol_match.end(1)      # end of ol inner content
        content = content[:full_ol_start] + modified_ol + content[full_ol_end:]

    return content


async def reinject_handler(websocket):
    """Handle Chrome client connection for re-injection."""
    print("Chrome connected!")
    await websocket.send(json.dumps({"type": "hello", "msg": "Connected to re-inject server"}))

    # Wait for Chrome to send us the upload results
    print("Waiting for upload results from Chrome...")
    await websocket.send(json.dumps({"type": "request_uploads"}))

    response = await websocket.recv()
    upload_data = json.loads(response)
    file_to_media = upload_data.get("uploads", {})
    print(f"Received {len(file_to_media)} media mappings")

    articles = ["1-01-creating-your-first-course", "2-01-settings-guide"]
    wp_posts = load_wp_posts()

    for article_slug in articles:
        filename = article_slug + ".md"
        if filename not in wp_posts:
            continue

        manifest = load_manifest(article_slug)
        if not manifest:
            continue

        annotated = [s for s in manifest["screenshots"] if s.get("found")]

        # Group by section, include step numbers
        section_groups = {}
        for s in annotated:
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

        # Inject images per-step into the original content
        new_content = inject_images_per_step(
            original["content"],
            section_groups,
            file_to_media
        )

        added = len(new_content) - len(original["content"])
        print(f"  Content: {len(original['content'])} -> {len(new_content)} (+{added} chars)")

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
    print("\n✅ All done!")


async def main():
    print(f"Starting re-inject server on ws://localhost:{PORT}")
    print(f"Waiting for Chrome to connect...\n")

    async with websockets.serve(reinject_handler, "localhost", PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
