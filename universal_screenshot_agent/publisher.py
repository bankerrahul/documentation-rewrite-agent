#!/usr/bin/env python3
"""
Generic WebSocket-based screenshot publisher.

Starts a WebSocket server on localhost:9876. Chrome connects to it and
receives commands to upload images and update posts. This bypasses
Cloudflare/CORS issues since ws://localhost is allowed from HTTPS pages.

All product-specific settings (articles, post type, alt text) come from
the ProductAdapter config.

Usage:
    1. Run via CLI: python -m universal_screenshot_agent.run -p thrive_apprentice publish
    2. Inject the WebSocket client JS into Chrome (on the production site's wp-admin)
    3. Screenshots are uploaded and injected automatically
"""

import asyncio
import base64
import json
import os
import re
import sys

import websockets


PORT = 9876


def inject_images_per_step(content, section_groups, file_to_media):
    """For each section, find the ordered list after the heading,
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
            # Try matching key words from the heading
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

        # Sort screenshots by step number descending (process in reverse)
        sorted_screenshots = sorted(screenshots, key=lambda s: s["step"], reverse=True)

        modified_ol = ol_content
        for s in sorted_screenshots:
            step_idx = s["step"] - 1
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
            insert_pos = li_m.end(2)
            modified_ol = modified_ol[:insert_pos] + img_html + modified_ol[insert_pos:]

            # Re-find li_matches since string was modified
            li_matches = list(li_pattern.finditer(modified_ol))

            print(f"    Injected {file_key} into step {s['step']} of '{section_name}'")

        # Replace old ol content with modified one
        full_ol_start = match.end() + ol_match.start(1)
        full_ol_end = match.end() + ol_match.end(1)
        content = content[:full_ol_start] + modified_ol + content[full_ol_end:]

    return content


class ScreenshotPublisher:
    """Generic WebSocket-based screenshot publisher.

    Reads articles, screenshots, and manifests from the product directory,
    then uploads to WordPress via Chrome WebSocket bridge.
    """

    def __init__(self, config: dict, adapter, screenshots_dir: str, wp_posts_path: str):
        self.config = config
        self.adapter = adapter
        self.screenshots_dir = screenshots_dir
        self.wp_posts_path = wp_posts_path
        self.articles = adapter.get_articles()
        self.alt_suffix = adapter.get_alt_text_suffix()

    def _load_wp_posts(self):
        with open(self.wp_posts_path, "r", encoding="utf-8") as f:
            return {p["filename"]: p for p in json.load(f)}

    def _load_manifest(self, article_slug):
        path = os.path.join(self.screenshots_dir, article_slug, "_manifest.json")
        if not os.path.exists(path):
            return None
        with open(path) as f:
            return json.load(f)

    async def _publish_handler(self, websocket):
        """Handle Chrome client connection."""
        print("Chrome connected!")
        product_name = self.config["product"]["name"]
        await websocket.send(json.dumps({
            "type": "hello",
            "msg": f"Connected to publish server ({product_name})"
        }))

        # Get existing upload results from Chrome
        print("Requesting existing upload results from Chrome...")
        await websocket.send(json.dumps({"type": "request_uploads"}))
        response = await websocket.recv()
        upload_data = json.loads(response)
        file_to_media = upload_data.get("uploads", {})
        print(f"Chrome has {len(file_to_media)} existing media mappings")

        wp_posts = self._load_wp_posts()

        # ─── Phase 1: Upload new screenshots ───
        print("\n" + "=" * 60)
        print("PHASE 1: Upload new screenshots")
        print("=" * 60)

        all_uploads = []
        seen = set(file_to_media.keys())

        for article_info in self.articles:
            article_slug = article_info["slug"]
            manifest = self._load_manifest(article_slug)
            if not manifest:
                print(f"  No manifest for {article_slug}, skipping")
                continue

            for s in manifest.get("screenshots", []):
                if s["file"] in seen:
                    continue
                seen.add(s["file"])
                fpath = os.path.join(self.screenshots_dir, article_slug, s["file"])
                if not os.path.exists(fpath):
                    print(f"  File not found: {fpath}")
                    continue
                all_uploads.append({
                    "file": s["file"],
                    "path": fpath,
                    "article": article_slug,
                    "alt": f"{s['section']} - {s['target']} {self.alt_suffix}",
                })

        print(f"\nNeed to upload {len(all_uploads)} new images "
              f"(skipping {len(file_to_media)} already uploaded)")

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

        for article_info in self.articles:
            article_slug = article_info["slug"]
            filename = article_slug + ".md"
            if filename not in wp_posts:
                print(f"\n  Skipping {article_slug}: not in wp_posts.json")
                continue

            manifest = self._load_manifest(article_slug)
            if not manifest:
                print(f"\n  Skipping {article_slug}: no manifest")
                continue

            all_screenshots = manifest.get("screenshots", [])
            if not all_screenshots:
                print(f"\n  Skipping {article_slug}: no screenshots")
                continue

            # Group by section with step numbers
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

            # Inject images per-step
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
        print(f"\u2705 All {self.config['product']['name']} articles published!")
        print("=" * 60)

    def run(self):
        """Start the WebSocket server."""
        print(f"Starting publish server on ws://localhost:{PORT}")
        print(f"Product: {self.config['product']['name']}")
        print(f"Articles: {len(self.articles)}")
        print(f"Waiting for Chrome to connect...\n")

        async def _main():
            async with websockets.serve(
                self._publish_handler,
                "localhost",
                PORT,
                max_size=50 * 1024 * 1024,  # 50MB max message size
            ):
                await asyncio.Future()

        asyncio.run(_main())
