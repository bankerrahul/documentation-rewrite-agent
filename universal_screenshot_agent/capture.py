"""
Generic screenshot capture engine for the Universal Screenshot Agent.

Uses Playwright to automate the browser and PIL to annotate screenshots.
All product-specific logic is delegated to the ProductAdapter:
  - Navigation: adapter.navigate_to_app(), adapter.navigate_to_section()
  - Tab switching: adapter.ensure_correct_tab()
  - Element finding: adapter.get_element_strategies()
  - Modal handling: adapter.is_modal_open(), adapter.dismiss_modal(), adapter.advance_modal()
  - Post-action hooks: adapter.post_action_hook()
  - Sample text: adapter.get_sample_text()
"""

import io
import json
import os
import re
from typing import Dict, List, Optional

from dotenv import load_dotenv
from PIL import Image
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from .annotate import annotate_screenshot
from .element_finder import find_element, scroll_to_element

# DPI for retina output (144 = 72 * 2x scale factor)
RETINA_DPI = (144, 144)


def take_annotated_screenshot(
    page: Page,
    element_box: Optional[Dict],
    adapter=None,
    scale_factor: int = 2,
    position: Optional[str] = None,
    highlight: bool = False,
) -> Image.Image:
    """Take a viewport screenshot and annotate it with an arrow.

    Args:
        page: Playwright page.
        element_box: Bounding box dict from Playwright (x, y, width, height).
                     If None, returns unannotated screenshot.
        adapter: ProductAdapter for layout config.
        scale_factor: DPI scale factor.
        position: Arrow position override ('left', 'right', 'top', 'bottom').
        highlight: Also draw a green highlight box around the element.

    Returns:
        PIL Image (annotated).
    """
    # Get scroll offset
    scroll = page.evaluate("() => ({ x: window.scrollX, y: window.scrollY })")
    scroll_offset = (scroll["x"], scroll["y"])

    # Take viewport screenshot
    screenshot_bytes = page.screenshot()
    image = Image.open(io.BytesIO(screenshot_bytes))

    if element_box:
        layout_config = adapter.get_layout_config() if adapter else None
        annotate_screenshot(
            image,
            element_box,
            scroll_offset=scroll_offset,
            scale_factor=scale_factor,
            position=position,
            highlight=highlight,
            layout_config=layout_config,
        )

    return image


def execute_step_action(page: Page, step: Dict, locator, adapter=None) -> None:
    """Execute the step's action (click, hover, type, etc.) to advance the UI state.

    After executing the action, calls adapter.post_action_hook() for product-specific
    post-action logic (e.g., saving in modals, entering courses).
    """
    action = step.get("action", "locate")
    context = step.get("context", "").lower()

    if locator is None:
        return

    try:
        if action == "click" or action == "toggle":
            locator.click(timeout=5000)
            page.wait_for_timeout(1500)
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass

        elif action == "hover":
            locator.hover(timeout=5000)
            page.wait_for_timeout(800)

        elif action == "type":
            try:
                locator.click(timeout=3000)
                page.wait_for_timeout(300)
                # Get sample text from adapter or extract from step
                sample_text = _get_sample_text(step, adapter)
                locator.fill(sample_text)
                page.wait_for_timeout(500)
                print(f"      [Typed: '{sample_text[:40]}']")
            except Exception as type_err:
                print(f"      [Type failed: {str(type_err)[:80]}]")

        elif action == "navigate":
            locator.click(timeout=5000)
            page.wait_for_timeout(1500)
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass

        elif action == "scroll":
            scroll_to_element(page, locator)

        elif action == "locate":
            # For locate — do nothing by default (just screenshot)
            pass

        # Call product-specific post-action hook
        if adapter:
            adapter.post_action_hook(page, step, action)

    except Exception as e:
        print(f"    Warning: Could not execute action '{action}': {str(e)[:120]}")


