import json
import os
import argparse
import math
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page, Browser, Locator
from PIL import Image, ImageDraw

# Load environment variables
load_dotenv()

WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

def login(page: Page):
    """Logs into the WordPress admin dashboard."""
    print(f"Logging into {WP_URL}...")
    if not WP_URL or not WP_USERNAME or not WP_PASSWORD:
        raise ValueError("Missing WP_URL, WP_USERNAME, or WP_PASSWORD in environment variables.")

    login_url = f"{WP_URL.rstrip('/')}/wp-login.php"
    page.goto(login_url)
    
    # Handle Pantheon Sandbox Notice
    try:
        # Check for title or specific button
        if "Sandbox Environment Notice" in page.title() or page.locator(".pds-button").count() > 0:
            print("Detected Pantheon Sandbox Notice. Clicking Continue...")
            page.click(".pds-button")
            page.wait_for_load_state('networkidle')
    except Exception as e:
        print(f"Error handling sandbox notice (ignoring): {e}")

    page.fill('#user_login', WP_USERNAME)
    page.fill('#user_pass', WP_PASSWORD)
    page.click('#wp-submit')
    
    # Wait for dashboard to load
    page.wait_for_load_state('networkidle')
    
    # Check if login was successful
    if "wp-admin" not in page.url and "admin.php" not in page.url:
        print(f"Warning: Login might have failed. Current URL: {page.url}")
    else:
        print("Login successful.")

def draw_arrow(image: Image.Image, start: Tuple[int, int], end: Tuple[int, int], color: str = "red", width: int = 5):
    """Draws an arrow on the image."""
    draw = ImageDraw.Draw(image)
    
    # Draw the line
    draw.line([start, end], fill=color, width=width)
    
    # Draw the arrowhead at the end
    # Calculate angle
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)
    
    arrow_len = width * 4
    arrow_angle = math.pi / 6
    
    # Calculate points for arrowhead
    x1 = end[0] - arrow_len * math.cos(angle - arrow_angle)
    y1 = end[1] - arrow_len * math.sin(angle - arrow_angle)
    x2 = end[0] - arrow_len * math.cos(angle + arrow_angle)
    y2 = end[1] - arrow_len * math.sin(angle + arrow_angle)
    
    draw.polygon([end, (x1, y1), (x2, y2)], fill=color)

