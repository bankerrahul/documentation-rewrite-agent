---
description: Publish rewritten documentation to WordPress via REST API.
---

# WordPress Publishing Workflow

Publish rewritten documentation articles to WordPress, manage categories, and set up redirects.

## Prerequisites

Ensure the following are configured in `knowledge_base/.env`:
```
WP_URL=https://your-site.com
WP_USERNAME=your-username
WP_PASSWORD=your-password
WP_HEADLESS=false
```

**2FA Support:** Set `WP_HEADLESS=false` so the browser window is visible. When you run the client, it will:
1. Open a browser and navigate to `wp-login.php`
2. Fill in your username/password automatically
3. If 2FA is required, pause and wait for you to complete it in the browser
4. Auto-detect when you reach the dashboard (up to 5 minutes)
5. Extract session cookies for API calls

Install Python dependencies:
```bash
cd knowledge_base
pip install -r requirements.txt
playwright install chromium
```

## Phase 1: Connection Test

```bash
cd knowledge_base
python wordpress_client.py --test --no-headless
```

This will:
1. Open a visible browser window
2. Log in (you complete 2FA if prompted)
3. Test the REST API with your session cookies
4. Show site info and discovered post type

## Phase 2: Review Existing State

### List existing docs
```bash
cd knowledge_base
python wordpress_client.py --list-posts
```

### List existing categories
```bash
cd knowledge_base
python wordpress_client.py --list-categories --taxonomy <taxonomy_name>
```

The taxonomy name depends on the theme (common: `category`, `docs_category`, `knowledge-base-category`).

## Phase 3: Category Setup

Read the reorganization plan's proposed category structure. For each new category:

1. Check if it already exists in WordPress
2. Create it via the API if needed
3. Record the category ID mapping

The WordPress client can handle this programmatically:

```python
from wordpress_client import WordPressClient
from lib.config import AgentConfig

config = AgentConfig.from_env()
client = WordPressClient(config.wp_url, config.wp_username, config.wp_app_password)

categories = [
    {"name": "Getting Started", "slug": "getting-started"},
    {"name": "Form Types & Setup", "slug": "form-types-setup"},
    # ...
]
slug_to_id = client.ensure_category_structure(categories, taxonomy="docs_category")
```

## Phase 4: Publish Articles

For each rewritten article in the product's output directory:

### 1. Read the rewritten content
Read `<product>/output/<article_id>/rewritten_doc.md`.

### 2. Convert markdown to HTML
The WordPress client handles this:
```python
html_content = client.markdown_to_html(markdown_content)
```

### 3. Upload images
For each image in `image_mapping.md`:
- Capture the screenshot using the spec
- Upload to WordPress media library
- Replace markdown image references with WordPress media URLs

### 4. Create the post as draft
```python
post = client.create_post(
    title="How to Get Started with Thrive Leads",
    content=html_content,
    slug="how-to-get-started-with-thrive-leads",
    status="draft",
    categories=[category_id],
    meta={"_yoast_wpseo_metadesc": "Learn how to install and activate Thrive Leads..."},
)
print(f"Draft created: {post.link}")
```

### 5. Review the draft
Share the preview link with the user for review.

### 6. Publish (with user approval)
```python
client.update_post(post.id, status="publish")
```

## Phase 5: Set Up Redirects

### Option A: Redirection Plugin (automated)

If the Redirection plugin is installed:
```python
client.create_redirect("/old-article-slug/", "/new-article-slug/")
```

### Option B: .htaccess rules (manual)

Generate rules from the redirect map:
```bash
cd knowledge_base
python redirect_generator.py <PRODUCT>_REORGANIZATION.md --htaccess
```

Copy the generated rules to your server's `.htaccess` file.

### Option C: CSV Import

Use the redirect CSV for bulk import into the Redirection plugin:
```
knowledge_base/<product>/redirect_map.csv
```

## Phase 6: Verification

After publishing:

1. **Check all published URLs** — Visit each article to confirm it loads correctly
2. **Test redirects** — Verify old URLs redirect to new ones with 301 status
3. **Check category pages** — Confirm articles appear under correct categories
4. **Test internal links** — Click through all cross-references between articles
5. **Check SEO metadata** — Verify meta descriptions and titles in page source
6. **Update batch state** — Record WordPress post IDs in `batch_state.json`

## Rollback

If issues are found after publishing:
- Set posts back to `draft` status via the API
- Remove redirects if they're causing problems
- Fix content and re-publish

## Notes

- Always publish as **draft** first, never directly to **publish**
- Get user approval before changing any post from draft to published
- The WordPress client handles pagination for sites with many docs
- Application Passwords are scoped to the user — use an editor/admin account