def _get_sample_text(step: Dict, adapter=None) -> str:
    """Get sample text for type actions.

    First tries adapter (which reads from config), then falls back
    to extracting from the step's raw text.
    """
    # Try adapter first
    if adapter:
        text = adapter.get_sample_text(step)
        if text and text != "Sample text":
            return text

    # Extract from raw text
    raw = step.get("raw_text", "")
    target = step.get("target", "").lower()

    # Extract text from parenthetical hints: (e.g., "Introduction to Email Marketing")
    paren_match = re.findall(r'\(e\.g\.?,?\s*["\u201c]([^"\u201d)]+)["\u201d]', raw)
    if paren_match:
        return paren_match[0]

    # Extract quoted example text
    quoted = re.findall(r'"([^"]{3,50})"', raw) + re.findall(r'\u201c([^\u201d]{3,50})\u201d', raw)
    if quoted:
        return quoted[0]

    # Adapter fallback
    if adapter:
        return adapter.get_sample_text(step)

    return "Sample text"


def _attempt_fallback_action(page: Page, step: Dict, adapter=None) -> None:
    """Try fallback actions when the primary element wasn't found."""
    action = step.get("action", "locate")
    target = step.get("target", "")

    try:
        if action == "click":
            if target:
                broad = page.get_by_text(target, exact=False)
                if broad.count() > 0:
                    for i in range(min(broad.count(), 3)):
                        try:
                            if broad.nth(i).is_visible(timeout=500):
                                broad.nth(i).click(timeout=3000)
                                page.wait_for_timeout(1000)
                                return
                        except Exception:
                            continue

        elif action == "type":
            inputs = page.locator("input:visible, textarea:visible")
            if inputs.count() > 0:
                for i in range(min(inputs.count(), 3)):
                    try:
                        inp = inputs.nth(i)
                        if inp.is_visible(timeout=500):
                            inp.click(timeout=2000)
                            sample = _get_sample_text(step, adapter)
                            inp.fill(sample)
                            page.wait_for_timeout(500)
                            return
                    except Exception:
                        continue

        elif action == "navigate":
            if target:
                link = page.locator(f"a:has-text('{target}'):visible, button:has-text('{target}'):visible")
                if link.count() > 0:
                    link.first.click(timeout=3000)
                    page.wait_for_timeout(1500)
                    return

    except Exception:
        pass


