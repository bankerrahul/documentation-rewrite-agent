"""
Screenshot capture module for Thrive Apprentice documentation.
Uses Playwright to automate the browser and PIL to annotate screenshots.
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

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

WP_URL = os.getenv("WP_URL", "http://thrive-themes.local").rstrip("/")
WP_USERNAME = os.getenv("WP_USERNAME", "rahul")
WP_PASSWORD = os.getenv("WP_PASSWORD", "baroda")

TA_URL = f"{WP_URL}/wp-admin/admin.php?page=thrive_apprentice"
SCALE_FACTOR = 2  # Retina DPI


def login(page: Page) -> None:
    """Log into WordPress."""
    print(f"  Logging into {WP_URL}...")
    page.goto(f"{WP_URL}/wp-login.php")
    page.fill("#user_login", WP_USERNAME)
    page.fill("#user_pass", WP_PASSWORD)
    page.click("#wp-submit")
    page.wait_for_load_state("networkidle")
    if "wp-admin" in page.url:
        print("  Login successful.")
    else:
        raise RuntimeError(f"Login failed. Current URL: {page.url}")


def navigate_to_ta(page: Page) -> None:
    """Navigate to Thrive Apprentice dashboard and wait for SPA to load."""
    page.goto(TA_URL)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)  # TA is a Vue SPA — needs extra time


def _click_content_tab(page: Page) -> bool:
    """Click the Content tab inside a course using exact TA selectors.

    From TA source: the Content tab's data-slug is "new" (not "content"),
    and it's always at index 1 in the tab bar (ul.tva-tabs-ul).
    """
    selectors = [
        "li[data-slug='new']",                      # Exact slug from TA source
        "ul.tva-tabs-ul > li[data-index='1']",      # Content is always tab index 1
        ".tva-tab-title:has-text('Content')",        # Fallback text match
    ]
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=2000):
                el.click()
                page.wait_for_timeout(2000)
                print(f"    [Clicked Content tab via: {sel}]")
                return True
        except Exception:
            continue
    print("    [WARNING: Could not click Content tab]")
    return False


def _ensure_correct_tab(page: Page, step: Dict) -> None:
    """Auto-switch to the Content tab when the step's target requires it.

    Many course structure elements (Add Module, Add Lesson, etc.) only exist
    on the Content tab. If we're inside a course but on the wrong tab,
    this function switches to Content before searching for elements.

    Skips tab-switching when a modal is open (e.g., Add Lesson modal showing
    the title input form — switching tabs would close the modal).
    """
    target_lower = step.get("target", "").lower()

    # Targets that only appear inside modals — never switch tabs for these
    _modal_targets = {"module title", "lesson title", "chapter title"}
    if target_lower in _modal_targets:
        return

    _content_tab_targets = {
        "add module", "add lesson", "add chapter", "add assessment",
        "edit content", "add content", "edit module details", "add course content",
    }
    if target_lower in _content_tab_targets:
        # Don't switch tabs if a modal is currently open
        modal = page.locator("#tvd-modal-base:visible, .tvd-modal:visible")
        try:
            if modal.count() > 0 and modal.first.is_visible(timeout=500):
                return  # Modal is open, don't click behind it
        except Exception:
            pass

        # Check if Content tab is already selected (data-slug="new")
        selected = page.locator("li.tva-tab-selected[data-slug='new']")
        try:
            if selected.count() > 0 and selected.first.is_visible(timeout=500):
                return  # Already on Content tab
        except Exception:
            pass
        # Check if we're inside a course at all (tab bar visible)
        tab_bar = page.locator("ul.tva-tabs-ul")
        if tab_bar.count() > 0:
            try:
                if tab_bar.first.is_visible(timeout=500):
                    print(f"      [Auto-switching to Content tab for target '{target_lower}']")
                    _click_content_tab(page)
            except Exception:
                pass


def _get_section_context(heading: str) -> str:
    """Map a section heading to a logical page context.

    Sections that share the same context don't need re-navigation.
    """
    heading_lower = heading.lower()
    if "accessing" in heading_lower:
        return "wp-dashboard"
    if any(kw in heading_lower for kw in [
        "creating your first course", "managing courses", "course list",
    ]):
        return "ta-courses-list"
    if any(kw in heading_lower for kw in [
        "adding modules", "adding chapters", "adding your first lesson",
        "lesson", "module", "chapter",
        "hierarchy", "content type", "structuring", "course structure",
        "navigation", "progress tracking",
    ]):
        return "ta-course-content"
    if any(kw in heading_lower for kw in ["publishing", "publish"]):
        return "ta-courses-list"
    if any(kw in heading_lower for kw in [
        "settings", "general settings", "email template", "login",
        "access restriction", "payment", "api key", "log", "data cleanup",
        "course page", "url slug", "auto-login", "auto login",
        "course comment", "dynamic label", "label", "translation",
        "certificate", "assessment upload",
    ]):
        return "ta-settings"
    if any(kw in heading_lower for kw in [
        "product", "bundle", "creating a course bundle", "adding courses to",
        "configuring access", "access rule", "access requirement",
    ]):
        return "ta-products"
    if any(kw in heading_lower for kw in [
        "design", "template", "dynamic text", "visual editor",
    ]):
        return "ta-design"
    if any(kw in heading_lower for kw in ["drip", "schedule"]):
        return "ta-course-drip"
    if any(kw in heading_lower for kw in [
        "profile page", "landing page", "menu link",
        "my profile", "edit profile",
    ]):
        return "wp-pages"
    if any(kw in heading_lower for kw in [
        "ai", "generating", "prompt-to-course", "remixing",
        "generate with ai", "course generation",
    ]):
        return "ta-courses-list"
    if any(kw in heading_lower for kw in [
        "login", "authentication", "registration",
    ]):
        return "ta-settings"
    if any(kw in heading_lower for kw in [
        "funnel", "opt-in", "email service", "landing",
        "free course", "lead generation",
    ]):
        return "ta-courses-list"
    return "ta-dashboard"


def navigate_to_section(page: Page, heading: str, steps: list = None, prev_context: str = "") -> None:
    """Try to navigate to the appropriate page for a given section.

    Args:
        page: Playwright page.
        heading: Section heading text.
        steps: Optional list of steps in this section.
        prev_context: The previous section's context string. If the current
                      section shares the same context, skip re-navigation
                      to preserve UI state from the previous section's actions.
    """
    heading_lower = heading.lower()
    current_context = _get_section_context(heading)

    # Skip re-navigation if we're in the same logical page context
    if prev_context and prev_context == current_context:
        print(f"    [Skipping re-navigation: same context '{current_context}']")
        return

    # For "Accessing" sections, go to WP Dashboard so we can navigate TA
    if "accessing" in heading_lower:
        page.goto(f"{WP_URL}/wp-admin/")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        return

    # Determine if we need to do a full TA reload.
    # If we're transitioning between TA contexts (e.g., courses-list → course-content),
    # the SPA is already loaded — just navigate within it.
    # Only do a full reload when coming from non-TA contexts (wp-dashboard, wp-pages).
    is_prev_ta = prev_context.startswith("ta-") if prev_context else False
    is_current_ta = current_context.startswith("ta-")

    if not is_prev_ta or not is_current_ta:
        # Coming from non-TA context or first section — do full TA load
        navigate_to_ta(page)
    else:
        print(f"    [Staying within TA SPA: {prev_context} → {current_context}]")

    # For sections about creating a course on the courses list page
    if any(kw in heading_lower for kw in [
        "creating your first course", "managing courses", "course list"
    ]):
        # Click "Courses" in TA sidebar to go to courses list
        courses = page.locator(".tva-menu .tva-menu-item:has-text('Courses')")
        if courses.count() > 0 and courses.first.is_visible():
            courses.first.click()
            page.wait_for_timeout(2000)
        return

    # For module/chapter/lesson sections, check if we're already inside a course.
    # If yes, just click Content tab. If not, go to courses list and let step 1 handle entering the course.
    if any(kw in heading_lower for kw in [
        "adding modules", "adding chapters", "adding your first lesson",
        "lesson", "module", "chapter",
    ]):
        # Check if we're already inside a course (tab bar visible)
        tab_bar = page.locator("ul.tva-tabs-ul")
        if tab_bar.count() > 0:
            try:
                if tab_bar.first.is_visible(timeout=2000):
                    _click_content_tab(page)
                    return
            except Exception:
                pass

        # Not inside a course — go to courses list.
        # Step 1 typically says "Open your course..." so it will handle entering.
        courses_sidebar = page.locator(".tva-menu .tva-menu-item:has-text('Courses')")
        if courses_sidebar.count() > 0 and courses_sidebar.first.is_visible():
            courses_sidebar.first.click()
            page.wait_for_timeout(2000)
            print("    [Navigated to Courses list — step 1 should enter the course]")
        return

    # For publishing sections, navigate to the courses list.
    # The steps will handle: 1) show Courses tab, 2) click course card, 3) click Unpublished.
    if any(kw in heading_lower for kw in ["publishing", "publish"]):
        courses_sidebar = page.locator(".tva-menu .tva-menu-item:has-text('Courses')")
        if courses_sidebar.count() > 0 and courses_sidebar.first.is_visible():
            courses_sidebar.first.click()
            page.wait_for_timeout(2000)
            print("    [Navigated to Courses list for publishing section]")
        return

    # For settings-related sections, navigate to Settings page
    if any(kw in heading_lower for kw in [
        "settings", "general settings", "email template", "login",
        "access restriction", "payment", "api key", "log", "data cleanup",
        "course page", "url slug", "auto-login", "auto login",
        "course comment", "dynamic label", "label", "translation",
        "certificate", "assessment upload",
    ]):
        _navigate_to_settings(page, heading_lower)
        return

    # For setup wizard sections, navigate to TA (wizard shows on home if active)
    if "setup wizard" in heading_lower or "wizard" in heading_lower:
        # Already at TA dashboard
        return

    # For Product / Bundle sections, navigate to Products tab
    if any(kw in heading_lower for kw in [
        "product", "bundle", "creating a course bundle", "adding courses to",
        "configuring access", "access rule", "access requirement",
    ]):
        _navigate_to_products(page)
        return

    # For Design / Template sections, navigate to Design tab
    if any(kw in heading_lower for kw in [
        "design", "template", "dynamic text", "visual editor",
    ]):
        _navigate_to_design(page)
        return

    # For Drip sections, navigate to course Drip tab
    if any(kw in heading_lower for kw in ["drip", "schedule"]):
        _navigate_to_course_drip(page)
        return

    # For WordPress Pages sections (profile pages, landing pages)
    if any(kw in heading_lower for kw in [
        "profile page", "landing page", "menu link",
        "my profile", "edit profile",
    ]):
        page.goto(f"{WP_URL}/wp-admin/edit.php?post_type=page")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        return

    # For AI / generation sections, navigate to Courses (AI starts from Add Course)
    if any(kw in heading_lower for kw in [
        "ai", "generating", "prompt-to-course", "remixing",
        "generate with ai", "course generation",
    ]):
        courses = page.locator(".tva-menu .tva-menu-item:has-text('Courses')")
        if courses.count() > 0 and courses.first.is_visible():
            courses.first.click()
            page.wait_for_timeout(2000)
        return

    # For login/authentication sections, navigate to Settings > Login
    if any(kw in heading_lower for kw in [
        "login", "authentication", "registration",
    ]):
        _navigate_to_settings(page, heading_lower)
        return

    # For import/migration sections, navigate to TA dashboard
    if any(kw in heading_lower for kw in [
        "import", "migration", "switching", "existing customer",
    ]):
        # Already at TA dashboard
        return

    # For course hierarchy / content type sections, navigate to course Content
    if any(kw in heading_lower for kw in [
        "hierarchy", "content type", "structuring", "course structure",
        "navigation", "progress tracking",
    ]):
        _navigate_to_course_content(page)
        return

    # For funnel / landing page / opt-in sections, navigate to TA dashboard
    if any(kw in heading_lower for kw in [
        "funnel", "opt-in", "email service", "landing",
        "free course", "lead generation",
    ]):
        # Start from Courses tab
        courses = page.locator(".tva-menu .tva-menu-item:has-text('Courses')")
        if courses.count() > 0 and courses.first.is_visible():
            courses.first.click()
            page.wait_for_timeout(2000)
        return


def _navigate_to_course_content(page: Page) -> None:
    """Navigate to the first course's Content tab.

    Checks if we're already inside a course before doing a full navigation.
    This preserves UI state when transitioning from course creation.
    """
    # First check: are we already inside a course? (tab bar visible)
    tab_bar = page.locator("ul.tva-tabs-ul")
    if tab_bar.count() > 0:
        try:
            if tab_bar.first.is_visible(timeout=2000):
                _click_content_tab(page)
                return
        except Exception:
            pass

    # Not inside a course — navigate to TA Courses list first
    courses = page.locator(".tva-menu .tva-menu-item:has-text('Courses')")
    if courses.count() > 0 and courses.first.is_visible():
        courses.first.click()
        page.wait_for_timeout(2000)

    # Click on the first course to enter it
    # Try multiple strategies
    entered = False

    # Strategy 1: Click on a course card
    course_selectors = [
        ".tva-course-card",
        ".tva-course-item",
        ".tva-course-card-container",
        "div[class*='course-card']",
        "div[class*='course-item']",
        ".tva-course-list .tva-course",
    ]
    for sel in course_selectors:
        try:
            card = page.locator(sel).first
            if card.is_visible(timeout=1000):
                card.click()
                page.wait_for_timeout(2000)
                entered = True
                print(f"    [Entered course via selector: {sel}]")
                break
        except Exception:
            continue

    if not entered:
        # Strategy 2: Click on a known course title
        for title in ["Introduction to Email Marketing", "My First Course"]:
            try:
                el = page.get_by_text(title, exact=False)
                if el.count() > 0 and el.first.is_visible():
                    el.first.click()
                    page.wait_for_timeout(2000)
                    entered = True
                    print(f"    [Entered course via title text: '{title}']")
                    break
            except Exception:
                continue

    if not entered:
        # Strategy 3: Click first clickable heading in main content area
        try:
            main = page.locator(".tva-content-area, .tva-courses-list, main, #wpbody-content")
            if main.count() > 0:
                link = main.first.locator("a, h3, h4, .tva-title").first
                if link.is_visible(timeout=1000):
                    link.click()
                    page.wait_for_timeout(2000)
                    entered = True
        except Exception:
            pass

    if not entered:
        print("    [WARNING: Could not enter a course — Content tab may not be available]")

    # Click Content tab using exact TA selectors
    _click_content_tab(page)


def _navigate_to_course_details(page: Page) -> None:
    """Navigate to the first course's Course details tab."""
    # Click Courses in sidebar
    courses = page.locator(".tva-menu .tva-menu-item:has-text('Courses')")
    if courses.count() > 0 and courses.first.is_visible():
        courses.first.click()
        page.wait_for_timeout(2000)

    # Click on the first course
    course_card = page.locator(".tva-course-card, .tva-course-item").first
    if course_card.is_visible():
        course_card.click()
        page.wait_for_timeout(2000)
    else:
        course_title = page.get_by_text("Introduction to Email Marketing", exact=False)
        if course_title.count() > 0 and course_title.first.is_visible():
            course_title.first.click()
            page.wait_for_timeout(2000)

    # Click Course details tab
    details_tab = page.locator(".tva-tab-title:has-text('Course details')")
    if details_tab.count() > 0 and details_tab.first.is_visible():
        details_tab.first.click()
        page.wait_for_timeout(2000)


