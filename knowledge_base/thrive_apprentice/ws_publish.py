#!/usr/bin/env python3
"""
WebSocket-based screenshot publisher.

Starts a WebSocket server on localhost:9876. Chrome connects to it and
receives commands to upload images and update posts. This bypasses
Cloudflare/CORS issues since ws://localhost is allowed from HTTPS pages.

Usage:
    1. Run: python3 ws_publish.py
    2. The script will inject a WebSocket client into Chrome via the MCP tool
    3. Images are sent as base64 over WebSocket, uploaded via WP REST API
"""
import asyncio
import base64
import json
import os
import sys

try:
    import websockets
except ImportError:
    print("Installing websockets...")
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


async def publish_handler(websocket):
    """Handle a Chrome client connection."""
    print("Chrome connected!")

    # Send a hello to confirm connection
    await websocket.send(json.dumps({"type": "hello", "msg": "Connected to publish server"}))

    articles = ["1-01-creating-your-first-course", "2-01-settings-guide"]
    wp_posts = load_wp_posts()

    # Collect all images to upload
    all_uploads = []
    seen = set()
    for article in articles:
        manifest = load_manifest(article)
        if not manifest:
            continue
        for s in manifest["screenshots"]:
            if not s.get("found") or s["file"] in seen:
                continue
            seen.add(s["file"])
            fpath = os.path.join(SCREENSHOTS_DIR, article, s["file"])
            if not os.path.exists(fpath):
                continue
            all_uploads.append({
                "file": s["file"],
                "path": fpath,
                "alt": f"{s['section']} - {s['target']} in Thrive Apprentice",
            })

    print(f"Will upload {len(all_uploads)} images")

    # Phase 1: Upload images one by one
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

        # Wait for upload confirmation
        response = await websocket.recv()
        result = json.loads(response)
        if result.get("status") == "ok":
            print(f"    -> OK: ID={result.get('id')} {result.get('url', '')}")
        else:
            print(f"    -> ERROR: {result.get('error', 'unknown')}")

    # Phase 2: Update posts
    for article_slug in articles:
        filename = article_slug + ".md"
        if filename not in wp_posts:
            continue

        manifest = load_manifest(article_slug)
        annotated = [s for s in manifest["screenshots"] if s.get("found")]

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
        print(f"\n  Updating post: {original['title'][:50]}...")

        await websocket.send(json.dumps({
            "type": "update_post",
            "title": original["title"],
            "content": original["content"],
            "section_groups": section_groups,
        }))

        response = await websocket.recv()
        result = json.loads(response)
        if result.get("status") == "ok":
            print(f"    -> OK: Post {result.get('post_id')} updated")
        else:
            print(f"    -> ERROR: {result.get('error', 'unknown')}")

    # Done
    await websocket.send(json.dumps({"type": "done"}))
    print("\n✅ All done!")


async def main():
    print(f"Starting WebSocket server on ws://localhost:{PORT}")
    print(f"Waiting for Chrome to connect...\n")

    async with websockets.serve(publish_handler, "localhost", PORT):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
