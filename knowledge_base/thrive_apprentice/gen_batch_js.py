#!/usr/bin/env python3
"""Generate individual JS batch files for creating WordPress drafts."""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'wp_posts.json')) as f:
    posts = json.load(f)

already_created = {
    '1-01-creating-your-first-course.md',
    '9-01-translating-your-school.md',
    '10-01-sendowl-setup-legacy.md',
    '10-02-sendowl-operations-legacy.md',
}

remaining = [p for p in posts if p['filename'] not in already_created]

# Split into batches of 4
BATCH_SIZE = 4
batches = [remaining[i:i+BATCH_SIZE] for i in range(0, len(remaining), BATCH_SIZE)]

for bi, batch in enumerate(batches):
    js_posts = [{'t': p['title'], 'c': p['content'], 'cats': p['categories']} for p in batch]

    js = f"""(async function() {{
  const posts = {json.dumps(js_posts, ensure_ascii=False)};
  const nonce = wpApiSettings.nonce;
  const results = [];
  for (let i = 0; i < posts.length; i++) {{
    const post = posts[i];
    try {{
      const resp = await fetch('/wp-json/wp/v2/ht-kb', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json', 'X-WP-Nonce': nonce }},
        body: JSON.stringify({{ title: post.t, content: post.c, status: 'draft', 'ht-kb-category': post.cats }})
      }});
      if (resp.ok) {{
        const data = await resp.json();
        results.push(data.id + ': ' + post.t.substring(0, 40));
      }} else {{
        results.push('ERR ' + resp.status + ': ' + post.t.substring(0, 40));
      }}
    }} catch(e) {{
      results.push('ERR: ' + post.t.substring(0, 40) + ' - ' + e.message);
    }}
    if (i < posts.length - 1) await new Promise(r => setTimeout(r, 500));
  }}
  window.__batch{bi:02d}Results = results;
  return results.join('\\n');
}})()"""

    outpath = os.path.join(BASE_DIR, f'js_batch_{bi:02d}.js')
    with open(outpath, 'w') as f:
        f.write(js)

    filenames = [p['filename'] for p in batch]
    size = os.path.getsize(outpath)
    print(f"Batch {bi:02d}: {len(batch)} posts, {size:>7,} bytes - {', '.join(filenames)}")

print(f"\nTotal: {len(batches)} batches, {len(remaining)} posts")
