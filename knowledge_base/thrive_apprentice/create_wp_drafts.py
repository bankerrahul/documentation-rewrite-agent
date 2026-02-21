#!/usr/bin/env python3
"""
Create WordPress draft posts via REST API from wp_posts.json.
Uses the browser's authenticated session by generating a JS blob
that can be loaded into the browser.
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load posts
with open(os.path.join(BASE_DIR, 'wp_posts.json')) as f:
    posts = json.load(f)

# Already created post filenames (from previous session)
already_created = {
    '1-01-creating-your-first-course.md',      # ID 114142892
    '9-01-translating-your-school.md',          # ID 114142879
    '10-01-sendowl-setup-legacy.md',            # ID 114142883
    '10-02-sendowl-operations-legacy.md',       # ID 114142885
}

# Filter to only posts that haven't been created yet
remaining = [p for p in posts if p['filename'] not in already_created]
print(f"Total posts: {len(posts)}")
print(f"Already created: {len(already_created)}")
print(f"Remaining to create: {len(remaining)}")

# Generate a single JS file that, when evaluated in the browser,
# creates all remaining posts via the REST API
js_posts = []
for p in remaining:
    js_posts.append({
        't': p['title'],
        'c': p['content'],
        'cats': p['categories']
    })

# Write the data as a JS file that self-executes
js_code = f"""
// Auto-generated WordPress draft creation script
// {len(js_posts)} posts to create
(async function() {{
  const posts = {json.dumps(js_posts, ensure_ascii=False)};

  const nonce = wpApiSettings.nonce;
  const results = [];
  const statusEl = document.createElement('div');
  statusEl.style.cssText = 'position:fixed;top:10px;right:10px;background:#000;color:#0f0;padding:20px;z-index:999999;font-family:monospace;font-size:14px;max-height:80vh;overflow-y:auto;border-radius:8px;min-width:400px;';
  document.body.appendChild(statusEl);

  function updateStatus(msg) {{
    statusEl.innerHTML = msg;
  }}

  for (let i = 0; i < posts.length; i++) {{
    const post = posts[i];
    updateStatus('Creating post ' + (i+1) + '/' + posts.length + ':<br>' + post.t.substring(0, 50) + '...');

    try {{
      const resp = await fetch('/wp-json/wp/v2/ht-kb', {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
          'X-WP-Nonce': nonce
        }},
        body: JSON.stringify({{
          title: post.t,
          content: post.c,
          status: 'draft',
          'ht-kb-category': post.cats
        }})
      }});

      if (!resp.ok) {{
        const errText = await resp.text();
        results.push({{ title: post.t, error: resp.status + ': ' + errText.substring(0, 100) }});
        updateStatus('ERROR on post ' + (i+1) + ': ' + resp.status);
      }} else {{
        const data = await resp.json();
        results.push({{ title: post.t, id: data.id, status: data.status }});
      }}
    }} catch (e) {{
      results.push({{ title: post.t, error: e.message }});
    }}

    // Delay between requests to avoid rate limiting
    if (i < posts.length - 1) {{
      await new Promise(r => setTimeout(r, 500));
    }}
  }}

  // Show final results
  const success = results.filter(r => r.id);
  const failed = results.filter(r => r.error);

  let html = '<h3>DONE!</h3>';
  html += '<p>Success: ' + success.length + ' / Failed: ' + failed.length + '</p>';
  if (failed.length > 0) {{
    html += '<h4>Failed:</h4>';
    failed.forEach(f => {{
      html += '<div style="color:red">' + f.title + ': ' + f.error + '</div>';
    }});
  }}
  html += '<h4>Created IDs:</h4>';
  success.forEach(s => {{
    html += '<div>' + s.id + ': ' + s.title.substring(0, 50) + '</div>';
  }});

  updateStatus(html);

  // Store results globally
  window.__wpCreateResults = results;

  return results;
}})();
"""

# Write the JS file
output_path = os.path.join(BASE_DIR, 'create_all_drafts.js')
with open(output_path, 'w') as f:
    f.write(js_code)

print(f"\nGenerated: {output_path}")
print(f"JS file size: {os.path.getsize(output_path):,} bytes")
print(f"\nTo use: Copy the contents of create_all_drafts.js and paste into the browser's developer console on any thrivethemes.com/wp-admin page.")
