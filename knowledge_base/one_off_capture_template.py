import os
import io
import math
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
from dotenv import load_dotenv

# This is a standalone script designed to capture ALL screenshots for a specific document
# in a single execution. Hardcode your selectors here to minimize credits.

def capture_all():
    load_dotenv()
    url = os.getenv("WP_URL")
    user = os.getenv("WP_USERNAME")
    pw = os.getenv("WP_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, device_scale_factor=2)
        page = context.new_page()

        # 1. Login
        print("Logging in...")
        page.goto(f"{url.rstrip('/')}/wp-login.php")
        try:
            if "Sandbox" in page.title(): page.click(".pds-button")
        except: pass
        page.fill('#user_login', user)
        page.fill('#user_pass', pw)
        page.click('#wp-submit')
        page.wait_for_load_state('networkidle')

        # 2. Define Tasks (Add your selectors here!)
        tasks = [
            {
                "id": "example_dashboard",
                "url": "/wp-admin/admin.php?page=tve_dash_section",
                "selector": "viewport",
                "ann": {"selector": "#toplevel_page_tve_dash_section", "pos": "right"}
            }
        ]

        for task in tasks:
            print(f"Capturing {task['id']}...")
            target = f"{url.rstrip('/')}/{task['url'].lstrip('/')}"
            page.goto(target)
            
            # Capture
            if task['selector'] == 'viewport':
                img_bytes = page.screenshot()
                offset = page.evaluate("() => ({x: window.scrollX, y: window.scrollY})")
            else:
                img_bytes = page.locator(task['selector']).screenshot()
                bbox = page.locator(task['selector']).bounding_box()
                offset = {"x": bbox['x'], "y": bbox['y']}

            # Annotate
            img = Image.open(io.BytesIO(img_bytes))
            draw = ImageDraw.Draw(img)
            
            ann = task.get('ann')
            if ann:
                target_box = page.locator(ann['selector']).bounding_box()
                # Simplified arrow logic for the standalone template
                tx = (target_box['x'] + target_box['width']/2 - offset['x']) * 2
                ty = (target_box['y'] + target_box['height']/2 - offset['y']) * 2
                draw.line([(tx+200, ty), (tx+10, ty)], fill="red", width=10)
                draw.polygon([(tx, ty), (tx+30, ty-15), (tx+30, ty+15)], fill="red")

            img.save(f"{task['id']}.png")
            print(f"Saved {task['id']}.png")

        browser.close()

if __name__ == "__main__":
    capture_all()