def _navigate_to_products(page: Page) -> None:
    """Navigate to the TA Products tab."""
    products = page.locator(".tva-menu .tva-menu-item:has-text('Products')")
    if products.count() > 0 and products.first.is_visible():
        products.first.click()
        page.wait_for_timeout(3000)


def _navigate_to_design(page: Page) -> None:
    """Navigate to the TA Design tab."""
    design = page.locator(".tva-menu .tva-menu-item:has-text('Design')")
    if design.count() > 0 and design.first.is_visible():
        design.first.click()
        page.wait_for_timeout(3000)


def _navigate_to_course_drip(page: Page) -> None:
    """Navigate to the first course's Drip tab."""
    # Click Courses in sidebar
    courses = page.locator(".tva-menu .tva-menu-item:has-text('Courses')")
    if courses.count() > 0 and courses.first.is_visible():
        courses.first.click()
        page.wait_for_timeout(2000)

    # Click on the first course card
    course_card = page.locator(".tva-course-card, .tva-course-item").first
    if course_card.is_visible():
        course_card.click()
        page.wait_for_timeout(2000)

    # Click Drip tab
    drip_tab = page.locator(".tva-tab-title:has-text('Drip')")
    if drip_tab.count() > 0 and drip_tab.first.is_visible():
        drip_tab.first.click()
        page.wait_for_timeout(2000)


