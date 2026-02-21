"""WordPress client for documentation management using browser automation.

Uses Playwright for login (browser-based auth) and then interacts with
WordPress via:
1. REST API using session cookies (extracted from the browser)
2. Direct browser automation for operations that need it

This avoids the need for Application Passwords — you just need WP_URL,
WP_USERNAME, and WP_PASSWORD from your .env file.

Dependencies: playwright, requests, markdown (optional)
"""

import json
import mimetypes
import os
import re
from typing import Dict, List, Optional, Tuple

import requests

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
except ImportError:
    sync_playwright = None

try:
    import markdown as _md_lib
except ImportError:
    _md_lib = None

from lib.wp_types import WPCategory, WPMedia, WPPost


class WordPressClient:
    """WordPress client using browser-based authentication.

    Launches a Playwright browser, logs in to WordPress, extracts session
    cookies, and uses them for REST API calls. The browser stays open for
    operations that need direct page interaction.
    """

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        headless: bool = True,
        post_type: str = "auto",
    ):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.headless = headless
        self.api_base = f"{self.base_url}/wp-json/wp/v2"

        # Playwright objects (initialized on login)
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

        # Requests session (populated after login with cookies)
        self.session = requests.Session()

        # State
        self._logged_in = False
        self.post_type = post_type  # Resolved after login

    # ------------------------------------------------------------------
    # Login / Connection
    # ------------------------------------------------------------------

    def login(self) -> None:
        """Log in to WordPress via the browser and extract session cookies.

        Supports 2FA: if the login lands on a 2FA page (not wp-admin),
        the browser is shown visibly and the script pauses so you can
        complete the 2FA challenge manually. Once you're in wp-admin,
        press Enter in the terminal to continue.
        """
        if not sync_playwright:
            raise ImportError("playwright is required. Install it with: pip install playwright && playwright install chromium")

        print(f"Launching browser and logging into {self.base_url}...")
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context(
            viewport={"width": 1280, "height": 800},
        )
        self._page = self._context.new_page()

        login_url = f"{self.base_url}/wp-login.php"
        self._page.goto(login_url)

        # Handle Pantheon Sandbox Notice (from capture_screenshots.py pattern)
        try:
            if "Sandbox Environment Notice" in self._page.title() or self._page.locator(".pds-button").count() > 0:
                print("Detected Pantheon Sandbox Notice. Clicking Continue...")
                self._page.click(".pds-button")
                self._page.wait_for_load_state("networkidle")
        except Exception:
            pass

        # Handle Cloudflare Turnstile / bot verification
        # Wait for the login form to appear (Cloudflare may show a challenge first)
        login_form_visible = self._page.locator("#user_login").count() > 0
        if not login_form_visible:
            title = self._page.title()
            if "moment" in title.lower() or "cloudflare" in title.lower() or "verify" in title.lower():
                print("Cloudflare verification detected. Waiting for it to complete...")
                if self.headless:
                    # Re-launch visible so user can complete challenge if needed
                    print("Re-launching browser in visible mode for Cloudflare challenge...")
                    self._browser.close()
                    self._browser = self._playwright.chromium.launch(headless=False)
                    self._context = self._browser.new_context(
                        viewport={"width": 1280, "height": 800},
                    )
                    self._page = self._context.new_page()
                    self._page.goto(login_url, wait_until="load")

                # Wait up to 60s for the login form to appear
                try:
                    self._page.locator("#user_login").wait_for(state="visible", timeout=60000)
                    print("Cloudflare challenge passed!")
                except Exception:
                    print("Waiting for you to complete the Cloudflare challenge...")
                    self._page.locator("#user_login").wait_for(state="visible", timeout=300000)

        self._page.fill("#user_login", self.username)
        self._page.fill("#user_pass", self.password)
        self._page.click("#wp-submit")
        try:
            self._page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            self._page.wait_for_timeout(3000)  # fallback: just wait 3s

        # Check if we landed on wp-admin or a 2FA / intermediate page
        if "wp-admin" not in self._page.url and "admin.php" not in self._page.url:
            # Likely a 2FA prompt — wait for the user to complete it
            print("\n" + "=" * 50)
            print("  2FA / additional authentication detected!")
            print("  Please complete the login in the browser window.")
            print("  The browser should be visible on your screen.")
            print("=" * 50)

            if self.headless:
                # Re-launch in visible mode so the user can interact
                print("Re-launching browser in visible mode for 2FA...")
                self._browser.close()
                self._browser = self._playwright.chromium.launch(headless=False)
                self._context = self._browser.new_context(
                    viewport={"width": 1280, "height": 800},
                )
                self._page = self._context.new_page()
                self._page.goto(login_url)
                self._page.wait_for_load_state("networkidle")

                # Re-enter credentials
                try:
                    self._page.fill("#user_login", self.username)
                    self._page.fill("#user_pass", self.password)
                    self._page.click("#wp-submit")
                    self._page.wait_for_load_state("networkidle")
                except Exception:
                    pass

            # Poll until the user completes 2FA and lands on wp-admin
            print("\nWaiting for you to complete 2FA...")
            print("(The script will auto-detect when you reach the dashboard)\n")
            max_wait = 300  # 5 minutes max
            waited = 0
            while waited < max_wait:
                current_url = self._page.url
                if "wp-admin" in current_url or "admin.php" in current_url:
                    break
                self._page.wait_for_timeout(2000)
                waited += 2

            if "wp-admin" not in self._page.url and "admin.php" not in self._page.url:
                raise RuntimeError(
                    f"Login timed out after {max_wait}s. Current URL: {self._page.url}"
                )

        print("Login successful.")
        self._logged_in = True

        # Extract cookies and populate the requests session
        self._sync_cookies()

        # Discover post type if needed
        if self.post_type == "auto":
            self.post_type = self._discover_post_type()

    def _sync_cookies(self) -> None:
        """Copy browser cookies to the requests session for API calls."""
        cookies = self._context.cookies()
        for cookie in cookies:
            self.session.cookies.set(
                cookie["name"],
                cookie["value"],
                domain=cookie.get("domain", ""),
                path=cookie.get("path", "/"),
            )
        # Also get the nonce for authenticated REST API calls
        self._nonce = self._page.evaluate(
            "() => typeof wpApiSettings !== 'undefined' ? wpApiSettings.nonce : ''"
        )
        if self._nonce:
            self.session.headers.update({"X-WP-Nonce": self._nonce})
        else:
            # Try fetching nonce from the admin page
            self._page.goto(f"{self.base_url}/wp-admin/")
            self._page.wait_for_load_state("networkidle")
            self._nonce = self._page.evaluate(
                "() => typeof wpApiSettings !== 'undefined' ? wpApiSettings.nonce : ''"
            )
            if self._nonce:
                self.session.headers.update({"X-WP-Nonce": self._nonce})
            else:
                print("Warning: Could not extract WP REST nonce. Some API calls may fail.")

    def _ensure_logged_in(self) -> None:
        """Ensure we have an active session."""
        if not self._logged_in:
            self.login()

    def close(self) -> None:
        """Close the browser and clean up."""
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        self._logged_in = False
        print("Browser closed.")

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ------------------------------------------------------------------
    # Connection test
    # ------------------------------------------------------------------

    def test_connection(self) -> dict:
        """Test API connection and return site info."""
        self._ensure_logged_in()
        resp = self.session.get(f"{self.base_url}/wp-json/")
        resp.raise_for_status()
        data = resp.json()
        return {
            "name": data.get("name", ""),
            "url": data.get("url", ""),
            "description": data.get("description", ""),
            "namespaces": data.get("namespaces", []),
            "authenticated": bool(self._nonce),
        }

    def _discover_post_type(self) -> str:
        """Auto-detect the custom post type used for documentation."""
        try:
            resp = self.session.get(f"{self.api_base}/types")
            resp.raise_for_status()
            types = resp.json()

            candidates = ["docs", "knowledge-base", "kb", "documentation", "doc"]
            for candidate in candidates:
                if candidate in types:
                    print(f"Discovered docs post type: {candidate}")
                    return candidate

            for name in types:
                if "doc" in name.lower() or "knowledge" in name.lower():
                    print(f"Discovered docs post type: {name}")
                    return name

            print("Warning: Could not discover docs post type. Defaulting to 'posts'.")
            return "posts"
        except Exception as e:
            print(f"Warning: Post type discovery failed ({e}). Defaulting to 'posts'.")
            return "posts"

    # ------------------------------------------------------------------
    # Fetching (REST API with cookie auth)
    # ------------------------------------------------------------------

    def _endpoint(self, post_type: Optional[str] = None) -> str:
        pt = post_type or self.post_type
        return f"{self.api_base}/{pt}"

    def get_posts(
        self,
        post_type: Optional[str] = None,
        per_page: int = 100,
        status: str = "any",
        **kwargs,
    ) -> List[WPPost]:
        """Fetch all posts of the given type with pagination."""
        self._ensure_logged_in()
        endpoint = self._endpoint(post_type)
        all_posts = []
        page = 1

        while True:
            params = {"per_page": per_page, "page": page, "status": status, **kwargs}
            resp = self.session.get(endpoint, params=params)
            if resp.status_code == 400:
                break
            resp.raise_for_status()
            data = resp.json()
            if not data:
                break

            for item in data:
                all_posts.append(self._to_wp_post(item))

            total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
            if page >= total_pages:
                break
            page += 1

        return all_posts

    def get_post(self, post_id: int, post_type: Optional[str] = None) -> WPPost:
        """Fetch a single post by ID."""
        self._ensure_logged_in()
        endpoint = f"{self._endpoint(post_type)}/{post_id}"
        resp = self.session.get(endpoint)
        resp.raise_for_status()
        return self._to_wp_post(resp.json())

    def get_post_by_slug(self, slug: str, post_type: Optional[str] = None) -> Optional[WPPost]:
        """Fetch a post by its URL slug."""
        self._ensure_logged_in()
        endpoint = self._endpoint(post_type)
        resp = self.session.get(endpoint, params={"slug": slug, "status": "any"})
        resp.raise_for_status()
        data = resp.json()
        if data:
            return self._to_wp_post(data[0])
        return None

    # ------------------------------------------------------------------
    # Publishing
    # ------------------------------------------------------------------

    def create_post(
        self,
        title: str,
        content: str,
        slug: str = "",
        status: str = "draft",
        categories: Optional[List[int]] = None,
        post_type: Optional[str] = None,
        meta: Optional[dict] = None,
    ) -> WPPost:
        """Create a new post/doc."""
        self._ensure_logged_in()
        endpoint = self._endpoint(post_type)
        payload = {
            "title": title,
            "content": content,
            "status": status,
        }
        if slug:
            payload["slug"] = slug
        if categories:
            payload["categories"] = categories
        if meta:
            payload["meta"] = meta

        resp = self.session.post(endpoint, json=payload)
        resp.raise_for_status()
        return self._to_wp_post(resp.json())

    def update_post(self, post_id: int, post_type: Optional[str] = None, **fields) -> WPPost:
        """Update an existing post."""
        self._ensure_logged_in()
        endpoint = f"{self._endpoint(post_type)}/{post_id}"
        resp = self.session.post(endpoint, json=fields)
        resp.raise_for_status()
        return self._to_wp_post(resp.json())

    # ------------------------------------------------------------------
    # Media
    # ------------------------------------------------------------------

    def upload_media(self, file_path: str, alt_text: str = "") -> WPMedia:
        """Upload an image/media file and return attachment data."""
        self._ensure_logged_in()
        filename = os.path.basename(file_path)
        mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

        with open(file_path, "rb") as f:
            # For media uploads, use multipart form instead of JSON
            resp = self.session.post(
                f"{self.api_base}/media",
                files={"file": (filename, f, mime_type)},
                headers={"Content-Disposition": f'attachment; filename="{filename}"'},
            )
        resp.raise_for_status()
        data = resp.json()

        media = WPMedia(
            id=data.get("id"),
            source_url=data.get("source_url", ""),
            alt_text=data.get("alt_text", ""),
            title=data.get("title", {}).get("rendered", ""),
            mime_type=data.get("mime_type", ""),
        )

        if alt_text and media.id:
            self.session.post(
                f"{self.api_base}/media/{media.id}",
                json={"alt_text": alt_text},
            )
            media.alt_text = alt_text

        return media

    # ------------------------------------------------------------------
    # Categories / Taxonomies
    # ------------------------------------------------------------------

    def get_categories(self, taxonomy: str = "category", per_page: int = 100) -> List[WPCategory]:
        """Fetch all categories for a taxonomy."""
        self._ensure_logged_in()
        endpoint = f"{self.api_base}/{taxonomy}"
        all_cats = []
        page = 1

        while True:
            resp = self.session.get(endpoint, params={"per_page": per_page, "page": page})
            if resp.status_code == 400:
                break
            resp.raise_for_status()
            data = resp.json()
            if not data:
                break

            for item in data:
                all_cats.append(WPCategory(
                    id=item.get("id"),
                    name=item.get("name", ""),
                    slug=item.get("slug", ""),
                    parent=item.get("parent", 0),
                    count=item.get("count", 0),
                    taxonomy=taxonomy,
                ))

            total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
            if page >= total_pages:
                break
            page += 1

        return all_cats

    def create_category(
        self,
        name: str,
        slug: str = "",
        parent: int = 0,
        taxonomy: str = "category",
    ) -> WPCategory:
        """Create a category if it doesn't exist."""
        self._ensure_logged_in()
        endpoint = f"{self.api_base}/{taxonomy}"

        existing = self.session.get(endpoint, params={"slug": slug or _slugify(name)})
        if existing.status_code == 200:
            data = existing.json()
            if data:
                return WPCategory(
                    id=data[0]["id"],
                    name=data[0]["name"],
                    slug=data[0]["slug"],
                    parent=data[0].get("parent", 0),
                    count=data[0].get("count", 0),
                    taxonomy=taxonomy,
                )

        payload = {"name": name, "parent": parent}
        if slug:
            payload["slug"] = slug
        resp = self.session.post(endpoint, json=payload)
        resp.raise_for_status()
        item = resp.json()
        return WPCategory(
            id=item.get("id"),
            name=item.get("name", ""),
            slug=item.get("slug", ""),
            parent=item.get("parent", 0),
            taxonomy=taxonomy,
        )

    def ensure_category_structure(
        self,
        categories: List[dict],
        taxonomy: str = "category",
    ) -> Dict[str, int]:
        """Create the full category hierarchy.

        Args:
            categories: List of dicts with 'name', 'slug', and optional 'parent_slug'.
            taxonomy: WordPress taxonomy name.

        Returns:
            Mapping of slug -> category ID.
        """
        slug_to_id = {}

        for cat in categories:
            if not cat.get("parent_slug"):
                result = self.create_category(
                    name=cat["name"],
                    slug=cat.get("slug", ""),
                    taxonomy=taxonomy,
                )
                slug_to_id[result.slug] = result.id

        for cat in categories:
            parent_slug = cat.get("parent_slug", "")
            if parent_slug and parent_slug in slug_to_id:
                result = self.create_category(
                    name=cat["name"],
                    slug=cat.get("slug", ""),
                    parent=slug_to_id[parent_slug],
                    taxonomy=taxonomy,
                )
                slug_to_id[result.slug] = result.id

        return slug_to_id

    # ------------------------------------------------------------------
    # Redirects (via Redirection plugin)
    # ------------------------------------------------------------------

    def create_redirect(self, old_url: str, new_url: str, group_id: int = 1) -> Optional[dict]:
        """Create a redirect via the Redirection plugin REST API."""
        self._ensure_logged_in()
        endpoint = f"{self.base_url}/wp-json/redirection/v1/redirect"
        payload = {
            "url": old_url,
            "action_data": {"url": new_url},
            "action_type": "url",
            "action_code": 301,
            "match_type": "url",
            "group_id": group_id,
        }
        try:
            resp = self.session.post(endpoint, json=payload)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError:
            return None

    # ------------------------------------------------------------------
    # Browser-based operations
    # ------------------------------------------------------------------

    @property
    def page(self) -> Page:
        """Access the Playwright page for direct browser automation."""
        self._ensure_logged_in()
        return self._page

    def navigate_to(self, path: str) -> None:
        """Navigate the browser to a path on the WP site."""
        self._ensure_logged_in()
        url = path if path.startswith("http") else f"{self.base_url}/{path.lstrip('/')}"
        self._page.goto(url)
        self._page.wait_for_load_state("networkidle")

    def get_page_content(self, path: str) -> str:
        """Navigate to a page and return its text content."""
        self.navigate_to(path)
        return self._page.inner_text("body")

    def screenshot(self, path: str, output_path: str, full_page: bool = False) -> str:
        """Take a screenshot of a page."""
        self.navigate_to(path)
        self._page.screenshot(path=output_path, full_page=full_page)
        return output_path

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to WordPress-compatible HTML."""
        if _md_lib:
            return _md_lib.markdown(
                markdown_content,
                extensions=["tables", "fenced_code", "nl2br"],
            )

        # Fallback: minimal regex-based conversion
        html = markdown_content
        for level in range(6, 0, -1):
            pattern = r"^{} (.+)$".format("#" * level)
            html = re.sub(pattern, rf"<h{level}>\1</h{level}>", html, flags=re.MULTILINE)
        html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)
        html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)
        html = re.sub(r"!\[(.+?)\]\((.+?)\)", r'<img src="\2" alt="\1" />', html)
        html = re.sub(r"\n\n", "</p>\n<p>", html)
        return f"<p>{html}</p>"

    @staticmethod
    def _to_wp_post(data: dict) -> WPPost:
        return WPPost(
            id=data.get("id"),
            title=data.get("title", {}).get("rendered", ""),
            slug=data.get("slug", ""),
            content=data.get("content", {}).get("rendered", ""),
            status=data.get("status", ""),
            categories=data.get("categories", []),
            meta=data.get("meta", {}),
            link=data.get("link", ""),
            excerpt=data.get("excerpt", {}).get("rendered", ""),
        )


def _slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    return text.strip("-")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    from lib.config import AgentConfig

    parser = argparse.ArgumentParser(description="WordPress browser-based client.")
    parser.add_argument("--test", action="store_true", help="Test connection and show site info.")
    parser.add_argument("--list-posts", action="store_true", help="List all docs.")
    parser.add_argument("--list-categories", action="store_true", help="List doc categories.")
    parser.add_argument("--taxonomy", default="category", help="Taxonomy for categories.")
    parser.add_argument("--no-headless", action="store_true", help="Show the browser window.")
    args = parser.parse_args()

    config = AgentConfig.from_env()
    if not config.wp_url or not config.wp_username or not config.wp_password:
        print("Error: Set WP_URL, WP_USERNAME, and WP_PASSWORD in .env")
        return

    with WordPressClient(
        base_url=config.wp_url,
        username=config.wp_username,
        password=config.wp_password,
        headless=not args.no_headless,
    ) as client:
        if args.test:
            info = client.test_connection()
            print(f"Connected to: {info['name']}")
            print(f"URL: {info['url']}")
            print(f"Post type: {client.post_type}")
            print(f"Authenticated: {info['authenticated']}")

        if args.list_posts:
            posts = client.get_posts()
            print(f"\n{len(posts)} docs found:")
            for p in posts:
                print(f"  [{p.id}] {p.title} ({p.status}) - /{p.slug}/")

        if args.list_categories:
            cats = client.get_categories(taxonomy=args.taxonomy)
            print(f"\n{len(cats)} categories ({args.taxonomy}):")
            for c in cats:
                parent_label = f" (parent: {c.parent})" if c.parent else ""
                print(f"  [{c.id}] {c.name} ({c.count} docs){parent_label}")


if __name__ == "__main__":
    main()