def capture_article(
    spec: Dict,
    output_dir: str,
    page: Page,
    adapter=None,
    execute_actions: bool = True,
) -> Dict:
    """Capture screenshots for all steps in an article spec.

    Args:
        spec: Parsed article spec from step_parser.
        output_dir: Directory to save screenshots (article-specific subfolder created).
        page: Playwright page (already logged in).
        adapter: ProductAdapter for product-specific behavior.
        execute_actions: Whether to execute click/hover/etc. actions after each screenshot.

    Returns:
        Dict with capture results: {total, captured, skipped, errors, screenshots}.
    """
    filename = spec["filename"]
    slug = filename.replace(".md", "")
    article_dir = os.path.join(output_dir, slug)
    os.makedirs(article_dir, exist_ok=True)

    # Get config from adapter
    browser_config = adapter.get_browser_config() if adapter else {}
    scale_factor = browser_config.get("scale_factor", 2)
    viewport_w = browser_config.get("viewport_width", 1280)
    viewport_h = browser_config.get("viewport_height", 800)

    print(f"\n{'='*60}")
    print(f"Article: {spec['title']}")
    print(f"File: {filename}")
    print(f"Output: {article_dir}")
    print(f"{'='*60}")

    results = {
        "total": 0,
        "captured": 0,
        "skipped": 0,
        "errors": 0,
        "not_found": 0,
        "screenshots": [],
        "validation_issues": [],
    }

    prev_context = ""
    for section in spec["sections"]:
        heading = section["heading"]
        heading_slug = section["heading_slug"]
        current_context = adapter.get_section_context(heading) if adapter else "default"
        print(f"\n  Section: {heading} [context: {current_context}]")

        # Navigate to appropriate page for this section
        try:
            if adapter:
                adapter.navigate_to_section(page, heading, section.get("steps", []), prev_context)
            else:
                print(f"    [No adapter — skipping navigation]")
        except Exception as e:
            print(f"    Warning: Section navigation failed: {str(e)[:100]}")
            if adapter:
                try:
                    adapter.navigate_to_app(page)
                except Exception:
                    pass

        prev_context = current_context

        for step in section["steps"]:
            results["total"] += 1
            step_num = step["step_num"]
            target = step["target"]
            action = step["action"]
            context = step.get("context", "")

            screenshot_name = f"{heading_slug}_step{step_num}.png"
            screenshot_path = os.path.join(article_dir, screenshot_name)

            has_target = step.get("has_target", bool(target))
            target_bold = step.get("target_bold", False)
            ctx_display = context[:30] + "..." if len(context) > 30 else context
            print(f"    Step {step_num}: {action} '{target}' ({ctx_display}) [bold={target_bold}, has_target={has_target}]")

            # --- Handle non-target steps: plain screenshot of current page ---
            if not has_target:
                print(f"    -> No target element. Taking plain screenshot of current state.")
                image = take_annotated_screenshot(page, None, adapter=adapter, scale_factor=scale_factor)
                image.save(screenshot_path, dpi=RETINA_DPI)
                results["captured"] += 1
                results["screenshots"].append({
                    "file": screenshot_name,
                    "step": step_num,
                    "section": heading,
                    "target": target,
                    "found": True,
                })
                if execute_actions:
                    _attempt_fallback_action(page, step, adapter)
                continue

            # --- Pre-step: dismiss any lingering modal ---
            _target_expects_modal = _check_target_expects_modal(page, step, adapter)
            if not _target_expects_modal and adapter and adapter.is_modal_open(page):
                adapter.dismiss_modal(page)

            # --- Special handling for generic toggle targets (On/Off) ---
            effective_target = target
            if action == "toggle" and target.lower() in ("on", "off"):
                step_idx = section["steps"].index(step)
                if step_idx > 0:
                    prev_step = section["steps"][step_idx - 1]
                    prev_target = prev_step.get("target", "")
                    if prev_target and prev_target.lower() not in ("on", "off"):
                        effective_target = prev_target
                        print(f"      [Toggle: using previous step target '{effective_target}' instead of '{target}']")

            # Ensure we're on the correct tab before searching
            if adapter:
                adapter.ensure_correct_tab(page, step)

            # Find the target element (adapter provides product-specific strategies)
            locator = find_element(page, effective_target, context, action, adapter=adapter)

            if locator is None:
                print(f"    -> \u26a0 ELEMENT NOT FOUND: '{target}' — step may be incorrect or UI has changed")
                image = take_annotated_screenshot(page, None, adapter=adapter, scale_factor=scale_factor)
                image.save(screenshot_path, dpi=RETINA_DPI)
                results["captured"] += 1
                results["not_found"] += 1
                results["screenshots"].append({
                    "file": screenshot_name,
                    "step": step_num,
                    "section": heading,
                    "target": target,
                    "found": False,
                })
                results["validation_issues"].append({
                    "section": heading,
                    "step": step_num,
                    "target": target,
                    "raw_text": step.get("raw_text", ""),
                    "issue": f"UI element '{target}' not found on page — verify step is accurate",
                })
                if execute_actions:
                    _attempt_fallback_action(page, step, adapter)
                continue

            try:
                # --- Check if element is behind a modal ---
                if adapter and adapter.is_element_behind_modal(page, locator):
                    print(f"    -> Element '{target}' is behind a modal. Dismissing...")
                    adapter.dismiss_modal(page)
                    page.wait_for_timeout(500)
                    locator = find_element(page, target, context, action, adapter=adapter)
                    if locator is None:
                        print(f"    -> Element NOT FOUND after modal dismiss: '{target}'.")
                        image = take_annotated_screenshot(page, None, adapter=adapter, scale_factor=scale_factor)
                        image.save(screenshot_path, dpi=RETINA_DPI)
                        results["skipped"] += 1
                        results["screenshots"].append({
                            "file": screenshot_name,
                            "step": step_num,
                            "section": heading,
                            "target": target,
                            "found": False,
                        })
                        continue

                # Scroll element into view
                scroll_to_element(page, locator)

                # Get bounding box
                bbox = locator.bounding_box()
                if not bbox:
                    print(f"    -> No bounding box for '{target}'. Unannotated screenshot.")
                    image = take_annotated_screenshot(page, None, adapter=adapter, scale_factor=scale_factor)
                    image.save(screenshot_path, dpi=RETINA_DPI)
                    results["skipped"] += 1
                    continue

                # Sanity check: skip annotation if element is way off-screen
                if (bbox["y"] < -100 or bbox["y"] > viewport_h + 100 or
                        bbox["x"] < -100 or bbox["x"] > viewport_w + 100):
                    print(f"    -> Element off-screen (y={bbox['y']:.0f}). Unannotated screenshot.")
                    image = take_annotated_screenshot(page, None, adapter=adapter, scale_factor=scale_factor)
                    image.save(screenshot_path, dpi=RETINA_DPI)
                    results["skipped"] += 1
                    results["screenshots"].append({
                        "file": screenshot_name,
                        "step": step_num,
                        "section": heading,
                        "target": target,
                        "found": False,
                    })
                    continue

                # Take annotated screenshot
                image = take_annotated_screenshot(page, bbox, adapter=adapter, scale_factor=scale_factor)
                image.save(screenshot_path, dpi=RETINA_DPI)
                print(f"    -> Saved: {screenshot_name}")
                results["captured"] += 1
                results["screenshots"].append({
                    "file": screenshot_name,
                    "step": step_num,
                    "section": heading,
                    "target": target,
                    "found": True,
                    "bbox": bbox,
                })

                # Execute the action to advance UI state
                if execute_actions:
                    execute_step_action(page, step, locator, adapter=adapter)

            except Exception as e:
                print(f"    -> ERROR: {str(e)[:150]}")
                try:
                    err_img = take_annotated_screenshot(page, None, adapter=adapter, scale_factor=scale_factor)
                    err_img.save(screenshot_path, dpi=RETINA_DPI)
                except Exception:
                    pass
                results["errors"] += 1

    # Save results manifest
    manifest_path = os.path.join(article_dir, "_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump({
            "filename": filename,
            "title": spec["title"],
            **results,
        }, f, indent=2, default=str)

    print(f"\n  Summary: {results['captured']} captured, {results['skipped']} skipped, "
          f"{results['not_found']} not found, {results['errors']} errors")

    # Print validation report for steps where elements weren't found
    if results["validation_issues"]:
        print(f"\n  {'='*60}")
        print(f"  \u26a0 VALIDATION REPORT — {len(results['validation_issues'])} step(s) could not find UI elements:")
        print(f"  {'='*60}")
        for issue in results["validation_issues"]:
            print(f"    Section: {issue['section']}")
            print(f"    Step {issue['step']}: \"{issue['raw_text'][:100]}\"")
            print(f"    Issue: {issue['issue']}")
            print()
        print(f"  These steps may have incorrect instructions, or the UI may have changed.")
        print(f"  Review and update the documentation if needed.")
        print(f"  {'='*60}")

    return results