def _navigate_to_settings(page: Page, heading_lower: str = "") -> None:
    """Navigate to the TA Settings page and optionally click a sub-tab."""
    # Click Settings in TA sidebar
    settings = page.locator(".tva-menu .tva-menu-item:has-text('Settings')")
    if settings.count() > 0 and settings.first.is_visible():
        settings.first.click()
        page.wait_for_timeout(3000)

    # Try to click specific sub-tab based on section heading
    sub_tab_map = {
        "email template": "Email templates",
        "label": "Labels & translations",
        "translation": "Labels & translations",
        "dynamic label": "Labels & translations",
        "login": "Login & access restriction",
        "access restriction": "Login & access restriction",
        "payment": "Payments",
        "log": "Logs",
        "api key": "Api keys",
        "data cleanup": "Data Cleanup",
        "assessment upload": "Assessment uploads",
    }

    for keyword, tab_name in sub_tab_map.items():
        if keyword in heading_lower:
            tab = page.locator(f"a:has-text('{tab_name}'):visible, span:has-text('{tab_name}'):visible")
            if tab.count() > 0 and tab.first.is_visible():
                tab.first.click()
                page.wait_for_timeout(2000)
            break


def take_annotated_screenshot(
    page: Page,
    element_box: Optional[Dict],
    position: Optional[str] = None,
    highlight: bool = False,
) -> Image.Image:
    """Take a viewport screenshot and annotate it with an arrow.

    Args:
        page: Playwright page.
        element_box: Bounding box dict from Playwright (x, y, width, height).
                     If None, returns unannotated screenshot.
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
        annotate_screenshot(
            image,
            element_box,
            scroll_offset=scroll_offset,
            scale_factor=SCALE_FACTOR,
            position=position,
            highlight=highlight,
        )

    return image


def is_modal_open(page: Page) -> bool:
    """Check if a TA modal overlay is currently open and visible."""
    try:
        modal = page.locator("#tvd-modal-base:visible, .tvd-modal-overlay:visible, .tva-modal:visible")
        return modal.count() > 0 and modal.first.is_visible(timeout=300)
    except Exception:
        return False


def dismiss_modal(page: Page) -> bool:
    """Try to dismiss any open modal. Returns True if a modal was dismissed."""
    if not is_modal_open(page):
        return False

    print("      [Dismissing open modal...]")

    # Strategy 1: Click the Close button
    try:
        close_btn = page.locator(
            "#tvd-modal-base button:has-text('Close'):visible, "
            ".tva-modal-create button:has-text('Close'):visible, "
            "button.tvd-modal-close:visible, "
            ".tvd-modal-close:visible"
        )
        if close_btn.count() > 0 and close_btn.first.is_visible(timeout=500):
            close_btn.first.click(timeout=2000)
            page.wait_for_timeout(800)
            if not is_modal_open(page):
                return True
    except Exception:
        pass

    # Strategy 2: Click the X button (close icon)
    try:
        x_btn = page.locator(
            "#tvd-modal-base .tvd-modal-close:visible, "
            ".modal-close:visible, "
            "[data-dismiss='modal']:visible"
        )
        if x_btn.count() > 0 and x_btn.first.is_visible(timeout=500):
            x_btn.first.click(timeout=2000)
            page.wait_for_timeout(800)
            if not is_modal_open(page):
                return True
    except Exception:
        pass

    # Strategy 3: Press Escape
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)
        if not is_modal_open(page):
            return True
    except Exception:
        pass

    # Strategy 4: Click the overlay background to close
    try:
        overlay = page.locator(".tvd-modal-overlay:visible")
        if overlay.count() > 0:
            # Click at the very edge of the overlay (outside the modal content)
            overlay.first.click(position={"x": 5, "y": 5}, timeout=2000)
            page.wait_for_timeout(800)
            if not is_modal_open(page):
                return True
    except Exception:
        pass

    return False


def is_element_behind_modal(page: Page, locator) -> bool:
    """Check if an element is behind an open modal overlay.

    Uses JavaScript to check if the element is covered by a modal.
    """
    if not is_modal_open(page):
        return False

    try:
        # Get the element's bounding box center
        bbox = locator.bounding_box()
        if not bbox:
            return True

        cx = bbox["x"] + bbox["width"] / 2
        cy = bbox["y"] + bbox["height"] / 2

        # Use elementFromPoint to see what's actually at that position
        top_element_tag = page.evaluate(
            """([x, y]) => {
                const el = document.elementFromPoint(x, y);
                if (!el) return 'none';
                // Walk up to see if it's inside a modal
                let node = el;
                while (node) {
                    if (node.id === 'tvd-modal-base' ||
                        node.classList?.contains('tvd-modal') ||
                        node.classList?.contains('tva-modal')) {
                        return 'modal';
                    }
                    node = node.parentElement;
                }
                return el.tagName.toLowerCase();
            }""",
            [cx, cy]
        )

        # If the top element is the modal, our target is behind it
        if top_element_tag == "modal":
            # But if the target IS inside the modal, it's fine
            is_inside_modal = page.evaluate(
                """(el) => {
                    let node = el;
                    while (node) {
                        if (node.id === 'tvd-modal-base' ||
                            node.classList?.contains('tvd-modal') ||
                            node.classList?.contains('tva-modal')) {
                            return true;
                        }
                        node = node.parentElement;
                    }
                    return false;
                }""",
                locator.element_handle()
            )
            return not is_inside_modal

        return False
    except Exception:
        return False


def execute_step_action(page: Page, step: Dict, locator) -> None:
    """Execute the step's action (click, hover, type, etc.) to advance the UI state.

    After executing the action, also handles modal cleanup:
    - If the step context mentions "Save" or "click Save", clicks Save in modal
    - If a modal is still open after a type action, dismisses it
    """
    action = step.get("action", "locate")
    context = step.get("context", "").lower()

    if locator is None:
        return

    try:
        if action == "click" or action == "toggle":
            locator.click(timeout=5000)
            page.wait_for_timeout(1500)
            # Wait for any navigation or AJAX
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass

        elif action == "hover":
            locator.hover(timeout=5000)
            page.wait_for_timeout(800)

        elif action == "type":
            # For type actions, click the field to focus it, then type text
            try:
                locator.click(timeout=3000)
                page.wait_for_timeout(300)
                # Actually type sample text into the field
                sample_text = _generate_sample_text(step)
                locator.fill(sample_text)
                page.wait_for_timeout(500)
                print(f"      [Typed: '{sample_text[:40]}']")
            except Exception as type_err:
                print(f"      [Type failed: {str(type_err)[:80]}]")

            # If the step context mentions "save" or "click save",
            # try to click the Save button to close the modal and advance state
            if any(kw in context for kw in ["save", "click save", "and click"]):
                _try_click_save_in_modal(page)

        elif action == "navigate":
            locator.click(timeout=5000)
            page.wait_for_timeout(1500)
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass

            # Post-navigate: if the step says "open your course" from the courses list,
            # click the first course card to enter it
            raw_text_lower = step.get("raw_text", "").lower()
            target_lower = step.get("target", "").lower()
            if target_lower == "courses" and any(kw in raw_text_lower for kw in [
                "open your course", "click on it", "clicking on it",
                "open the course", "select your course",
            ]):
                print("      [Post-navigate: entering first course...]")
                _click_first_course_card(page)
                # Click Content tab using exact TA selectors
                _click_content_tab(page)

        elif action == "scroll":
            scroll_to_element(page, locator)

        elif action == "locate":
            # For "locate" action on Add buttons: click after screenshot to open modal
            # so the next step (type title, click save) can interact with it
            target_lower = step.get("target", "").lower()
            if target_lower.startswith("add ") and any(
                kw in target_lower for kw in ["module", "lesson", "chapter", "assessment"]
            ):
                try:
                    locator.click(timeout=3000)
                    page.wait_for_timeout(1500)
                    print(f"      [Locate+click: opened modal for '{target_lower}']")
                    # The TA modal wizard may show multiple steps before the form.
                    # Advance through: type selection → parent selection → form
                    _advance_modal_to_form(page, target_lower)
                except Exception:
                    pass

        # For other "locate" actions: do nothing (just screenshot)

    except Exception as e:
        print(f"    Warning: Could not execute action '{action}': {str(e)[:120]}")


def _generate_sample_text(step: Dict) -> str:
    """Generate sample text for type actions based on step context.

    Extracts example text from parenthetical hints in the raw text,
    or provides sensible defaults per target type.
    """
    raw = step.get("raw_text", "")
    target = step.get("target", "").lower()

    # 1. Extract text from parenthetical hints: (e.g., "Introduction to Email Marketing")
    paren_match = re.findall(r'\(e\.g\.?,?\s*["\u201c]([^"\u201d)]+)["\u201d]', raw)
    if paren_match:
        return paren_match[0]

    # 2. Extract quoted example text
    quoted = re.findall(r'"([^"]{3,50})"', raw) + re.findall(r'\u201c([^\u201d]{3,50})\u201d', raw)
    if quoted:
        return quoted[0]

    # 3. Defaults based on target type
    defaults = {
        "course title": "Introduction to Email Marketing",
        "course name": "Introduction to Email Marketing",
        "module title": "Getting Started",
        "module name": "Getting Started",
        "lesson title": "Welcome to the Course",
        "lesson name": "Welcome to the Course",
        "chapter title": "Chapter 1: Basics",
        "chapter name": "Chapter 1: Basics",
        "course summary": "Learn the fundamentals of email marketing in this comprehensive course.",
        "course description": "Learn the fundamentals of email marketing in this comprehensive course.",
        "course overview": "This course covers everything you need to know about email marketing.",
        "url": "https://example.com",
        "email": "student@example.com",
    }
    for key, default_text in defaults.items():
        if key in target:
            return default_text

    # 4. Generic fallback
    return "Sample text"


def _click_first_course_card(page: Page) -> None:
    """Click the first course card to enter a course from the courses list."""
    selectors = [
        ".tva-course-card",
        ".tva-course-item",
        ".tva-course-card-container",
        "div[class*='course-card']",
        "div[class*='course-item']",
    ]
    for sel in selectors:
        try:
            card = page.locator(sel).first
            if card.is_visible(timeout=1000):
                card.click()
                page.wait_for_timeout(2000)
                print(f"      [Entered course via: {sel}]")
                return
        except Exception:
            continue

    # Fallback: try clicking a known course title
    for title in ["Introduction to Email Marketing", "My First Course"]:
        try:
            el = page.get_by_text(title, exact=False)
            if el.count() > 0 and el.first.is_visible():
                el.first.click()
                page.wait_for_timeout(2000)
                print(f"      [Entered course via title: '{title}']")
                return
        except Exception:
            continue

    print("      [WARNING: Could not click a course card]")


def _advance_modal_to_form(page: Page, target_lower: str) -> None:
    """Advance the TA 'Add Item' modal wizard to the form step.

    The modal has multiple steps:
    - Step 0: Type selection (module/lesson/chapter/assessment)
    - Step 1: Parent selection (which module/chapter to add to)
    - Step 2: Form (title input + save)

    When clicking a specific "Add Lesson" button inside a module,
    the modal may skip step 0 and go straight to step 1 or 2.
    """
    # Wait for modal to appear
    modal = page.locator("#tvd-modal-base:visible, .tvd-modal:visible")
    try:
        modal.first.wait_for(state="visible", timeout=3000)
    except Exception:
        print("      [Modal advance: no modal appeared]")
        return

    page.wait_for_timeout(500)  # Let modal render fully

    # Check if we're already on the form step (has title input)
    form_input = page.locator("#tvd-form-modal-step input:visible")
    if form_input.count() > 0:
        print("      [Modal advance: already on form step]")
        return

    # Check all visible modal steps to understand where we are
    visible_steps = page.locator(".tva-modal-step:visible")
    print(f"      [Modal advance: {visible_steps.count()} visible modal step(s)]")

    # Step 0: If type selection is showing, click the right type
    type_map = {"add module": "module", "add lesson": "lesson",
                "add chapter": "chapter", "add assessment": "assessment"}
    item_type = type_map.get(target_lower, "lesson")
    type_btn = page.locator(f"[data-fn='setModel'][data-type='{item_type}']:visible")
    if type_btn.count() > 0:
        print(f"      [Modal advance: clicking type '{item_type}']")
        type_btn.first.click()
        page.wait_for_timeout(1500)

    # Re-check if we're now on the form step
    form_input = page.locator("#tvd-form-modal-step input:visible")
    if form_input.count() > 0:
        print("      [Modal advance: now on form step after type selection]")
        return

    # Step 1: Parent selection — select the first parent, then click Continue
    parent_step = page.locator("#tvd-parent-selection-step:visible")
    if parent_step.count() > 0:
        # Select the first available parent option in the dropdown
        parent_select = page.locator("#tva-parent-target:visible")
        if parent_select.count() > 0:
            try:
                # Select the first non-empty option
                options = parent_select.first.locator("option")
                for i in range(options.count()):
                    val = options.nth(i).get_attribute("value")
                    if val and val != "0" and val != "":
                        parent_select.first.select_option(index=i)
                        print(f"      [Modal advance: selected parent option index {i}]")
                        page.wait_for_timeout(500)
                        break
            except Exception as e:
                print(f"      [Modal advance: could not select parent: {str(e)[:80]}]")

        continue_btn = page.locator(
            "#tvd-parent-selection-step [data-fn='setParent']:visible, "
            "#tvd-parent-selection-step .tva-modal-btn-green:visible"
        )
        if continue_btn.count() > 0:
            print(f"      [Modal advance: clicking Continue in parent selection]")
            continue_btn.first.click()
            page.wait_for_timeout(2000)
    else:
        print(f"      [Modal advance: parent selection step not visible, skipping]")

    # Final check — look for any input in the modal
    page.wait_for_timeout(1000)
    form_input = page.locator("#tvd-form-modal-step input:visible")
    if form_input.count() > 0:
        print("      [Modal advance: now on form step]")
        return

    # Broader check: any text input inside the modal
    any_input = page.locator(
        "#tvd-modal-base input[type='text']:visible, "
        "#tvd-modal-base input:not([type='hidden']):visible, "
        ".tvd-modal input[type='text']:visible"
    )
    if any_input.count() > 0:
        print(f"      [Modal advance: found {any_input.count()} input(s) in modal (not in #tvd-form-modal-step)]")
    else:
        print(f"      [Modal advance: form step NOT reached, no inputs found in modal]")
        # Last resort: dump the modal's visible text for debugging
        try:
            modal_text = page.locator("#tvd-modal-base").first.inner_text(timeout=1000)
            print(f"      [Modal text: {modal_text[:200]}]")
        except Exception:
            pass


def _attempt_fallback_action(page: Page, step: Dict) -> None:
    """Try fallback actions when the primary element wasn't found.

    This prevents the UI state chain from breaking when one step fails.
    """
    action = step.get("action", "locate")
    target = step.get("target", "")

    try:
        if action == "click":
            # Try broad text search for the target
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
            # Try to find and focus the first visible input
            inputs = page.locator("input:visible, textarea:visible")
            if inputs.count() > 0:
                for i in range(min(inputs.count(), 3)):
                    try:
                        inp = inputs.nth(i)
                        if inp.is_visible(timeout=500):
                            inp.click(timeout=2000)
                            sample = _generate_sample_text(step)
                            inp.fill(sample)
                            page.wait_for_timeout(500)
                            return
                    except Exception:
                        continue

        elif action == "navigate":
            # Try clicking any link or button with the target text
            if target:
                link = page.locator(f"a:has-text('{target}'):visible, button:has-text('{target}'):visible")
                if link.count() > 0:
                    link.first.click(timeout=3000)
                    page.wait_for_timeout(1500)
                    return

    except Exception:
        pass


def _try_click_save_in_modal(page: Page) -> None:
    """Try to click a Save button inside an open modal to dismiss it.

    From TA source: modal save button uses .tva-modal-btn-green[data-fn='save']
    or .tvd-modal-save class.
    """
    try:
        save_btn = page.locator(
            ".tva-modal-btn-green[data-fn='save']:visible, "
            ".tvd-modal-save:visible, "
            "#tvd-modal-base button:has-text('Save'):visible, "
            ".tva-modal-create button:has-text('Save'):visible"
        )
        if save_btn.count() > 0 and save_btn.first.is_visible(timeout=1000):
            save_btn.first.click(timeout=3000)
            page.wait_for_timeout(1500)
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass
            print("      [Clicked Save in modal to advance state]")
    except Exception:
        pass


def capture_article(
    spec: Dict,
    output_dir: str,
    page: Page,
    start_url: Optional[str] = None,
    execute_actions: bool = True,
) -> Dict:
    """Capture screenshots for all steps in an article spec.

    Args:
        spec: Parsed article spec from step_parser.
        output_dir: Directory to save screenshots (article-specific subfolder created).
        page: Playwright page (already logged in).
        start_url: URL to navigate to before starting. Defaults to TA_URL.
        execute_actions: Whether to execute click/hover/etc. actions after each screenshot.

    Returns:
        Dict with capture results: {total, captured, skipped, errors, screenshots}.
    """
    filename = spec["filename"]
    slug = filename.replace(".md", "")
    article_dir = os.path.join(output_dir, slug)
    os.makedirs(article_dir, exist_ok=True)

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
        current_context = _get_section_context(heading)
        print(f"\n  Section: {heading} [context: {current_context}]")

        # Navigate to appropriate page for this section
        try:
            navigate_to_section(page, heading, section.get("steps", []), prev_context)
        except Exception as e:
            print(f"    Warning: Section navigation failed: {str(e)[:100]}")
            # Fall back to TA URL
            navigate_to_ta(page)

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
                image = take_annotated_screenshot(page, None)
                image.save(screenshot_path, dpi=RETINA_DPI)
                results["captured"] += 1
                results["screenshots"].append({
                    "file": screenshot_name,
                    "step": step_num,
                    "section": heading,
                    "target": target,
                    "found": True,  # Mark as found — it's a valid plain screenshot
                })
                # Try to advance state even without a specific target
                if execute_actions:
                    _attempt_fallback_action(page, step)
                continue

            # --- Pre-step: dismiss any lingering modal ---
            # If the target is NOT inside a modal (e.g., not Module Title, not Save inside modal),
            # then any open modal should be dismissed first so we can see the real page.
            # But if the target IS expected to be in a modal, leave it open.
            _target_expects_modal = (
                # Type actions into modal form fields
                (action == "type" and any(
                    kw in target.lower() for kw in ["title", "name", "url"]
                ))
                # Save button inside a modal (for lesson/module/chapter creation)
                or (target.lower() == "save" and any(
                    kw in context.lower() for kw in ["create the lesson", "create the module",
                        "create the chapter", "and click save", "click save"]
                ))
                # Any action where previous step opened a modal (title/form context)
                or (target.lower() == "save" and is_modal_open(page)
                    and page.locator("#tvd-form-modal-step:visible").count() > 0)
            )
            if not _target_expects_modal and is_modal_open(page):
                dismiss_modal(page)

            # --- Special handling for generic toggle targets (On/Off) ---
            # When a toggle step has target "On" or "Off", try to find the toggle
            # near the previous step's target instead (e.g., "Enable Comments for Courses")
            effective_target = target
            if action == "toggle" and target.lower() in ("on", "off"):
                # Look at the previous step in this section for context
                step_idx = section["steps"].index(step)
                if step_idx > 0:
                    prev_step = section["steps"][step_idx - 1]
                    prev_target = prev_step.get("target", "")
                    if prev_target and prev_target.lower() not in ("on", "off"):
                        effective_target = prev_target
                        print(f"      [Toggle: using previous step target '{effective_target}' instead of '{target}']")

            # Ensure we're on the correct tab before searching
            _ensure_correct_tab(page, step)

            # Find the target element
            locator = find_element(page, effective_target, context, action)

            if locator is None:
                print(f"    -> ⚠ ELEMENT NOT FOUND: '{target}' — step may be incorrect or UI has changed")
                image = take_annotated_screenshot(page, None)
                image.save(screenshot_path, dpi=RETINA_DPI)
                results["captured"] += 1  # Still save plain screenshot
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
                # Try fallback action to advance UI state
                if execute_actions:
                    _attempt_fallback_action(page, step)
                continue

            try:
                # --- Check if element is behind a modal ---
                if is_element_behind_modal(page, locator):
                    print(f"    -> Element '{target}' is behind a modal. Dismissing...")
                    dismiss_modal(page)
                    page.wait_for_timeout(500)
                    # Re-find the element after modal dismissed
                    locator = find_element(page, target, context, action)
                    if locator is None:
                        print(f"    -> Element NOT FOUND after modal dismiss: '{target}'.")
                        image = take_annotated_screenshot(page, None)
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
                    image = take_annotated_screenshot(page, None)
                    image.save(screenshot_path, dpi=RETINA_DPI)
                    results["skipped"] += 1
                    continue

                # Sanity check: skip annotation if element is way off-screen
                # (can happen when an element is matched but not scrolled into view)
                viewport_h = 800  # CSS pixels
                viewport_w = 1280
                if (bbox["y"] < -100 or bbox["y"] > viewport_h + 100 or
                        bbox["x"] < -100 or bbox["x"] > viewport_w + 100):
                    print(f"    -> Element off-screen (y={bbox['y']:.0f}). Unannotated screenshot.")
                    image = take_annotated_screenshot(page, None)
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
                image = take_annotated_screenshot(page, bbox)
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
                    execute_step_action(page, step, locator)

            except Exception as e:
                print(f"    -> ERROR: {str(e)[:150]}")
                # Take error screenshot
                try:
                    err_img = take_annotated_screenshot(page, None)
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
        print(f"  ⚠ VALIDATION REPORT — {len(results['validation_issues'])} step(s) could not find UI elements:")
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


def capture_articles(
    spec_files: List[str],
    output_dir: str,
    headed: bool = False,
) -> None:
    """Capture screenshots for multiple articles.

    Args:
        spec_files: List of paths to JSON spec files.
        output_dir: Root output directory for screenshots.
        headed: Run browser in headed mode (visible).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            device_scale_factor=SCALE_FACTOR,
        )
        page = context.new_page()

        try:
            login(page)

            all_results = []
            for spec_file in spec_files:
                with open(spec_file, "r") as f:
                    spec = json.load(f)

                result = capture_article(spec, output_dir, page)
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
                    print(f"    → {issue['issue']}")
                    print()
                print(f"  Full report saved to: {report_path}")
                print(f"{'='*70}")
            else:
                print(f"\n  ✓ All steps validated — every UI element was found on the page.")

        finally:
            browser.close()
