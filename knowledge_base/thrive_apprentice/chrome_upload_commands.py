#!/usr/bin/env python3
"""
Generate individual JS commands for uploading screenshots via Chrome.
Each command uploads one image and returns its media ID.

Output: A JSON file with JS commands to execute sequentially.
"""
import base64
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
WP_POSTS_JSON = os.path.join(BASE_DIR, "wp_posts.json")


def load_wp_posts():
    with open(WP_POSTS_JSON, "r", encoding="utf-8") as f:
        return {p["filename"]: p for p in json.load(f)}


def load_manifest(article_slug):
    path = os.path.join(SCREENSHOTS_DIR, article_slug, "_manifest.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def main():
    articles = ["1-01-creating-your-first-course", "2-01-settings-guide"]
    wp_posts = load_wp_posts()

    all_commands = []

    # Phase 1: Generate upload commands for each unique image
    seen_files = set()
    upload_list = []

    for article_slug in articles:
        manifest = load_manifest(article_slug)
        if not manifest:
            continue

        annotated = [s for s in manifest["screenshots"] if s.get("found")]
        for s in annotated:
            key = f"{article_slug}/{s['file']}"
            if key in seen_files:
                continue
            seen_files.add(key)

            fpath = os.path.join(SCREENSHOTS_DIR, article_slug, s["file"])
            if not os.path.exists(fpath):
                continue

            with open(fpath, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")

            alt = f"{s['section']} - {s['target']} in Thrive Apprentice"
            upload_list.append({
                "filename": s["file"],
                "b64": b64,
                "alt": alt,
                "b64_len": len(b64),
            })

    print(f"Total images to upload: {len(upload_list)}")
    total_b64 = sum(u["b64_len"] for u in upload_list)
    print(f"Total base64 data: {total_b64 // 1024}KB")

    # Generate JS for each upload
    for i, u in enumerate(upload_list):
        js = (
            f"(async () => {{\n"
            f"  const b64 = '{u['b64']}';\n"
            f"  const filename = '{u['filename']}';\n"
            f"  const alt = {json.dumps(u['alt'])};\n"
            f"  const result = await window.__uploadImage(b64, filename, alt);\n"
            f"  return JSON.stringify(result);\n"
            f"}})();\n"
        )
        all_commands.append({
            "type": "upload",
            "index": i,
            "filename": u["filename"],
            "js": js,
            "js_size": len(js),
        })
        print(f"  [{i+1}/{len(upload_list)}] {u['filename']}: {len(js)//1024}KB JS")

    # Phase 2: Generate content update commands
    for article_slug in articles:
        filename = article_slug + ".md"
        if filename not in wp_posts:
            continue

        manifest = load_manifest(article_slug)
        annotated = [s for s in manifest["screenshots"] if s.get("found")]

        # Group by section
        section_groups = {}
        for s in annotated:
            sec = s["section"]
            if sec not in section_groups:
                section_groups[sec] = []
            section_groups[sec].append({"file": s["file"], "section": s["section"], "target": s["target"]})

        original = wp_posts[filename]
        content_escaped = json.dumps(original["content"])
        section_groups_json = json.dumps(section_groups)

        js = f"""(async () => {{
  const nonce = wpApiSettings.nonce;
  const title = {json.dumps(original['title'])};
  const originalContent = {content_escaped};
  const sectionGroups = {section_groups_json};
  const fileToMedia = window.__uploadResults;

  // Inject images into content
  function injectImages(content, groups, media) {{
    for (const [sectionName, screenshots] of Object.entries(groups)) {{
      const blocks = [];
      for (const s of screenshots) {{
        if (media[s.file]) {{
          const m = media[s.file];
          blocks.push(
            '<!-- wp:image {{"id":' + m.id + ',"sizeSlug":"large"}} -->\\n' +
            '<figure class="wp-block-image size-large">' +
            '<img src="' + m.url + '" alt="' + m.alt + '" class="wp-image-' + m.id + '"/>' +
            '</figure>\\n' +
            '<!-- /wp:image -->'
          );
        }}
      }}
      if (blocks.length === 0) continue;
      const imagesHtml = blocks.join('\\n\\n');
      const escaped = sectionName.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
      let regex = new RegExp('<h[23]>' + escaped + '</h[23]>', 'i');
      let match = content.match(regex);
      if (!match) {{
        const words = sectionName.split(/\\s+/);
        if (words.length >= 2) {{
          const first = words[0].replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
          const last = words[words.length-1].replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
          regex = new RegExp('<h[23]>[^<]*' + first + '[^<]*' + last + '[^<]*</h[23]>', 'i');
          match = content.match(regex);
        }}
      }}
      if (!match) {{ console.warn('Heading not found: ' + sectionName); continue; }}
      const afterHeading = content.substring(match.index + match[0].length);
      const listClose = afterHeading.indexOf('<!-- /wp:list -->');
      if (listClose === -1) {{ console.warn('No list after: ' + sectionName); continue; }}
      const insertPos = match.index + match[0].length + listClose + '<!-- /wp:list -->'.length;
      content = content.substring(0, insertPos) + '\\n\\n' + imagesHtml + content.substring(insertPos);
    }}
    return content;
  }}

  const newContent = injectImages(originalContent, sectionGroups, fileToMedia);
  const added = newContent.length - originalContent.length;
  console.log('Content: ' + originalContent.length + ' -> ' + newContent.length + ' (+' + added + ')');

  // Find the draft post
  let postId = null;
  for (const status of ['draft', 'publish', 'any']) {{
    const resp = await fetch('/wp-json/wp/v2/ht-kb?search=' + encodeURIComponent(title) + '&status=' + status + '&per_page=10', {{
      headers: {{ 'X-WP-Nonce': nonce }}
    }});
    if (resp.ok) {{
      const posts = await resp.json();
      for (const p of posts) {{
        if (p.title.rendered.trim() === title.trim()) {{
          postId = p.id;
          break;
        }}
      }}
    }}
    if (postId) break;
  }}

  if (!postId) return 'Draft not found for: ' + title;

  // Update the post
  const resp = await fetch('/wp-json/wp/v2/ht-kb/' + postId, {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json', 'X-WP-Nonce': nonce }},
    body: JSON.stringify({{ content: newContent }})
  }});

  if (!resp.ok) {{
    const err = await resp.text();
    return 'ERROR updating ' + postId + ': ' + resp.status + ' ' + err.substring(0, 200);
  }}

  return 'SUCCESS: Updated post ' + postId + ' (' + title.substring(0, 50) + '...) +' + added + ' chars from images';
}})();"""

        all_commands.append({
            "type": "update",
            "article": filename,
            "title": original["title"],
            "js": js,
            "js_size": len(js),
        })
        print(f"  Update command for {filename}: {len(js)//1024}KB JS")

    # Save commands
    output_path = os.path.join(BASE_DIR, "chrome_commands.json")
    with open(output_path, "w") as f:
        json.dump(all_commands, f)

    print(f"\nSaved {len(all_commands)} commands to {output_path}")


if __name__ == "__main__":
    main()
