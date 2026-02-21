# Universal Screenshot Agent

Automated screenshot capture and annotation pipeline for product documentation. Point it at any web app's admin panel, give it markdown docs with step-by-step instructions, and it captures annotated screenshots with red arrows pointing at each UI element.

Works with any WordPress-based product. Includes Thrive Apprentice as a working reference example.

## Quick Start

```bash
# 1. Clone the repo
git clone <repo-url> && cd universal-screenshot-agent

# 2. Create virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -e . && playwright install chromium

# 4. Set up environment
cp .env.example .env
# Edit .env with your local WordPress URL and credentials

# 5. Try it with the included Thrive Apprentice example
screenshot-agent -p thrive_apprentice parse
```

## Prerequisites

- **Python 3.8+**
- **Local WordPress site** with your product installed (for screenshot capture)
- **Chrome browser** (for the publishing step, which uses a WebSocket bridge)

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -e .
playwright install chromium
```

Copy `.env.example` to `.env` and fill in your WordPress credentials:

```
WP_URL=http://your-local-site.local
WP_USERNAME=admin
WP_PASSWORD=yourpassword
```

## Project Structure

```
universal_screenshot_agent/
  run.py                  # CLI entry point
  capture.py              # Playwright screenshot capture engine
  element_finder.py       # Multi-strategy UI element location
  step_parser.py          # Markdown docs -> JSON step specs
  annotate.py             # PIL red-arrow annotation
  product_adapter.py      # ProductAdapter ABC + GenericWebAppAdapter
  config_loader.py        # YAML config loader with env var interpolation
  publisher.py            # WebSocket publisher (upload + inject into posts)

  products/
    _template/            # Copy this to create a new product
      config.yaml         # Configuration template (fully documented)
      adapter.py          # Optional custom adapter skeleton

    thrive_apprentice/    # Working reference example
      config.yaml         # Full TA config (selectors, nav flows, etc.)
      adapter.py          # Custom adapter for Vue.js SPA
      docs/               # 2 sample markdown articles
```

## CLI Commands

All commands require `--product` / `-p` to specify which product to work with.

### List available products

```bash
screenshot-agent list-products
```

### Parse docs into step specs

```bash
# Parse all articles
screenshot-agent -p thrive_apprentice parse

# Parse a single article
screenshot-agent -p thrive_apprentice parse --article 1-01-creating-your-first-course
```

Reads markdown files from `products/{product}/docs/` and generates JSON specs in `products/{product}/specs/`.

### Capture screenshots

```bash
# Capture one article (headless)
screenshot-agent -p thrive_apprentice capture 1-01-creating-your-first-course

# Capture with visible browser (for debugging)
screenshot-agent -p thrive_apprentice capture 1-01-creating-your-first-course --headed

# Capture all articles
screenshot-agent -p thrive_apprentice capture-all
```

Opens a Playwright browser, logs into WordPress, navigates through the product UI, and captures annotated screenshots for each step.

### Publish to production

```bash
screenshot-agent -p thrive_apprentice publish
```

Starts a WebSocket server. Connect from Chrome (on the production site's wp-admin) to upload screenshots and inject them into draft posts.

## Creating a New Product

### Step 1: Copy the template

```bash
cp -r products/_template products/my_product
```

### Step 2: Edit config.yaml

The config file has these key sections:

**Product info:**
```yaml
product:
  name: "My Product"
  slug: "my_product"
```

**Local site (where screenshots are captured):**
```yaml
local_site:
  url: "${WP_URL:-http://my-product.local}"
  admin_entry: "/wp-admin/admin.php?page=my_product"
```

**Browser settings:**
```yaml
browser:
  viewport_width: 1280
  viewport_height: 800
  scale_factor: 2          # 2 for Retina
  spa_load_delay_ms: 2000  # Extra wait for SPA frameworks
```

**Section contexts** — map doc section headings to logical page contexts. Sections with the same context skip re-navigation:
```yaml
section_contexts:
  - context: "settings-page"
    keywords: ["settings", "configuration", "preferences"]
  - context: "main-page"
    keywords: ["getting started", "overview"]
  - context: "default"
    keywords: []  # catch-all