def process_screenshot_task(page: Page, task: Dict[str, Any], output_dir: str):
    """Navigates and captures a single screenshot with optional annotations."""
    print(f"Processing task: {task.get('id', 'unknown')}")
    
    target_url = task.get('url')
    if not target_url.startswith('http'):
        target_url = f"{WP_URL.rstrip('/')}/{target_url.lstrip('/')}"
        
    print(f"Navigating to {target_url}...")
    page.goto(target_url)
    page.wait_for_load_state('domcontentloaded')
    
    # Execute actions if any
    actions = task.get('actions', [])
    for action in actions:
        act_type = action.get('type')
        selector = action.get('selector')
        
        if act_type == 'click':
            print(f"Clicking {selector}...")
            page.click(selector)
            page.wait_for_load_state('networkidle') # Wait after click
        elif act_type == 'type':
            text = action.get('text', '')
            print(f"Typing '{text}' into {selector}...")
            page.fill(selector, text)
        elif act_type == 'wait':
            ms = action.get('ms', 1000)
            print(f"Waiting {ms}ms...")
            page.wait_for_timeout(ms)
            
        page.wait_for_timeout(500)

    # Resolve annotation targets before taking screenshot
    annotations = task.get('annotations', [])
    annotation_data = []
    
    for ann in annotations:
        target_selector = ann.get('selector')
        if not target_selector:
            continue
            
        # Get bounding box relative to viewport
        try:
             # Support :has-text psuedo class via playwright locator
             bbox = page.locator(target_selector).first.bounding_box()
             box = bbox
        except:
             box = None
        if box:
            annotation_data.append({
                "type": ann.get('type', 'arrow'),
                "box": box,
                "position": ann.get('position', 'left'),
                "color": ann.get('color', 'red'),
                "selector_raw": target_selector
            })
        else:
            print(f"Warning: Annotation target {target_selector} not found.")

    # Capture screenshot
    selector = task.get('selector', 'body')
    output_filename = task.get('output_file', f"{task['id']}.png")
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"Capturing selector '{selector}' to {output_path}...")
    
    # We always capture to a buffer first to post-process with PIL
    if selector == 'body':
        screenshot_bytes = page.screenshot(full_page=True)
        # For full page, coordinates are absolute
        offset_x, offset_y = 0, 0
    elif selector == 'viewport':
        # If there are annotations, try to scroll the first annotation target into view
        # to ensure it's in the 'fold'.
        if annotation_data:
             first_selector = annotation_data[0].get('selector_raw')
             if first_selector:
                  try:
                       page.locator(first_selector).scroll_into_view_if_needed()
                       # Brief wait for scroll animation
                       page.wait_for_timeout(500)
                  except:
                       pass

        screenshot_bytes = page.screenshot()
        # For viewport, coordinates from bounding_box are absolute to page.
        # We need to subtract current scroll position.
        scroll_offsets = page.evaluate("() => ({ x: window.scrollX, y: window.scrollY })")
        offset_x = scroll_offsets['x']
        offset_y = scroll_offsets['y']
        print(f"Viewport scroll offset: {offset_x}, {offset_y}")
    else:
        # Revert to standard element screenshot (Micro view)
        element_handle = page.locator(selector)
        screenshot_bytes = element_handle.screenshot()
        
        # We need the element's position to offset annotation coordinates
        elem_box = element_handle.bounding_box()
        if not elem_box:
             print(f"Could not find bounding box for capture selector {selector}")
             return
        offset_x, offset_y = elem_box['x'], elem_box['y']

    # Open image with PIL
    image = Image.open(io.BytesIO(screenshot_bytes))
    
    # Handle DPI scaling (force scale 2 for Retina)
    scale_factor = 2 
    
    for ann in annotation_data:
        box = ann['box']
        # Convert CSS coordinates to Image coordinates
        target_x = (box['x'] + box['width'] / 2 - offset_x) * scale_factor
        target_y = (box['y'] + box['height'] / 2 - offset_y) * scale_factor
        
        # Calculate start/end of arrow based on position
        # Default length doubled from 60 to 120 as per user request
        arrow_length = 120 * scale_factor 
        gap = 5 * scale_factor # gap between arrow tip and element
        
        if ann['position'] == 'left':
             # Arrow comes from left, points to left edge center
             end_point = ( (box['x'] - offset_x) * scale_factor - gap, target_y )
             start_point = ( end_point[0] - arrow_length, target_y )
        elif ann['position'] == 'right':
             # Arrow comes from right, points to right edge center
             end_point = ( (box['x'] + box['width'] - offset_x) * scale_factor + gap, target_y )
             start_point = ( end_point[0] + arrow_length, target_y )
        elif ann['position'] == 'top':
             # Located: Top of element
             end_point = ( target_x, (box['y'] - offset_y) * scale_factor - gap )
             start_point = ( target_x, end_point[1] - arrow_length )
        elif ann['position'] == 'bottom':
             # Located: Bottom of element
             end_point = ( target_x, (box['y'] + box['height'] - offset_y) * scale_factor + gap )
             start_point = ( target_x, end_point[1] + arrow_length )
        
        # Check bounds
        img_w, img_h = image.size
        if (start_point[0] < 0 or start_point[0] > img_w or 
            start_point[1] < 0 or start_point[1] > img_h):
            print(f"Warning: Annotation arrow start point {start_point} is out of bounds (Image: {img_w}x{img_h}). Try changing position.")
            
        print(f"Drawing arrow: {ann['position']} for {ann.get('selector')} at {start_point} -> {end_point}")
        draw_arrow(image, start_point, end_point, color=ann['color'], width=5 * scale_factor)

    image.save(output_path)
    print("Success.")

def main():
    parser = argparse.ArgumentParser(description="Capture screenshots for documentation.")
    parser.add_argument("config", help="Path to the JSON configuration file.")
    parser.add_argument("--output", default="screenshots", help="Directory to save screenshots.")
    args = parser.parse_args()
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
        
    with open(args.config, 'r') as f:
        tasks = json.load(f)
        
    with sync_playwright() as p:
        # Launch browser with High DPI settings
        # device_scale_factor=2 emulates Retina
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            device_scale_factor=2 
        )
        page = context.new_page()
        
        try:
            login(page)
            
            for task in tasks:
                task_id = task.get('id', 'unknown')
                try:
                    process_screenshot_task(page, task, args.output)
                except Exception as e:
                    print(f"Error processing task {task_id}: {e}")
                    # Dump HTML on individual task failure to help debug selectors
                    error_html_path = os.path.join(args.output, f"error_{task_id}.html")
                    try:
                        with open(error_html_path, "w") as f:
                            f.write(page.content())
                        print(f"  -> Saved error HTML to {error_html_path}")
                    except:
                        pass
                    # Continue to next task in batch
                    continue
                    
        except Exception as e:
            print(f"Global error: {e}")
            page.screenshot(path=os.path.join(args.output, "error.png"))
            print(f"Saved error screenshot to {os.path.join(args.output, 'error.png')}")
            print(f"Current URL: {page.url}")
            with open(os.path.join(args.output, "error.html"), "w") as f:
                f.write(page.content())
            print(f"Saved error HTML to {os.path.join(args.output, 'error.html')}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    import io # Late import for bytesio
    main()
