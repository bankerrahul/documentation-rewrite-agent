"""
Generic UI element finder for the Universal Screenshot Agent.

Uses a multi-strategy approach to find target elements on any web page.
Product-specific strategies are provided by the ProductAdapter; this module
provides generic strategies that work across all web apps.

Strategy priority:
1. Product adapter strategies (from adapter.get_element_strategies())
2. Form field strategies (for 'type' actions)
3. Toggle/switch strategies (for 'toggle' actions)
4. Generic role-based (Playwright best practices: button, link, tab, etc.)
5. Text-based (exact + partial text matching)
"""

from typing import Optional, List, Tuple, Callable
from playwright.sync_api import Page, Locator


def find_element(
    page: Page,
    target: str,
    context: str = "",
    action: str = "click",
    adapter=None,
) -> Optional[Locator]:
    """Try multiple strategies to find a target UI element on the page.

    Args:
        page: Playwright page.
        target: The UI element text label (e.g., "Save", "Add Course").
        context: Descriptive context (e.g., "left sidebar", "dropdown").
        action: The action type (click, hover, type, etc.).
        adapter: Optional ProductAdapter instance for product-specific strategies.

    Returns:
        A Playwright Locator pointing to the element, or None if not found.
    """
    if not target:
        return None

    strategies = _build_strategies(page, target, context, action, adapter)

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
    page: Page, target: str, context: str, action: str, adapter=None
) -> List[Tuple[str, Callable]]:
    """Build ordered list of (name, fn) strategies to try."""
    ctx_lower = context.lower() if context else ""
    target_lower = target.lower()

    strategies = []

    # ================================================================
    # Product-specific strategies (highest priority)
    # ================================================================
    if adapter is not None:
        product_strategies = adapter.get_element_strategies(page, target, context, action)
        strategies.extend(product_strategies)

    # ================================================================
    # Form field strategies (for 'type' actions)
    # ================================================================
    if action == "type":
        # Input by placeholder text
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
        # ARIA labeled inputs
        strategies.append(
            ("aria-label-input", lambda t=target: page.locator(
                f"input[aria-label*='{t}' i]:visible, "
                f"textarea[aria-label*='{t}' i]:visible"
            ))
        )
        # Playwright get_by_label
        strategies.append(
            ("by-label", lambda t=target: page.get_by_label(t, exact=False))
        )

    # ================================================================
    # Toggle/switch strategies (for 'toggle' actions)
    # ================================================================
    if action == "toggle" or "toggle" in ctx_lower:
        # Toggle near label text
        strategies.append((
            "toggle-near-label", lambda t=target: page.locator(
                f"div:has(> *:has-text('{t}')) input[type='checkbox']:visible, "
                f"label:has-text('{t}') input[type='checkbox'], "
                f"label:has-text('{t}') ~ input[type='checkbox']"
            )
        ))

        # Fallback: just find the text label itself
        strategies.append((
            "toggle-label-text", lambda t=target: page.locator(
                f"span:has-text('{t}'):visible, "
                f"label:has-text('{t}'):visible, "
                f"p:has-text('{t}'):visible"
            )
        ))

        # For multi-word targets, try matching significant keywords
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

    # ================================================================
    # Dropdown/select strategies
    # ================================================================
    if any(kw in ctx_lower for kw in ["dropdown", "select", "option"]):
        strategies.append(
            ("select-option", lambda t=target: page.locator(f"select:has(option:has-text('{t}'))"))
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
    # Keyword-based strategies for multi-word descriptive targets
    # ================================================================
    target_words = [w for w in target_lower.split() if len(w) > 3 and w not in (
        "the", "this", "that", "from", "with", "your", "into", "each",
        "page", "pages",
    )]
    if len(target_words) >= 2 and not _target_bold_check(target):
        for word in target_words[:3]:
            strategies.append((
                f"keyword-{word}",
                lambda w=word: page.locator(
                    f"button:has-text('{w}'):visible, "
                    f"a:has-text('{w}'):visible, "
                    f"span:has-text('{w}'):visible, "
                    f"h3:has-text('{w}'):visible, "
                    f"h4:has-text('{w}'):visible"
                )
            ))

    return strategies


def _target_bold_check(target: str) -> bool:
    """Quick check if this target is a known bold UI element (not inferred).
    Returns True if it matches a known bold pattern."""
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
