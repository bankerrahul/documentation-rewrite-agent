"""
Smart UI element location for Thrive Apprentice admin pages.
Tries multiple strategies to find a target element by its text label.

Strategy priority (high → low):
1. Thrive Apprentice-specific CSS selectors (most precise)
2. WordPress admin-specific selectors
3. Playwright role-based selectors
4. Text-based selectors with context filtering
5. Form field strategies (for 'type' actions)
"""

from typing import Optional, List, Tuple, Callable
from playwright.sync_api import Page, Locator


def find_element(
    page: Page,
    target: str,
    context: str = "",
    action: str = "click",
) -> Optional[Locator]:
    """Try multiple strategies to find a target UI element on the page.

    Args:
        page: Playwright page.
        target: The UI element text label (e.g., "Thrive Apprentice", "Save", "Add Course").
        context: Descriptive context (e.g., "left sidebar", "dropdown", "top of the page").
        action: The action type (click, hover, type, etc.) for context-aware finding.

    Returns:
        A Playwright Locator pointing to the element, or None if not found.
    """
    if not target:
        return None

    strategies = _build_strategies(page, target, context, action)

    for name, strategy_fn in strategies:
        try:
            locator = strategy_fn()
            if locator is not None:
                # Check if element exists and is visible
                count = locator.count()
                if count > 0:
                    # Try to find the first visible one
                    for i in range(min(count, 5)):
                        el = locator.nth(i)
                        try:
                            if el.is_visible(timeout=1000):
                                return el
                        except Exception:
                            continue
        except Exception:
            continue

    return None