def _check_target_expects_modal(page: Page, step: Dict, adapter=None) -> bool:
    """Check if the step's target is expected to be inside a modal.

    This prevents dismissing modals when the next step needs to interact
    with elements inside the modal (e.g., form fields, save buttons).
    """
    action = step.get("action", "locate")
    target = step.get("target", "").lower()
    context = step.get("context", "").lower()

    # Type actions into form fields (title, name, url)
    if action == "type" and any(kw in target for kw in ["title", "name", "url"]):
        return True

    # Save button inside a modal
    if target == "save" and any(kw in context for kw in [
        "create the lesson", "create the module", "create the chapter",
        "and click save", "click save"
    ]):
        return True

    # If modal is open and has a form step, any action likely targets the modal
    if adapter and adapter.is_modal_open(page):
        try:
            form = page.locator("form:visible, input:visible")
            if form.count() > 0:
                return True
        except Exception:
            pass

    return False


def capture_articles(
    spec_files: List[str],
    output_dir: str,
    adapter=None,
    headed: bool = False,
) -> None:
    """Capture screenshots for multiple articles.

    Args:
        spec_files: List of paths to JSON spec files.
        output_dir: Root output directory for screenshots.
        adapter: ProductAdapter instance.
        headed: Run browser in headed mode (visible).
    """
    # Load .env — check current directory first, then package root
    package_root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(package_root)
    for env_candidate in [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(package_root, ".env"),
        os.path.join(project_root, ".env"),
    ]:
        if os.path.exists(env_candidate):
            load_dotenv(env_candidate)
            break

    # Get browser config from adapter
    browser_config = adapter.get_browser_config() if adapter else {}
    viewport_w = browser_config.get("viewport_width", 1280)
    viewport_h = browser_config.get("viewport_height", 800)
    scale_factor = browser_config.get("scale_factor", 2)

    # Get auth credentials from env
    username = os.getenv("WP_USERNAME", "admin")
    password = os.getenv("WP_PASSWORD", "password")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context(
            viewport={"width": viewport_w, "height": viewport_h},
            device_scale_factor=scale_factor,
        )
        page = context.new_page()

        try:
            # Login
            if adapter:
                adapter.login(page, username, password)
            else:
                # Basic WP login fallback
                base_url = os.getenv("WP_URL", "http://localhost")
                page.goto(f"{base_url}/wp-login.php")
                page.fill("#user_login", username)
                page.fill("#user_pass", password)
                page.click("#wp-submit")
                page.wait_for_load_state("networkidle")

            all_results = []
            for spec_file in spec_files:
                with open(spec_file, "r") as f:
                    spec = json.load(f)

                result = capture_article(spec, output_dir, page, adapter=adapter)
                all_results.append((spec.get("filename", spec_file), result))

            # Print combined validation report
            all_issues = []
            for filename, result in all_results:
                for issue in result.get("validation_issues", []):
                    all_issues.append({**issue, "article": filename})

            # Save combined validation report
            report_path = os.path.join(output_dir, "_validation_report.json")
            report = {
                "total_articles": len(all_results),
                "total_steps": sum(r.get("total", 0) for _, r in all_results),
                "total_captured": sum(r.get("captured", 0) for _, r in all_results),
                "total_not_found": sum(r.get("not_found", 0) for _, r in all_results),
                "total_errors": sum(r.get("errors", 0) for _, r in all_results),
                "issues": all_issues,
            }
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2, default=str)

            if all_issues:
                print(f"\n{'='*70}")
                print(f"  COMBINED VALIDATION REPORT — {len(all_issues)} issue(s) across all articles")
                print(f"{'='*70}")
                for issue in all_issues:
                    print(f"  [{issue['article']}] Section: {issue['section']}, Step {issue['step']}")
                    print(f"    \"{issue['raw_text'][:100]}\"")
                    print(f"    \u2192 {issue['issue']}")
                    print()
                print(f"  Full report saved to: {report_path}")
                print(f"{'='*70}")
            else:
                print(f"\n  \u2713 All steps validated — every UI element was found on the page.")

        finally:
            browser.close()
