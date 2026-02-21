#!/usr/bin/env python3
"""
Run the screenshot publish process by injecting JS into Chrome via clipboard.

This script:
1. Generates the full publish_screenshots.js with embedded base64 images
2. Copies it to the macOS clipboard
3. Tells the user to paste it into Chrome DevTools console

Usage:
    python3 run_chrome_publish.py
"""
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Step 1: Generate the JS file
print("Step 1: Generating publish_screenshots.js...")
result = subprocess.run(
    [sys.executable, os.path.join(BASE_DIR, "gen_chrome_publish.py")],
    capture_output=True, text=True, cwd=BASE_DIR,
)
print(result.stdout)
if result.returncode != 0:
    print("ERROR:", result.stderr)
    sys.exit(1)

js_path = os.path.join(BASE_DIR, "publish_screenshots.js")
js_size = os.path.getsize(js_path) / 1024

print(f"\nStep 2: JS file ready at: {js_path}")
print(f"Size: {js_size:.0f} KB")

# Step 3: Copy to clipboard (macOS)
try:
    with open(js_path, 'r') as f:
        js_content = f.read()
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(js_content.encode())
    print("\nStep 3: ✅ Copied to clipboard!")
    print(f"\nNow go to Chrome, open DevTools console on thrivethemes.com/wp-admin,")
    print(f"and paste with Cmd+V then press Enter.")
    print(f"\nThe script will show a green status overlay as it:")
    print(f"  1. Uploads all screenshots to the media library")
    print(f"  2. Injects image blocks into the original content")
    print(f"  3. Updates the draft posts")
except Exception as e:
    print(f"\nCouldn't copy to clipboard: {e}")
    print(f"Manually copy the contents of: {js_path}")