def _build_strategies(
    page: Page, target: str, context: str, action: str
) -> List[Tuple[str, Callable]]:
    """Build ordered list of (name, fn) strategies to try."""
    ctx_lower = context.lower() if context else ""
    target_lower = target.lower()

    strategies = []

    # ================================================================
    # Form field strategies (for 'type' actions) — highest priority
    # ================================================================
    if action == "type":
        # Input by placeholder text (e.g., "Course Title" → input[placeholder*="Course"])
        strategies.append(
            ("input-placeholder", lambda t=target: page.locator(f"input[placeholder*='{t}' i]:visible"))
        )
        # Textarea by placeholder
        strategies.append(
            ("textarea-placeholder", lambda t=target: page.locator(f"textarea[placeholder*='{t}' i]:visible"))
        )
        # Input with label nearby
        strategies.append(
            ("label-input", lambda t=target: page.locator(
                f"label:has-text('{t}') + input, "
                f"label:has-text('{t}') + div input, "
                f"label:has-text('{t}') + textarea"
            ))
        )
        # Thrive Apprentice course name input (the top input on course editor)
        if any(kw in target_lower for kw in ["course title", "course name"]):
            strategies.insert(0, (
                "tva-course-name",
                lambda: page.locator("input[placeholder*='Course name' i], input[placeholder*='name' i].tva-course-name")
            ))
        # Module/Lesson/Chapter title inputs in modals
        # From TA source: modal form is inside #tvd-form-modal-step
        if any(kw in target_lower for kw in ["module title", "lesson title", "chapter title"]):
            kind = target_lower.split()[0].title()  # Module, Lesson, Chapter
            # Highest priority: input inside the TA modal form step
            strategies.insert(0, (
                "tva-modal-title-input",
                lambda: page.locator(
                    "#tvd-form-modal-step input[type='text']:visible, "
                    "#tvd-form-modal-step input:visible"
                )
            ))
            # Also try placeholder-based match
            strategies.insert(1, (
                f"tva-{kind.lower()}-title",
                lambda k=kind: page.locator(f"input[placeholder*='{k} Title' i], input[placeholder*='{k} Name' i]")
            ))

    # ================================================================
    # Toggle/switch strategies (for 'toggle' actions)
    # ================================================================
    if action == "toggle" or "toggle" in ctx_lower:
        # Look for a toggle switch near the target text label.
        # Thrive Apprentice uses custom toggle switches (divs with classes like
        # tvd-switch, tva-toggle, etc.) and also standard checkboxes.

        # Strategy: find the label text, then look for a toggle/checkbox sibling nearby
        strategies.insert(0, (
            "toggle-near-label", lambda t=target: page.locator(
                f"div:has(> *:has-text('{t}')) input[type='checkbox']:visible, "
                f"div:has(> *:has-text('{t}')) .tvd-switch:visible, "
                f"div:has(> *:has-text('{t}')) .tva-toggle:visible, "
                f"label:has-text('{t}') input[type='checkbox'], "
                f"label:has-text('{t}') + .tvd-switch, "
                f"label:has-text('{t}') ~ input[type='checkbox']"
            )
        ))

        # For TA settings toggles: look for the row containing the label text
        # and find the toggle within that row
        strategies.insert(0, (
            "toggle-in-row", lambda t=target: page.locator(
                f".tva-settings-row:has-text('{t}') .tvd-switch:visible, "
                f".tva-settings-row:has-text('{t}') input[type='checkbox']:visible, "
                f"tr:has-text('{t}') input[type='checkbox']:visible, "
                f"div.setting-row:has-text('{t}') input[type='checkbox']:visible"
            )
        ))

        # Fallback: just find the text label itself (the arrow will point at the label area)
        strategies.insert(0, (
            "toggle-label-text", lambda t=target: page.locator(
                f"span:has-text('{t}'):visible, "
                f"label:has-text('{t}'):visible, "
                f"p:has-text('{t}'):visible"
            )
        ))

        # For multi-word targets, also try matching individual significant keywords
        # E.g., "Automatic Login" → try "auto-login", "login"
        target_words = [w for w in target_lower.split() if len(w) > 3 and w not in (
            "the", "this", "that", "from", "with", "your", "into", "enable", "disable"
        )]
        for word in target_words:
            strategies.append((
                f"toggle-keyword-{word}", lambda w=word: page.locator(
                    f"span:has-text('{w}'):visible, "
                    f"label:has-text('{w}'):visible, "
                    f"p:has-text('{w}'):visible"
                )
            ))
            # Also try with hyphenated variant (e.g., "login" → "auto-login")
            strategies.append((
                f"toggle-keyword-hyphen-{word}", lambda w=word: page.locator(
                    f"span:text-matches('.*{w}.*', 'i'):visible, "
                    f"label:text-matches('.*{w}.*', 'i'):visible, "
                    f"p:text-matches('.*{w}.*', 'i'):visible"
                )
            ))

    # ================================================================
    # Thrive Apprentice-specific selectors
    # ================================================================

    # --- TA Left sidebar navigation (Home, Courses, Members, Reports, etc.) ---
    # The TA sidebar uses: div.tva-menu > div.tva-menu-item[data-route]
    if any(kw in ctx_lower for kw in ["sidebar", "left", "menu", "navigation", "nav"]):
        strategies.append(
            ("tva-sidebar-item", lambda t=target: page.locator(
                f".tva-menu .tva-menu-item:has-text('{t}'), "
                f".tva-menu a.tva-menu-item:has-text('{t}')"
            ))
        )

    # --- TA Generate with AI / AI-specific elements ---
    if any(kw in target_lower for kw in ["generate with ai", "generate course", "remix"]):
        strategies.insert(0, (
            "tva-ai-btn", lambda t=target: page.locator(
                f"button:has-text('{t}'):visible, "
                f"a:has-text('{t}'):visible, "
                f"span:has-text('{t}'):visible, "
                f".tva-ai-generate:has-text('{t}'):visible"
            )
        ))

    # --- Thrive Architect launch button ---
    if any(kw in target_lower for kw in ["launch thrive architect", "thrive architect", "edit with thrive"]):
        strategies.insert(0, (
            "tva-architect-btn", lambda t=target: page.locator(
                f"a:has-text('{t}'):visible, "
                f"button:has-text('{t}'):visible, "
                f"#thrive_preview_button:visible, "
                f".tcb-enable-editor:visible"
            )
        ))

    # --- WP Pages / Posts admin items ---
    if any(kw in target_lower for kw in ["pages", "add new"]):
        strategies.insert(0, (
            "wp-pages", lambda t=target: page.locator(f"#adminmenu a:has-text('{t}'):visible")
        ))

    # --- Dynamic text / field insertion ---
    if any(kw in target_lower for kw in ["dynamic text", "dynamic field", "insert dynamic"]):
        strategies.insert(0, (
            "tva-dynamic-text", lambda t=target: page.locator(
                f"button:has-text('{t}'):visible, "
                f"a:has-text('{t}'):visible, "
                f".tcb-inline-dynamic:visible, "
                f"[data-fn='dynamic_text']:visible"
            )
        ))

    # Always try TA sidebar for well-known sidebar items
    _sidebar_items = {
        "home", "courses", "members", "reports", "design", "products",
        "protected files", "settings", "notice", "preview", "assessments",
    }
    if target_lower in _sidebar_items:
        strategies.insert(0, (
            "tva-sidebar-known", lambda t=target: page.locator(
                f".tva-menu .tva-menu-item:has-text('{t}'), "
                f".tva-menu a.tva-menu-item:has-text('{t}')"
            )
        ))

    # --- TA Course tabs (Course details, Content, Access restrictions, Drip, etc.) ---
    # From TA source: tabs use data-slug attributes on li elements within ul.tva-tabs-ul
    _tab_slug_map = {
        "course details": "details", "content": "new",
        "access restrictions": "access", "drip": "drip",
        "course completion": "completion", "view reports": None,
    }
    if any(kw in ctx_lower for kw in ["tab"]) or target_lower in _tab_slug_map:
        slug = _tab_slug_map.get(target_lower)
        if slug:
            strategies.insert(0, (
                "tva-course-tab-slug",
                lambda s=slug: page.locator(f"ul.tva-tabs-ul > li[data-slug='{s}']")
            ))
        strategies.insert(1 if slug else 0, (
            "tva-course-tab", lambda t=target: page.locator(
                f".tva-tab-title:has-text('{t}')"
            )
        ))

    # --- TA Settings sub-tabs (General, Login & Access, etc.) ---
    if any(kw in ctx_lower for kw in ["settings", "tab", "section"]):
        strategies.append(
            ("tva-settings-tab", lambda t=target: page.locator(
                f".tva-settings-tab:has-text('{t}'), "
                f".tva-tab-title:has-text('{t}')"
            ))
        )

    # --- TA Action buttons (Add Course, Add Lesson, Add Module, etc.) ---
    # From TA source: buttons use data-fn="openAddItemModal" and data-type attributes
    _ta_action_btns = {
        "add course", "add lesson", "add module", "add chapter", "add assessment",
        "add new course", "create your first course", "add content",
    }
    if target_lower in _ta_action_btns or target_lower.startswith("add "):
        # Highest priority: exact data-type selector from TA source code
        _type_map = {
            "add module": "module", "add lesson": "lesson",
            "add chapter": "chapter", "add assessment": "assessment",
        }
        item_type = _type_map.get(target_lower)
        if item_type:
            strategies.insert(0, (
                "tva-add-by-data-type",
                lambda t=item_type: page.locator(
                    f"[data-fn='openAddItemModal'][data-type='{t}']:visible"
                )
            ))
            # Also try TA-specific CSS classes
            _class_map = {"module": ".tva-add-main-btn", "lesson": ".tva-add-lesson",
                          "chapter": ".tva-add-chapter", "assessment": ".tva-add-main-btn"}
            css_class = _class_map.get(item_type, "")
            if css_class:
                strategies.insert(1, (
                    "tva-add-by-class",
                    lambda c=css_class, t=item_type: page.locator(
                        f"{c}[data-type='{t}']:visible, {c}:has-text('{t.title()}'):visible"
                    )
                ))

        # Fallback: text-based match
        strategies.append((
            "tva-action-btn", lambda t=target: page.locator(
                f"button:has-text('{t}'):visible, "
                f"a:has-text('{t}'):visible, "
                f"div.tva-course-add:has-text('{t}'):visible, "
                f"span:has-text('{t}'):visible"
            )
        ))

    # --- TA Save / green buttons ---
    # From TA source: modal save uses .tva-modal-btn-green[data-fn="save"] / .tvd-modal-save
    if target_lower in {"save", "save and continue", "continue", "publish", "done"}:
        strategies.insert(0, (
            "tva-modal-save",
            lambda: page.locator(
                ".tva-modal-btn-green[data-fn='save']:visible, "
                ".tvd-modal-save:visible"
            )
        ))
        strategies.insert(1, (
            "tva-save-btn", lambda t=target: page.locator(
                f"button.tva-btn-green:has-text('{t}'):visible, "
                f"button.tvd-btn-green:has-text('{t}'):visible, "
                f"button:has-text('{t}'):visible"
            )
        ))

    # --- TA Course status / publishing ---
    if target_lower in {"course status", "published", "unpublished", "draft", "scheduled"}:
        strategies.insert(0, (
            "tva-course-publish-btn",
            lambda: page.locator("#tva-course-publish:visible")
        ))
    # "Publish" as a dropdown option (not the button itself)
    if target_lower == "publish" and any(kw in ctx_lower for kw in ["dropdown", "select", "option"]):
        strategies.insert(0, (
            "tva-publish-option",
            lambda: page.locator(
                ".tva-course-status-drop a:has-text('Publish'):visible, "
                ".tva-course-status-drop li:has-text('Publish'):visible"
            )
        ))

    # --- TA Modal buttons ---
    strategies.append(
        ("tva-modal-btn", lambda t=target: page.locator(
            f"#tvd-modal-base button:has-text('{t}'):visible, "
            f".tva-modal-create button:has-text('{t}'):visible"
        ))
    )

    # --- Edit Module Details / Edit Content links ---
    if target_lower in {"edit content", "edit module details", "edit", "delete module"}:
        strategies.insert(0, (
            "tva-edit-link", lambda t=target: page.locator(
                f".tva-course-item a:has-text('{t}'):visible, "
                f".tva-item-actions a:has-text('{t}'):visible, "
                f"a:has-text('{t}'):visible"
            )
        ))

    # --- Course overview / summary / description labels ---
    if target_lower in {"course overview", "course summary", "course description", "cover image"}:
        strategies.insert(0, (
            "tva-label", lambda t=target: page.locator(
                f"label.course-label:has-text('{t}'):visible, "
                f"label:has-text('{t}'):visible, "
                f"h3:has-text('{t}'):visible, "
                f"h4:has-text('{t}'):visible, "
                f".tva-section-title:has-text('{t}'):visible"
            )
        ))
    # Map "Course Description" → "Course summary" (TA uses "summary" not "description")
    if target_lower == "course description":
        strategies.insert(0, (
            "tva-course-summary", lambda: page.locator(
                "label.course-label:has-text('Course summary'):visible, "
                "label:has-text('Course summary'):visible"
            )
        ))

    # --- TA Course card (for vague "your course" / "the course" targets) ---
    if target_lower in {"your course", "the course", "course you want", "first course"}:
        strategies.insert(0, (
            "tva-course-card",
            lambda: page.locator(".tva-course-card:visible")
        ))

    # ================================================================
    # WordPress admin-specific selectors
    # ================================================================

    # --- WP admin sidebar (Thrive Dashboard submenu) ---
    # Only match WP admin menu for known WP/Thrive menu items
    _wp_menu_items = {
        "thrive dashboard", "thrive apprentice", "thrive comments", "thrive ovation",
        "thrive optimize", "thrive leads", "thrive quiz builder", "thrive ultimatum",
        "thrive theme builder", "product manager", "dashboard", "posts", "pages",
        "media", "appearance", "plugins", "users", "tools", "settings",
    }
    if target_lower in _wp_menu_items:
        strategies.insert(0, (
            "wp-adminmenu", lambda t=target: page.locator(f"#adminmenu a:has-text('{t}')")
        ))

    # WP admin bar
    strategies.append(
        ("wp-adminbar", lambda t=target: page.locator(f"#wpadminbar a:has-text('{t}')"))
    )

    # ================================================================
    # Generic role-based strategies (Playwright best practices)
    # ================================================================

    # Buttons
    strategies.append(
        ("role-button", lambda t=target: page.get_by_role("button", name=t, exact=False))
    )

    # Links
    strategies.append(
        ("role-link", lambda t=target: page.get_by_role("link", name=t, exact=False))
    )

    # Tabs
    strategies.append(
        ("role-tab", lambda t=target: page.get_by_role("tab", name=t, exact=False))
    )

    # Menu items
    strategies.append(
        ("role-menuitem", lambda t=target: page.get_by_role("menuitem", name=t, exact=False))
    )

    # Headings
    strategies.append(
        ("role-heading", lambda t=target: page.get_by_role("heading", name=t, exact=False))
    )

    # ================================================================
    # Text-based strategies (lower priority — more ambiguous)
    # ================================================================

    # Exact text match
    strategies.append(
        ("text-exact", lambda t=target: page.get_by_text(t, exact=True))
    )

    # Partial text match
    strategies.append(
        ("text-partial", lambda t=target: page.get_by_text(t, exact=False))
    )

    # ================================================================
    # Dropdown/select strategies
    # ================================================================
    if any(kw in ctx_lower for kw in ["dropdown", "select", "option"]):
        strategies.insert(0,
            ("select-option", lambda t=target: page.locator(f"select:has(option:has-text('{t}'))"))
        )

    # ================================================================
    # Keyword-based strategies for multi-word descriptive targets
    # (e.g., inferred targets like "School Design Template")
    # ================================================================
    target_words = [w for w in target_lower.split() if len(w) > 3 and w not in (
        "the", "this", "that", "from", "with", "your", "into", "each",
        "page", "pages", "course", "courses",
    )]
    if len(target_words) >= 2 and not target_bold_check(target, page):
        # Try matching significant keywords in visible elements
        for word in target_words[:3]:
            strategies.append((
                f"keyword-{word}",
                lambda w=word: page.locator(
                    f"button:has-text('{w}'):visible, "
                    f"a:has-text('{w}'):visible, "
                    f"span:has-text('{w}'):visible, "
                    f"div.tva-menu-item:has-text('{w}'):visible, "
                    f"h3:has-text('{w}'):visible, "
                    f"h4:has-text('{w}'):visible"
                )
            ))

    # ================================================================
    # UI section selectors for TA-specific terms
    # ================================================================
    _ta_section_map = {
        "design": ".tva-menu .tva-menu-item:has-text('Design')",
        "template": ".tva-menu .tva-menu-item:has-text('Design')",
        "branding": ".tva-menu .tva-menu-item:has-text('Design')",
        "typography": ".tva-menu .tva-menu-item:has-text('Design')",
        "layout": ".tva-menu .tva-menu-item:has-text('Design')",
        "product": ".tva-menu .tva-menu-item:has-text('Products')",
        "payment": ".tva-menu .tva-menu-item:has-text('Products')",
        "member": ".tva-menu .tva-menu-item:has-text('Members')",
        "report": ".tva-menu .tva-menu-item:has-text('Reports')",
        "drip": ".tva-tab-title:has-text('Drip')",
        "access restriction": ".tva-tab-title:has-text('Access restrictions')",
    }
    for keyword, selector in _ta_section_map.items():
        if keyword in target_lower:
            strategies.append((
                f"ta-section-{keyword}",
                lambda sel=selector: page.locator(sel)
            ))

    return strategies


def target_bold_check(target: str, page) -> bool:
    """Quick check if this target is a known bold UI element (not inferred).
    Returns True if it matches a known bold pattern."""
    # Known bold targets are typically short (1-3 words) and Title Case
    words = target.split()
    if len(words) <= 3 and target[0].isupper():
        return True
    return False


def scroll_to_element(page: Page, locator: Locator) -> None:
    """Scroll element into view, centered in viewport if possible."""
    try:
        locator.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
    except Exception:
        pass
