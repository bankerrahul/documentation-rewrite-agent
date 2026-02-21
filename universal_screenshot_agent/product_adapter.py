"""
Product Adapter — abstract base class for product-specific screenshot automation.

Each web product provides an adapter that implements product-specific navigation,
element finding, modal handling, and publishing logic.

The GenericWebAppAdapter provides config-driven defaults that work for simple
web apps without needing custom code.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Callable
from playwright.sync_api import Page, Locator


class ProductAdapter(ABC):
    """Abstract base class for product-specific screenshot automation."""

    def __init__(self, config: dict):
        """Initialize with parsed config.yaml dict."""
        self.config = config
        self.product_name = config["product"]["name"]
        self.product_slug = config["product"]["slug"]
        self._prev_context = ""

    # ─── Site & Auth ───

    def get_local_url(self) -> str:
        """Return the local site base URL."""
        return self.config["local_site"]["url"].rstrip("/")

    def get_admin_entry_url(self) -> str:
        """Return the full URL to the product's admin page."""
        base = self.get_local_url()
        entry = self.config["local_site"]["admin_entry"]
        return f"{base}{entry}"

    def get_login_url(self) -> str:
        """Return the login URL."""
        base = self.get_local_url()
        path = self.config.get("local_site", {}).get("login_path", "/wp-login.php")
        return f"{base}{path}"

    def get_browser_config(self) -> dict:
        """Return browser settings."""
        defaults = {
            "viewport_width": 1280,
            "viewport_height": 800,
            "scale_factor": 2,
            "spa_load_delay_ms": 2000,
        }
        defaults.update(self.config.get("browser", {}))
        return defaults

    def get_layout_config(self) -> dict:
        """Return layout constants for annotation positioning."""
        defaults = {
            "sidebar_width_css": 100,
            "wp_sidebar_width_css": 160,
            "toolbar_height_css": 32,
        }
        defaults.update(self.config.get("layout", {}))
        return defaults

    # ─── Login ───

    def login(self, page: Page, username: str, password: str) -> None:
        """Log into the site. Default: WordPress standard login."""
        auth = self.config.get("auth", {})
        login_url = self.get_login_url()
        
        username_field = auth.get("username_field", "#user_login")
        password_field = auth.get("password_field", "#user_pass")
        submit_button = auth.get("submit_button", "#wp-submit")
        success_indicator = auth.get("success_indicator", "wp-admin")
        
        print(f"  Logging into {self.get_local_url()}...")
        page.goto(login_url)
        page.fill(username_field, username)
        page.fill(password_field, password)
        page.click(submit_button)
        page.wait_for_load_state("networkidle")
        
        if success_indicator in page.url:
            print("  Login successful.")
        else:
            raise RuntimeError(f"Login failed. Current URL: {page.url}")

    # ─── Navigation ───

    @abstractmethod
    def navigate_to_app(self, page: Page) -> None:
        """Navigate to the product's main admin page and wait for it to load."""
        ...

    @abstractmethod
    def navigate_to_section(
        self, page: Page, heading: str,
        steps: list = None, prev_context: str = ""
    ) -> None:
        """Navigate to the appropriate page/tab for a documentation section heading.
        
        Args:
            page: Playwright page
            heading: Section heading text (e.g., "Creating Your First Course")
            steps: List of steps in this section (for lookahead)
            prev_context: Context string from the previous section
        """
        ...

    def get_section_context(self, heading: str) -> str:
        """Map a section heading to a context string using config rules.
        
        Checks heading text against keyword lists in config['section_contexts'].
        Returns the matching context string, or 'default' if no match.
        """
        heading_lower = heading.lower()
        contexts = self.config.get("section_contexts", [])
        
        for ctx_rule in contexts:
            keywords = ctx_rule.get("keywords", [])
            context_name = ctx_rule.get("context", "default")
            for kw in keywords:
                if kw.lower() in heading_lower:
                    return context_name
        
        # Return the last context entry as default (if it has empty keywords)
        for ctx_rule in reversed(contexts):
            if not ctx_rule.get("keywords"):
                return ctx_rule.get("context", "default")
        
        return "default"

    # ─── Tab Management ───

    def ensure_correct_tab(self, page: Page, step: Dict) -> None:
        """Switch tabs if necessary before element search.
        
        Default: no-op. Override in product adapters that have tab-based UIs.
        """
        pass

    # ─── Element Finding ───

    def get_element_strategies(
        self, page: Page, target: str, context: str, action: str
    ) -> List[Tuple[str, Callable]]:
        """Return product-specific element-finding strategies.
        
        These are prepended to the generic strategies in element_finder.py.
        Each strategy is a (name, callable) tuple where callable returns a Locator or None.
        
        Default: build strategies from config selectors.
        Override for complex product-specific logic.
        """
        return self._build_config_strategies(page, target, context, action)

    def _build_config_strategies(
        self, page: Page, target: str, context: str, action: str
    ) -> List[Tuple[str, Callable]]:
        """Build element-finding strategies from config selectors.
        
        Reads self.config['selectors'] and generates Playwright locators.
        """
        strategies = []
        selectors = self.config.get("selectors", {})
        target_lower = target.lower()
        
        # Sidebar navigation items
        sidebar = selectors.get("sidebar", {})
        known_items = [x.lower() for x in sidebar.get("known_items", [])]
        if target_lower in known_items:
            template = sidebar.get("item_template", "")
            if template:
                sel = template.replace("{text}", target)
                strategies.append((
                    f"config-sidebar-{target_lower}",
                    lambda s=sel: page.locator(s).first
                ))
        
        # WP admin menu items
        wp_admin = selectors.get("wp_admin", {})
        wp_items = [x.lower() for x in wp_admin.get("known_items", [])]
        if target_lower in wp_items:
            template = wp_admin.get("menu", "")
            if template:
                sel = template.replace("{text}", target)
                strategies.append((
                    f"config-wp-menu-{target_lower}",
                    lambda s=sel: page.locator(s).first
                ))
        
        # Action buttons (Add Module, Add Lesson, etc.)
        action_btns = selectors.get("action_buttons", {})
        type_map = action_btns.get("type_map", {})
        if target_lower in type_map:
            item_type = type_map[target_lower]
            template = action_btns.get("add_item_selector", "")
            if template:
                sel = template.replace("{type}", item_type)
                strategies.append((
                    f"config-action-btn-{item_type}",
                    lambda s=sel: page.locator(s).first
                ))
        
        return strategies

    # ─── Modal Handling ───

    def is_modal_open(self, page: Page) -> bool:
        """Check if a product-specific modal is open.
        
        Default: check config selectors.modals.overlay
        """
        selectors = self.config.get("selectors", {}).get("modals", {})
        overlay_sel = selectors.get("overlay", "")
        if not overlay_sel:
            return False
        try:
            loc = page.locator(overlay_sel)
            return loc.count() > 0 and loc.first.is_visible(timeout=500)
        except Exception:
            return False

    def dismiss_modal(self, page: Page) -> bool:
        """Dismiss an open modal. Returns True if a modal was dismissed.
        
        Default: try close button, then X button from config.
        """
        selectors = self.config.get("selectors", {}).get("modals", {})
        
        for key in ["close_button", "x_button"]:
            sel = selectors.get(key, "")
            if not sel:
                continue
            try:
                # Handle multi-line selector strings (comma-separated alternatives)
                loc = page.locator(sel.strip())
                if loc.count() > 0 and loc.first.is_visible(timeout=500):
                    loc.first.click()
                    page.wait_for_timeout(500)
                    return True
            except Exception:
                continue
        return False

    def advance_modal(self, page: Page, target: str) -> None:
        """Advance a multi-step modal wizard to the form step.
        
        Default: no-op. Override in product adapters with complex modal wizards.
        """
        pass

    def is_element_behind_modal(self, page: Page, locator: Locator) -> bool:
        """Check if an element is behind a modal overlay.
        
        Default: check if modal is open.
        """
        return self.is_modal_open(page)

    # ─── Post-Action Hooks ───

    def post_action_hook(self, page: Page, step: Dict, action: str) -> None:
        """Product-specific logic after executing a step action.
        
        Default: no-op. Override for things like:
        - Saving after typing in a modal
        - Entering a course after navigating
        - Advancing modal wizard after clicking a button
        """
        pass

    # ─── Sample Text ───

    def get_sample_text(self, step: Dict) -> str:
        """Generate sample text for 'type' actions.
        
        Default: look up target in config['sample_text'], fall back to generic text.
        """
        target_lower = step.get("target", "").lower()
        sample_map = self.config.get("sample_text", {})
        
        # Exact match
        if target_lower in sample_map:
            return sample_map[target_lower]
        
        # Partial match
        for key, value in sample_map.items():
            if key in target_lower or target_lower in key:
                return value
        
        # Generic fallback
        if "url" in target_lower:
            return "https://example.com"
        if "email" in target_lower:
            return "student@example.com"
        if "name" in target_lower or "title" in target_lower:
            return "Sample Title"
        
        return "Sample text"

    # ─── Publishing ───

    def get_articles(self) -> List[Dict]:
        """Return list of article dicts with 'slug' and optional 'post_id' keys."""
        return self.config.get("articles", [])

    def get_post_type(self) -> str:
        """Return the WP REST API post type (e.g., 'ht-kb', 'posts')."""
        return self.config.get("production_site", {}).get("post_type", "posts")

    def get_production_url(self) -> str:
        """Return the production site URL."""
        return self.config.get("production_site", {}).get("url", "")

    def get_taxonomy(self) -> str:
        """Return the taxonomy name for categorization."""
        return self.config.get("production_site", {}).get("taxonomy", "category")

    def get_alt_text_suffix(self) -> str:
        """Return suffix for image alt text (e.g., 'in My Product')."""
        return f"in {self.product_name}"

    def get_seo_config(self) -> dict:
        """Return SEO configuration from config.yaml.

        Returns dict with optional keys:
            brand_suffix: str — appended to SEO titles (e.g., " - Thrive Themes")
            default_keyphrases: list[str] — keyphrases added to every article
        """
        return self.config.get("seo", {})

    def get_categories_for_article(self, filename: str) -> List[int]:
        """Return category IDs for an article based on config mappings."""
        cats_config = self.config.get("categories", {})
        
        # Check overrides first
        overrides = cats_config.get("overrides", {})
        if filename in overrides:
            return overrides[filename]
        
        # Check prefix map
        prefix_map = cats_config.get("prefix_map", {})
        for prefix, cat_ids in prefix_map.items():
            if filename.startswith(prefix):
                return cat_ids
        
        return []


