"""
Thrive Apprentice product adapter.

Contains all TA-specific logic for:
- SPA navigation (Vue.js admin panel)
- Tab switching (Course details, Content, Access restrictions, Drip)
- Multi-step modal wizard (type selection → parent selection → form)
- Complex element finding with TA CSS selectors (.tva-*, .tvd-*)
- Post-action hooks (entering courses, saving modals)
"""

import sys
import os
import re
from typing import Dict, List, Tuple, Callable, Optional
from playwright.sync_api import Page, Locator

# Add parent dirs to path so we can import the universal agent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from universal_screenshot_agent.product_adapter import GenericWebAppAdapter


class ThriveApprenticeAdapter(GenericWebAppAdapter):
    """Adapter for Thrive Apprentice — Thrive Themes' LMS plugin.

    Handles the Vue.js SPA admin, multi-step modal wizards,
    tab-based course editing, and TA-specific CSS selectors.
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self._selectors = config.get("selectors", {})
        self._tab_config = config.get("tab_switching", {})
        self._modal_config = config.get("modal_wizard", {})
        self._settings_tabs = config.get("settings_sub_tabs", {})

    # ─── Navigation ───

    def navigate_to_app(self, page: Page) -> None:
        """Navigate to Thrive Apprentice admin and wait for Vue SPA to load."""
        url = self.get_admin_entry_url()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        delay = self.get_browser_config().get("spa_load_delay_ms", 3000)
        page.wait_for_timeout(delay)

    def navigate_to_section(
        self, page: Page, heading: str,
        steps: list = None, prev_context: str = ""
    ) -> None:
        """Navigate to the appropriate page/tab for a section heading.

        Handles TA-specific navigation:
        - SPA context-aware re-navigation (avoid full reload within TA)
        - Settings sub-tab auto-selection
        - Course Content tab switching
        - Course entering from course list
        """
        heading_lower = heading.lower()
        current_context = self.get_section_context(heading)

        # Skip re-navigation if same context
        if prev_context and prev_context == current_context:
            print(f"    [Skipping re-navigation: same context '{current_context}']")
            return

        # Determine if we need full TA reload or can stay within SPA
        is_prev_ta = prev_context.startswith("ta-") if prev_context else False
        is_current_ta = current_context.startswith("ta-")

        if not is_prev_ta or not is_current_ta:
            # Coming from non-TA context or first section — do full TA load
            self.navigate_to_app(page)
        else:
            print(f"    [Staying within TA SPA: {prev_context} → {current_context}]")

        # Context-specific navigation
        if current_context == "wp-dashboard":
            page.goto(f"{self.get_local_url()}/wp-admin/")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
            return

        if current_context == "ta-courses-list":
            self._click_sidebar("Courses", page)
            return

        if current_context == "ta-course-content":
            self._navigate_to_course_content(page)
            return

        if current_context == "ta-settings":
            self._navigate_to_settings(page, heading_lower)
            return

        if current_context == "ta-products":
            self._click_sidebar("Products", page)
            return

        if current_context == "ta-design":
            self._click_sidebar("Design", page)
            return

        if current_context == "ta-course-drip":
            self._navigate_to_course_drip(page)
            return

        if current_context == "wp-pages":
            page.goto(f"{self.get_local_url()}/wp-admin/edit.php?post_type=page")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
            return

        # Default: already at TA dashboard
        print(f"    [At TA dashboard for context: {current_context}]")

    def _click_sidebar(self, item_name: str, page: Page, wait_ms: int = 2000) -> bool:
        """Click a TA sidebar menu item."""
        template = self._selectors.get("sidebar", {}).get("item_template", "")
        if template:
            sel = template.replace("{text}", item_name)
        else:
            sel = f".tva-menu .tva-menu-item:has-text('{item_name}')"

        try:
            loc = page.locator(sel)
            if loc.count() > 0 and loc.first.is_visible():
                loc.first.click()
                page.wait_for_timeout(wait_ms)
                return True
        except Exception:
            pass
        return False

    def _navigate_to_course_content(self, page: Page) -> None:
        """Navigate to a course's Content tab.

        Checks if already inside a course before doing full navigation.
        """
        tabs_sel = self._selectors.get("tabs", {})
        tab_container = tabs_sel.get("container", "ul.tva-tabs-ul")

        # Check if already inside a course (tab bar visible)
        tab_bar = page.locator(tab_container)
        if tab_bar.count() > 0:
            try:
                if tab_bar.first.is_visible(timeout=2000):
                    self._click_content_tab(page)
                    return
            except Exception:
                pass

        # Not inside a course — go to courses list first
        self._click_sidebar("Courses", page)

        # Click on the first course card
        self._click_first_course_card(page)

        # Click Content tab
        self._click_content_tab(page)

    def _click_content_tab(self, page: Page) -> bool:
        """Click the Content tab inside a course."""
        tabs_sel = self._selectors.get("tabs", {})
        content_slug = tabs_sel.get("content_tab_slug", "new")
        content_index = tabs_sel.get("content_tab_index", 1)
        tab_container = tabs_sel.get("container", "ul.tva-tabs-ul")

        selectors = [
            f"li[data-slug='{content_slug}']",
            f"{tab_container} > li[data-index='{content_index}']",
            ".tva-tab-title:has-text('Content')",
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

    def _click_first_course_card(self, page: Page) -> bool:
        """Click the first course card to enter a course."""
        card_selectors = self._selectors.get("course", {}).get("card_selectors", [
            ".tva-course-card", ".tva-course-item",
        ])
        for sel in card_selectors:
            try:
                card = page.locator(sel).first
                if card.is_visible(timeout=1000):
                    card.click()
                    page.wait_for_timeout(2000)
                    print(f"      [Entered course via: {sel}]")
                    return True
            except Exception:
                continue

        # Fallback: known course titles
        for title in self.config.get("known_course_titles", []):
            try:
                el = page.get_by_text(title, exact=False)
                if el.count() > 0 and el.first.is_visible():
                    el.first.click()
                    page.wait_for_timeout(2000)
                    print(f"      [Entered course via title: '{title}']")
                    return True
            except Exception:
                continue

        # Last resort: click first clickable heading in main content area
        try:
            main = page.locator(".tva-content-area, .tva-courses-list, main, #wpbody-content")
            if main.count() > 0:
                link = main.first.locator("a, h3, h4, .tva-title").first
                if link.is_visible(timeout=1000):
                    link.click()
                    page.wait_for_timeout(2000)
                    return True
        except Exception:
            pass

        print("      [WARNING: Could not enter a course]")
        return False

    def _navigate_to_settings(self, page: Page, heading_lower: str = "") -> None:
        """Navigate to TA Settings page and optionally click a sub-tab."""
        self._click_sidebar("Settings", page, wait_ms=3000)

        # Try to click specific sub-tab based on section heading
        for keyword, tab_name in self._settings_tabs.items():
            if keyword in heading_lower:
                tab = page.locator(
                    f"a:has-text('{tab_name}'):visible, span:has-text('{tab_name}'):visible"
                )
                if tab.count() > 0 and tab.first.is_visible():
                    tab.first.click()
                    page.wait_for_timeout(2000)
                break

    def _navigate_to_course_drip(self, page: Page) -> None:
        """Navigate to the first course's Drip tab."""
        self._click_sidebar("Courses", page)

        # Click first course card
        card_selectors = self._selectors.get("course", {}).get("card_selectors", [".tva-course-card"])
        for sel in card_selectors[:2]:
            try:
                card = page.locator(sel).first
                if card.is_visible():
                    card.click()
                    page.wait_for_timeout(2000)
                    break
            except Exception:
                continue

        # Click Drip tab
        drip_tab = page.locator(".tva-tab-title:has-text('Drip')")
        if drip_tab.count() > 0 and drip_tab.first.is_visible():
            drip_tab.first.click()
            page.wait_for_timeout(2000)

    # ─── Tab Management ───

    def ensure_correct_tab(self, page: Page, step: Dict) -> None:
        """Auto-switch to Content tab when the step's target requires it.

        Skips when:
        - Target is a modal input field (would close the modal)
        - Content tab is already selected
        - We're not inside a course
        """
        target_lower = step.get("target", "").lower()

        # Targets that only appear inside modals — never switch tabs
        modal_targets = set(self._tab_config.get("modal_targets", []))
        if target_lower in modal_targets:
            return

        # Targets that need the Content tab
        content_targets = set(self._tab_config.get("content_tab_targets", []))
        if target_lower not in content_targets:
            return

        # Don't switch tabs if a modal is currently open
        if self.is_modal_open(page):
            return

        # Check if Content tab is already selected
        tabs_sel = self._selectors.get("tabs", {})
        content_slug = tabs_sel.get("content_tab_slug", "new")
        selected = page.locator(f"li.tva-tab-selected[data-slug='{content_slug}']")
        try:
            if selected.count() > 0 and selected.first.is_visible(timeout=500):
                return  # Already on Content tab
        except Exception:
            pass

        # Check if we're inside a course (tab bar visible)
        tab_container = tabs_sel.get("container", "ul.tva-tabs-ul")
        tab_bar = page.locator(tab_container)
        if tab_bar.count() > 0:
            try:
                if tab_bar.first.is_visible(timeout=500):
                    print(f"      [Auto-switching to Content tab for target '{target_lower}']")
                    self._click_content_tab(page)
            except Exception:
                pass

    # ─── Element Finding ───

    def get_element_strategies(
        self, page: Page, target: str, context: str, action: str
    ) -> List[Tuple[str, Callable]]:
        """Return TA-specific element-finding strategies.

        Includes all the Thrive Apprentice CSS selectors (.tva-*, .tvd-*),
        sidebar items, course tabs, action buttons, modals, and more.
        """
        strategies = []
        target_lower = target.lower()
        ctx_lower = context.lower() if context else ""

        # ─── Form fields (type action) ───
        if action == "type":
            # Course name input
            if any(kw in target_lower for kw in ["course title", "course name"]):
                course_input = self._selectors.get("course", {}).get("course_name_input", "")
                if course_input:
                    strategies.append((
                        "tva-course-name",
                        lambda s=course_input: page.locator(s)
                    ))

            # Modal title inputs (module/lesson/chapter)
            if any(kw in target_lower for kw in ["module title", "lesson title", "chapter title"]):
                form_step = self._selectors.get("modals", {}).get("form_step", "#tvd-form-modal-step")
                strategies.append((
                    "tva-modal-title-input",
                    lambda fs=form_step: page.locator(f"{fs} input[type='text']:visible, {fs} input:visible")
                ))
                # Placeholder-based match
                kind = target_lower.split()[0].title()
                strategies.append((
                    f"tva-{kind.lower()}-title",
                    lambda k=kind: page.locator(f"input[placeholder*='{k} Title' i], input[placeholder*='{k} Name' i]")
                ))

        # ─── Toggle strategies ───
        if action == "toggle" or "toggle" in ctx_lower:
            strategies.append((
                "tva-toggle-in-row", lambda t=target: page.locator(
                    f".tva-settings-row:has-text('{t}') .tvd-switch:visible, "
                    f".tva-settings-row:has-text('{t}') input[type='checkbox']:visible, "
                    f"tr:has-text('{t}') input[type='checkbox']:visible, "
                    f"div.setting-row:has-text('{t}') input[type='checkbox']:visible"
                )
            ))
            strategies.append((
                "tva-toggle-near-label", lambda t=target: page.locator(
                    f"div:has(> *:has-text('{t}')) .tvd-switch:visible, "
                    f"div:has(> *:has-text('{t}')) .tva-toggle:visible"
                )
            ))

        # ─── Sidebar navigation ───
        sidebar = self._selectors.get("sidebar", {})
        known_items = [x.lower() for x in sidebar.get("known_items", [])]
        if target_lower in known_items:
            strategies.append((
                "tva-sidebar-known", lambda t=target: page.locator(
                    f".tva-menu .tva-menu-item:has-text('{t}'), "
                    f".tva-menu a.tva-menu-item:has-text('{t}')"
                )
            ))

        # Sidebar context hint
        if any(kw in ctx_lower for kw in ["sidebar", "left", "menu", "navigation", "nav"]):
            strategies.append((
                "tva-sidebar-item", lambda t=target: page.locator(
                    f".tva-menu .tva-menu-item:has-text('{t}'), "
                    f".tva-menu a.tva-menu-item:has-text('{t}')"
                )
            ))

        # ─── Course tabs ───
        tab_slug_map = self._selectors.get("tabs", {}).get("slug_map", {})
        if any(kw in ctx_lower for kw in ["tab"]) or target_lower in tab_slug_map:
            slug = tab_slug_map.get(target_lower)
            if slug:
                strategies.append((
                    "tva-course-tab-slug",
                    lambda s=slug: page.locator(f"ul.tva-tabs-ul > li[data-slug='{s}']")
                ))
            strategies.append((
                "tva-course-tab", lambda t=target: page.locator(f".tva-tab-title:has-text('{t}')")
            ))

        # ─── Settings sub-tabs ───
        if any(kw in ctx_lower for kw in ["settings", "tab", "section"]):
            strategies.append((
                "tva-settings-tab", lambda t=target: page.locator(
                    f".tva-settings-tab:has-text('{t}'), .tva-tab-title:has-text('{t}')"
                )
            ))

        # ─── Action buttons (Add Module, Add Lesson, etc.) ───
        action_btns = self._selectors.get("action_buttons", {})
        type_map = action_btns.get("type_map", {})
        if target_lower in type_map or target_lower.startswith("add "):
            item_type = type_map.get(target_lower)
            if item_type:
                add_sel = action_btns.get("add_item_selector", "")
                if add_sel:
                    strategies.append((
                        "tva-add-by-data-type",
                        lambda s=add_sel.replace("{type}", item_type): page.locator(s)
                    ))
                class_map = action_btns.get("class_map", {})
                css_class = class_map.get(item_type, "")
                if css_class:
                    strategies.append((
                        "tva-add-by-class",
                        lambda c=css_class, t=item_type: page.locator(
                            f"{c}[data-type='{t}']:visible, {c}:has-text('{t.title()}'):visible"
                        )
                    ))
            # Text fallback
            strategies.append((
                "tva-action-btn", lambda t=target: page.locator(
                    f"button:has-text('{t}'):visible, "
                    f"a:has-text('{t}'):visible, "
                    f"div.tva-course-add:has-text('{t}'):visible, "
                    f"span:has-text('{t}'):visible"
                )
            ))

        # ─── Save / green buttons ───
        if target_lower in {"save", "save and continue", "continue", "publish", "done"}:
            strategies.append((
                "tva-modal-save",
                lambda: page.locator(
                    ".tva-modal-btn-green[data-fn='save']:visible, "
                    ".tvd-modal-save:visible"
                )
            ))
            strategies.append((
                "tva-save-btn", lambda t=target: page.locator(
                    f"button.tva-btn-green:has-text('{t}'):visible, "
                    f"button.tvd-btn-green:has-text('{t}'):visible, "
                    f"button:has-text('{t}'):visible"
                )
            ))

        # ─── Course status / publishing ───
        if target_lower in {"course status", "published", "unpublished", "draft", "scheduled"}:
            pub_btn = self._selectors.get("course", {}).get("publish_button", "#tva-course-publish")
            strategies.append((
                "tva-course-publish-btn",
                lambda s=pub_btn: page.locator(f"{s}:visible")
            ))
        if target_lower == "publish" and any(kw in ctx_lower for kw in ["dropdown", "select", "option"]):
            strategies.append((
                "tva-publish-option",
                lambda: page.locator(
                    ".tva-course-status-drop a:has-text('Publish'):visible, "
                    ".tva-course-status-drop li:has-text('Publish'):visible"
                )
            ))

        # ─── Modal buttons ───
        strategies.append((
            "tva-modal-btn", lambda t=target: page.locator(
                f"#tvd-modal-base button:has-text('{t}'):visible, "
                f".tva-modal-create button:has-text('{t}'):visible"
            )
        ))

        # ─── Edit links ───
        if target_lower in {"edit content", "edit module details", "edit", "delete module"}:
            strategies.append((
                "tva-edit-link", lambda t=target: page.locator(
                    f".tva-course-item a:has-text('{t}'):visible, "
                    f".tva-item-actions a:has-text('{t}'):visible, "
                    f"a:has-text('{t}'):visible"
                )
            ))

        # ─── Course labels ───
        if target_lower in {"course overview", "course summary", "course description", "cover image"}:
            strategies.append((
                "tva-label", lambda t=target: page.locator(
                    f"label.course-label:has-text('{t}'):visible, "
                    f"label:has-text('{t}'):visible, "
                    f"h3:has-text('{t}'):visible, "
                    f"h4:has-text('{t}'):visible, "
                    f".tva-section-title:has-text('{t}'):visible"
                )
            ))
        if target_lower == "course description":
            strategies.append((
                "tva-course-summary", lambda: page.locator(
                    "label.course-label:has-text('Course summary'):visible, "
                    "label:has-text('Course summary'):visible"
                )
            ))

        # ─── Vague course targets ───
        vague_targets = self._selectors.get("vague_course_targets", [])
        if target_lower in vague_targets:
            strategies.append((
                "tva-course-card",
                lambda: page.locator(".tva-course-card:visible")
            ))

        # ─── AI / Generate with AI ───
        if any(kw in target_lower for kw in ["generate with ai", "generate course", "remix"]):
            strategies.append((
                "tva-ai-btn", lambda t=target: page.locator(
                    f"button:has-text('{t}'):visible, "
                    f"a:has-text('{t}'):visible, "
                    f"span:has-text('{t}'):visible, "
                    f".tva-ai-generate:has-text('{t}'):visible"
                )
            ))

        # ─── Thrive Architect ───
        if any(kw in target_lower for kw in ["launch thrive architect", "thrive architect", "edit with thrive"]):
            strategies.append((
                "tva-architect-btn", lambda t=target: page.locator(
                    f"a:has-text('{t}'):visible, "
                    f"button:has-text('{t}'):visible, "
                    f"#thrive_preview_button:visible, "
                    f".tcb-enable-editor:visible"
                )
            ))

        # ─── Dynamic text ───
        if any(kw in target_lower for kw in ["dynamic text", "dynamic field", "insert dynamic"]):
            strategies.append((
                "tva-dynamic-text", lambda t=target: page.locator(
                    f"button:has-text('{t}'):visible, "
                    f"a:has-text('{t}'):visible, "
                    f".tcb-inline-dynamic:visible, "
                    f"[data-fn='dynamic_text']:visible"
                )
            ))

        # ─── WP admin menu items ───
        wp_admin = self._selectors.get("wp_admin", {})
        wp_items = [x.lower() for x in wp_admin.get("known_items", [])]
        if target_lower in wp_items:
            strategies.append((
                "wp-adminmenu", lambda t=target: page.locator(f"#adminmenu a:has-text('{t}')")
            ))

        # ─── WP Pages ───
        if any(kw in target_lower for kw in ["pages", "add new"]):
            strategies.append((
                "wp-pages", lambda t=target: page.locator(f"#adminmenu a:has-text('{t}'):visible")
            ))

        # ─── WP admin bar ───
        strategies.append((
            "wp-adminbar", lambda t=target: page.locator(f"#wpadminbar a:has-text('{t}')")
        ))

        # ─── TA section map ───
        section_map = self._selectors.get("section_map", {})
        for keyword, selector in section_map.items():
            if keyword in target_lower:
                strategies.append((
                    f"ta-section-{keyword}",
                    lambda sel=selector: page.locator(sel)
                ))

        return strategies

    # ─── Modal Handling ───

    def is_modal_open(self, page: Page) -> bool:
        """Check if a TA modal overlay is currently open."""
        modal_sel = self._selectors.get("modals", {}).get("overlay", "")
        if not modal_sel:
            return False
        try:
            modal = page.locator(modal_sel)
            return modal.count() > 0 and modal.first.is_visible(timeout=300)
        except Exception:
            return False

    def dismiss_modal(self, page: Page) -> bool:
        """Dismiss an open TA modal using multiple strategies."""
        if not self.is_modal_open(page):
            return False

        print("      [Dismissing open modal...]")
        modals_sel = self._selectors.get("modals", {})

        # Strategy 1: Close button
        close_sel = modals_sel.get("close_button", "")
        if close_sel:
            try:
                close_btn = page.locator(close_sel.strip())
                if close_btn.count() > 0 and close_btn.first.is_visible(timeout=500):
                    close_btn.first.click(timeout=2000)
                    page.wait_for_timeout(800)
                    if not self.is_modal_open(page):
                        return True
            except Exception:
                pass

        # Strategy 2: X button
        x_sel = modals_sel.get("x_button", "")
        if x_sel:
            try:
                x_btn = page.locator(x_sel.strip())
                if x_btn.count() > 0 and x_btn.first.is_visible(timeout=500):
                    x_btn.first.click(timeout=2000)
                    page.wait_for_timeout(800)
                    if not self.is_modal_open(page):
                        return True
            except Exception:
                pass

        # Strategy 3: Escape key
        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(800)
            if not self.is_modal_open(page):
                return True
        except Exception:
            pass

        # Strategy 4: Click overlay background
        try:
            overlay = page.locator(".tvd-modal-overlay:visible")
            if overlay.count() > 0:
                overlay.first.click(position={"x": 5, "y": 5}, timeout=2000)
                page.wait_for_timeout(800)
                if not self.is_modal_open(page):
                    return True
        except Exception:
            pass

        return False

    def advance_modal(self, page: Page, target: str) -> None:
        """Advance the TA 'Add Item' modal wizard to the form step.

        Steps: type selection → parent selection → form (title input + save)
        """
        target_lower = target.lower()

        # Wait for modal
        modal_sel = self._selectors.get("modals", {}).get("overlay", "")
        try:
            page.locator(modal_sel).first.wait_for(state="visible", timeout=3000)
        except Exception:
            print("      [Modal advance: no modal appeared]")
            return

        page.wait_for_timeout(500)

        # Check if already on form step
        form_step = self._selectors.get("modals", {}).get("form_step", "#tvd-form-modal-step")
        form_input = page.locator(f"{form_step} input:visible")
        if form_input.count() > 0:
            print("      [Modal advance: already on form step]")
            return

        # Step 0: Type selection
        wizard = self._modal_config.get("type_selection", {})
        wizard_types = wizard.get("type_map", {})
        item_type = wizard_types.get(target_lower, "lesson")
        type_btn_sel = wizard.get("button_selector", "").replace("{type}", item_type)
        if type_btn_sel:
            type_btn = page.locator(type_btn_sel)
            if type_btn.count() > 0:
                print(f"      [Modal advance: clicking type '{item_type}']")
                type_btn.first.click()
                page.wait_for_timeout(1500)

        # Re-check form step
        form_input = page.locator(f"{form_step} input:visible")
        if form_input.count() > 0:
            print("      [Modal advance: now on form step after type selection]")
            return

        # Step 1: Parent selection
        parent_config = self._modal_config.get("parent_selection", {})
        parent_step_sel = parent_config.get("step_selector", "#tvd-parent-selection-step:visible")
        parent_step = page.locator(parent_step_sel)
        if parent_step.count() > 0:
            parent_dropdown_sel = parent_config.get("parent_dropdown", "#tva-parent-target:visible")
            parent_select = page.locator(parent_dropdown_sel)
            if parent_select.count() > 0:
                try:
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

            continue_sel = parent_config.get("continue_button", "")
            if continue_sel:
                continue_btn = page.locator(continue_sel.strip())
                if continue_btn.count() > 0:
                    print(f"      [Modal advance: clicking Continue in parent selection]")
                    continue_btn.first.click()
                    page.wait_for_timeout(2000)

        # Final check
        page.wait_for_timeout(1000)
        form_input = page.locator(f"{form_step} input:visible")
        if form_input.count() > 0:
            print("      [Modal advance: now on form step]")
        else:
            any_input = page.locator(
                "#tvd-modal-base input[type='text']:visible, "
                "#tvd-modal-base input:not([type='hidden']):visible, "
                ".tvd-modal input[type='text']:visible"
            )
            if any_input.count() > 0:
                print(f"      [Modal advance: found {any_input.count()} input(s) in modal]")
            else:
                print(f"      [Modal advance: form step NOT reached]")

    def is_element_behind_modal(self, page: Page, locator: Locator) -> bool:
        """Check if an element is behind an open modal overlay using JS."""
        if not self.is_modal_open(page):
            return False

        try:
            bbox = locator.bounding_box()
            if not bbox:
                return True

            cx = bbox["x"] + bbox["width"] / 2
            cy = bbox["y"] + bbox["height"] / 2

            top_element_tag = page.evaluate(
                """([x, y]) => {
                    const el = document.elementFromPoint(x, y);
                    if (!el) return 'none';
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

            if top_element_tag == "modal":
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

    # ─── Post-Action Hooks ───

    def post_action_hook(self, page: Page, step: Dict, action: str) -> None:
        """TA-specific post-action logic.

        Handles:
        - Clicking Save in modal after type actions
        - Entering course after navigating to Courses
        - Advancing modal wizard after clicking Add buttons
        """
        target_lower = step.get("target", "").lower()
        context = step.get("context", "").lower()

        # After type: if context mentions "save", click Save in modal
        if action == "type" and any(kw in context for kw in ["save", "click save", "and click"]):
            self._try_click_save_in_modal(page)

        # After navigate: if "open your course", enter the course
        if action == "navigate":
            raw_text_lower = step.get("raw_text", "").lower()
            if target_lower == "courses" and any(kw in raw_text_lower for kw in [
                "open your course", "click on it", "clicking on it",
                "open the course", "select your course",
            ]):
                print("      [Post-navigate: entering first course...]")
                self._click_first_course_card(page)
                self._click_content_tab(page)

        # After locate on Add buttons: click to open modal, advance wizard
        if action == "locate":
            if target_lower.startswith("add ") and any(
                kw in target_lower for kw in ["module", "lesson", "chapter", "assessment"]
            ):
                try:
                    # Re-find the element to click it
                    from universal_screenshot_agent.element_finder import find_element
                    locator = find_element(page, step["target"], step.get("context", ""), "click", adapter=self)
                    if locator:
                        locator.click(timeout=3000)
                        page.wait_for_timeout(1500)
                        print(f"      [Locate+click: opened modal for '{target_lower}']")
                        self.advance_modal(page, target_lower)
                except Exception:
                    pass

    def _try_click_save_in_modal(self, page: Page) -> None:
        """Click Save button inside an open modal."""
        save_sel = self._selectors.get("modals", {}).get("save_button", "")
        if not save_sel:
            return
        try:
            save_btn = page.locator(save_sel.strip())
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
