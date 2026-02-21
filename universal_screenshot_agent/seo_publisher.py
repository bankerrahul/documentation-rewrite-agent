#!/usr/bin/env python3
"""
SEO metadata publisher for the Universal Screenshot Agent.

Publishes SEO metadata (title, description, keyphrases) to WordPress posts
via the AIOSEO REST API addon, using the same WebSocket bridge pattern as
the screenshot publisher.

Reads seo_meta.json from the product directory and pushes each article's
SEO data to the corresponding WordPress post.

Usage:
    1. Run via CLI: python -m universal_screenshot_agent.run -p my_product publish-seo
    2. Inject the WebSocket client JS into Chrome (on the production site's wp-admin)
    3. SEO metadata is pushed automatically via AIOSEO REST API fields
"""

import asyncio
import json
import os
import sys

import websockets


PORT = 9876


class SeoPublisher:
    """WebSocket-based SEO metadata publisher.

    Reads seo_meta.json and sends AIOSEO update commands to Chrome,
    which uses the WP REST API to update post SEO fields.
    """

    def __init__(self, config: dict, adapter, seo_meta_path: str):
        self.config = config
        self.adapter = adapter
        self.seo_meta_path = seo_meta_path
        self.post_type = adapter.get_post_type()
        self.seo_config = config.get("seo", {})

    def _load_seo_meta(self):
        """Load seo_meta.json and return list of entries."""
        with open(self.seo_meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _build_aioseo_payload(self, entry: dict) -> dict:
        """Build the aioseo_meta_data payload for a single article.

        Constructs the nested structure that AIOSEO REST API expects.
        """
        brand_suffix = self.seo_config.get("brand_suffix", "")
        seo_title = entry["seo_title"]
        if brand_suffix and not seo_title.endswith(brand_suffix):
            seo_title = seo_title + brand_suffix

        payload = {
            "title": seo_title,
            "description": entry["meta_description"],
        }

        # Build keyphrases structure
        focus_kp = entry.get("focus_keyphrase", "")
        additional_kps = entry.get("additional_keyphrases", [])

        if focus_kp:
            keyphrases = {
                "focus": {
                    "keyphrase": focus_kp,
                    "score": 0,
                },
            }
            if additional_kps:
                keyphrases["additional"] = [
                    {"keyphrase": kp, "score": 0}
                    for kp in additional_kps
                ]
            payload["keyphrases"] = keyphrases

        return payload

    async def _publish_handler(self, websocket):
        """Handle Chrome client connection for SEO publishing."""
        print("Chrome connected!", flush=True)
        product_name = self.config["product"]["name"]
        await websocket.send(json.dumps({
            "type": "hello",
            "msg": f"Connected to SEO publish server ({product_name})"
        }))

        seo_entries = self._load_seo_meta()
        print(f"\nLoaded {len(seo_entries)} SEO entries from {self.seo_meta_path}", flush=True)

        # Filter to entries that have a post_id
        actionable = [e for e in seo_entries if e.get("post_id")]
        if not actionable:
            print("ERROR: No entries have a post_id. Cannot update SEO.", flush=True)
            await websocket.send(json.dumps({"type": "done"}))
            return

        print(f"\n{'=' * 60}", flush=True)
        print("Updating SEO metadata via AIOSEO REST API", flush=True)
        print(f"{'=' * 60}\n", flush=True)

        success_count = 0
        fail_count = 0

        for i, entry in enumerate(actionable):
            post_id = entry["post_id"]
            filename = entry.get("filename", "unknown")
            seo_title = entry.get("seo_title", "")

            print(f"  [{i+1}/{len(actionable)}] {filename} (post {post_id})", flush=True)
            print(f"    Title: {seo_title}", flush=True)
            print(f"    Desc: {entry.get('meta_description', '')[:60]}...", flush=True)
            print(f"    Focus: {entry.get('focus_keyphrase', '')}", flush=True)

            aioseo_data = self._build_aioseo_payload(entry)

            await websocket.send(json.dumps({
                "type": "update_seo",
                "post_id": post_id,
                "post_type": self.post_type,
                "aioseo_meta_data": aioseo_data,
            }))

            response = await websocket.recv()
            result = json.loads(response)

            if result.get("status") == "ok":
                print(f"    -> OK", flush=True)
                success_count += 1
            else:
                error = result.get("error", "unknown")
                print(f"    -> ERROR: {error}", flush=True)
                fail_count += 1

        await websocket.send(json.dumps({"type": "done"}))
        print(f"\n{'=' * 60}", flush=True)
        print(f"SEO update complete: {success_count} OK, {fail_count} failed", flush=True)
        print(f"{'=' * 60}", flush=True)

    def run(self):
        """Start the WebSocket server."""
        print(f"Starting SEO publish server on ws://localhost:{PORT}", flush=True)
        print(f"Product: {self.config['product']['name']}", flush=True)
        print(f"Post type: {self.post_type}", flush=True)
        print(f"SEO meta: {self.seo_meta_path}", flush=True)
        print(f"Waiting for Chrome to connect...\n", flush=True)

        async def _main():
            async with websockets.serve(
                self._publish_handler,
                "localhost",
                PORT,
                max_size=10 * 1024 * 1024,
            ):
                await asyncio.Future()

        asyncio.run(_main())


def get_chrome_client_js(post_type: str = "ht-kb") -> str:
    """Return the JavaScript code to inject into Chrome for SEO publishing.

    This handles the WebSocket client side: connects to the Python server,
    receives update_seo commands, and uses fetch() to PUT aioseo_meta_data
    to the WP REST API.
    """
    return f"""
(async () => {{
    const ws = new WebSocket('ws://localhost:{PORT}');
    const postType = '{post_type}';

    // Store upload results for resume capability
    if (!window._seoResults) window._seoResults = {{}};

    ws.onopen = () => console.log('[SEO] Connected to server');

    ws.onmessage = async (event) => {{
        const msg = JSON.parse(event.data);

        if (msg.type === 'hello') {{
            console.log('[SEO]', msg.msg);
        }}

        else if (msg.type === 'update_seo') {{
            const {{ post_id, post_type: pt, aioseo_meta_data }} = msg;
            const endpoint = `/wp-json/wp/v2/${{pt || postType}}/${{post_id}}`;

            try {{
                const resp = await fetch(endpoint, {{
                    method: 'PUT',
                    headers: {{
                        'X-WP-Nonce': wpApiSettings.nonce,
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{ aioseo_meta_data }}),
                }});

                if (!resp.ok) {{
                    const text = await resp.text();
                    throw new Error(`HTTP ${{resp.status}}: ${{text.slice(0, 200)}}`);
                }}

                const data = await resp.json();
                window._seoResults[post_id] = {{ status: 'ok', id: data.id }};
                ws.send(JSON.stringify({{ status: 'ok', post_id: data.id }}));
                console.log(`[SEO] Updated post ${{post_id}}`);
            }} catch (err) {{
                window._seoResults[post_id] = {{ status: 'error', error: err.message }};
                ws.send(JSON.stringify({{ status: 'error', error: err.message }}));
                console.error(`[SEO] Failed post ${{post_id}}:`, err.message);
            }}
        }}

        else if (msg.type === 'done') {{
            console.log('[SEO] All done!');
        }}
    }};

    ws.onerror = (err) => console.error('[SEO] WebSocket error:', err);
    ws.onclose = () => console.log('[SEO] Disconnected');
}})();
"""