```

**Navigation flows** — define how to reach each context:
```yaml
navigation_flows:
  settings-page:
    requires_app: true
    actions:
      - click: "#settings-link"
        wait_ms: 2000
```

**Selectors** — CSS selectors for product-specific UI elements:
```yaml
selectors:
  sidebar:
    item_template: "nav a:has-text('{text}')"
    known_items: ["Dashboard", "Settings", "Reports"]
  modals:
    overlay: ".modal:visible"
    close_button: "button.close:visible"
```

**Articles** — for publishing:
```yaml
articles:
  - slug: "getting-started"
    post_id: 12345
```

### Step 3: Add documentation files

Place your markdown docs in `products/my_product/docs/`. Each doc should use Gutenberg ordered-list blocks with bold UI element targets:

```markdown
<!-- wp:heading {"level":2} -->
## Getting Started

<!-- wp:list {"ordered":true} -->
<ol>
<li>Navigate to <strong>My Product</strong> in the WordPress sidebar</li>
<li>Click <strong>Add New</strong> to create your first item</li>
<li>Enter a <strong>Title</strong> for your item</li>
</ol>
<!-- /wp:list -->
```

Bold text (`<strong>`) = UI element to find and annotate with an arrow.

### Step 4: Run the pipeline

```bash
screenshot-agent -p my_product parse
screenshot-agent -p my_product capture-all --headed  # Use --headed first to debug
screenshot-agent -p my_product publish
```

## Writing a Custom Adapter

For **simple web apps**, the `GenericWebAppAdapter` + config.yaml is enough. You don't need a custom adapter.

Write a custom `adapter.py` when your product has:
- **SPA navigation** (Vue.js, React) that needs extra wait times or tab switching
- **Multi-step modal wizards** (e.g., type selection -> parent selection -> form)
- **Complex element finding** that can't be expressed as simple CSS selectors in config
- **Post-action hooks** (e.g., saving after typing, entering a course after navigating)

See `products/thrive_apprentice/adapter.py` for a complete example (853 lines) covering all of these patterns.

Your adapter extends `GenericWebAppAdapter` and overrides only what you need:

```python
from universal_screenshot_agent.product_adapter import GenericWebAppAdapter

class MyProductAdapter(GenericWebAppAdapter):
    def navigate_to_section(self, page, heading, steps=None, prev_context=""):
        # Custom navigation logic
        ...

    def get_element_strategies(self, page, target, context, action):
        # Return product-specific CSS selector strategies
        strategies = []
        strategies.append(("my-sidebar", lambda: page.locator(f".my-nav a:has-text('{target}')")))
        return strategies
```

The agent auto-discovers your adapter class when it's in `products/{slug}/adapter.py`.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WP_URL` | `http://localhost` | Local WordPress site URL |
| `WP_USERNAME` | `admin` | WordPress admin username |
| `WP_PASSWORD` | `password` | WordPress admin password |

Set these in `.env` (copied from `.env.example`) or export them in your shell.

## Pipeline Overview

```
Markdown Docs          Step Parser           Playwright            PIL Annotate
  (.md files)    --->  (JSON specs)    --->  (screenshots)   --->  (red arrows)
                                                                        |
                                                                        v
                                                              WebSocket Publisher
                                                              (upload to WP REST API
                                                               + inject into posts)
```

1. **Parse**: `step_parser.py` reads markdown docs and extracts ordered-list steps with bold UI targets into JSON specs
2. **Capture**: `capture.py` opens Playwright, logs in, navigates through the product using the adapter, finds each target element, and takes viewport screenshots
3. **Annotate**: `annotate.py` draws red arrows pointing at the target element on each screenshot
4. **Publish**: `publisher.py` runs a WebSocket server; Chrome (on the production site) connects and uploads images via WP REST API, then injects `<img>` tags into draft post content

## Reference: Thrive Apprentice Example

The `products/thrive_apprentice/` directory is included as a fully working example with:
- `config.yaml` — 430+ lines of TA-specific selectors, navigation flows, and section context mappings
- `adapter.py` — 853-line custom adapter handling Vue.js SPA, multi-step modal wizards, tab switching, and 40+ element-finding strategies
- `docs/` — 2 sample articles to demonstrate the pipeline

This is the most complex adapter possible (Vue.js SPA with custom modal wizards). Most products will need much simpler configs.