class GenericWebAppAdapter(ProductAdapter):
    """Default adapter — config-driven only, no hardcoded logic.
    
    Works for any web app with standard HTML roles and text-based elements.
    All behavior is driven by config.yaml selectors and navigation flows.
    
    For products with complex UIs (multi-step modals, SPA tab switching),
    extend this class in products/{slug}/adapter.py.
    """

    def navigate_to_app(self, page: Page) -> None:
        """Navigate to the product's admin page using config URL."""
        url = self.get_admin_entry_url()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        delay = self.get_browser_config().get("spa_load_delay_ms", 2000)
        page.wait_for_timeout(delay)

    def navigate_to_section(
        self, page: Page, heading: str,
        steps: list = None, prev_context: str = ""
    ) -> None:
        """Navigate to section using config-driven navigation flows.
        
        Determines the section context from heading keywords,
        then executes the action sequence defined in navigation_flows.
        """
        context = self.get_section_context(heading)
        
        # Skip re-navigation if same context as previous section
        if context == prev_context:
            print(f"    [Same context '{context}' — skipping re-navigation]")
            return
        
        self._prev_context = context
        
        flows = self.config.get("navigation_flows", {})
        flow = flows.get(context)
        
        if not flow:
            print(f"    [No navigation flow for context '{context}']")
            return
        
        # Check if this flow requires the app to be loaded
        if flow.get("requires_app"):
            self.navigate_to_app(page)
        
        # Execute action sequence
        actions = flow.get("actions", [])
        for action_def in actions:
            self._execute_nav_action(page, action_def)
        
        print(f"    [Navigated to context: {context}]")

    def _execute_nav_action(self, page: Page, action_def: dict) -> None:
        """Execute a single navigation action from config."""
        if "goto" in action_def:
            url = action_def["goto"]
            # Interpolate local_site.url if referenced
            url = url.replace("${local_site.url}", self.get_local_url())
            page.goto(url)
            wait_state = action_def.get("wait", "networkidle")
            page.wait_for_load_state(wait_state)
        
        elif "click" in action_def:
            selector = action_def["click"]
            try:
                loc = page.locator(selector)
                if loc.count() > 0 and loc.first.is_visible(timeout=3000):
                    loc.first.click()
                else:
                    print(f"      [Nav action: '{selector}' not found/visible]")
            except Exception as e:
                print(f"      [Nav action click failed: {e}]")
        
        elif "click_first" in action_def:
            # Try multiple selectors, click the first visible one
            selectors = action_def["click_first"]
            clicked = False
            for sel in selectors:
                try:
                    loc = page.locator(sel)
                    if loc.count() > 0 and loc.first.is_visible(timeout=2000):
                        loc.first.click()
                        clicked = True
                        break
                except Exception:
                    continue
            if not clicked:
                print(f"      [Nav action: none of {selectors} found]")
        
        # Wait after action
        wait_ms = action_def.get("wait_ms", 0)
        if wait_ms:
            page.wait_for_timeout(wait_ms)
