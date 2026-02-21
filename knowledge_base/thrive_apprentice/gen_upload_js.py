#!/usr/bin/env python3
"""
Generate individual JS upload commands as separate files.
Each file uploads one image to the WP media library.
"""
import base64
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
OUTPUT_DIR = os.path.join(BASE_DIR, "upload_commands")
os.makedirs(OUTPUT_DIR, exist_ok=True)

articles = ["1-01-creating-your-first-course", "2-01-settings-guide"]

all_uploads = []
seen = set()

for article in articles:
    manifest_path = os.path.join(SCREENSHOTS_DIR, article, "_manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)

    for s in manifest["screenshots"]:
        if not s.get("found"):
            continue
        if s["file"] in seen:
            continue
        seen.add(s["file"])

        fpath = os.path.join(SCREENSHOTS_DIR, article, s["file"])
        if not os.path.exists(fpath):
            continue

        alt = f"{s['section']} - {s['target']} in Thrive Apprentice"
        all_uploads.append({
            "file": s["file"],
            "path": fpath,
            "alt": alt,
        })

print(f"Total uploads: {len(all_uploads)}")

# Generate JS for each upload
manifest_entries = []
for i, u in enumerate(all_uploads):
    with open(u["path"], "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    alt_escaped = u["alt"].replace("'", "\\'")
    filename = u["file"]

    js = (
        f"(async () => {{\n"
        f"  const b64 = '{b64}';\n"
        f"  const nonce = wpApiSettings.nonce;\n"
        f"  const bs = atob(b64);\n"
        f"  const ab = new ArrayBuffer(bs.length);\n"
        f"  const ia = new Uint8Array(ab);\n"
        f"  for (let i = 0; i < bs.length; i++) ia[i] = bs.charCodeAt(i);\n"
        f"  const file = new File([ab], '{filename}', {{ type: 'image/png' }});\n"
        f"  const fd = new FormData();\n"
        f"  fd.append('file', file);\n"
        f"  const resp = await fetch('/wp-json/wp/v2/media', {{ method: 'POST', headers: {{ 'X-WP-Nonce': nonce }}, body: fd }});\n"
        f"  if (!resp.ok) return 'ERR:' + resp.status + ':' + (await resp.text()).substring(0,100);\n"
        f"  const m = await resp.json();\n"
        f"  await fetch('/wp-json/wp/v2/media/' + m.id, {{ method: 'POST', headers: {{ 'Content-Type': 'application/json', 'X-WP-Nonce': nonce }}, body: JSON.stringify({{ alt_text: '{alt_escaped}' }}) }});\n"
        f"  if (!window.__ur) window.__ur = {{}};\n"
        f"  window.__ur['{filename}'] = {{ id: m.id, url: m.source_url, alt: '{alt_escaped}' }};\n"
        f"  return 'OK:' + m.id + ':' + m.source_url;\n"
        f"}})();\n"
    )

    out_path = os.path.join(OUTPUT_DIR, f"upload_{i:02d}_{filename.replace('.png', '.js')}")
    with open(out_path, "w") as f:
        f.write(js)

    manifest_entries.append({
        "index": i,
        "filename": filename,
        "js_file": out_path,
        "js_size": len(js),
        "alt": u["alt"],
    })
    print(f"  [{i+1}/{len(all_uploads)}] {filename}: {len(js)//1024}KB")

# Save manifest
manifest_path = os.path.join(OUTPUT_DIR, "_manifest.json")
with open(manifest_path, "w") as f:
    json.dump(manifest_entries, f, indent=2)

print(f"\nGenerated {len(manifest_entries)} JS files in {OUTPUT_DIR}")
print(f"Manifest: {manifest_path}")
