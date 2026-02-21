# Documentation Rewrite Agent

An end-to-end documentation pipeline for Thrive Themes products. Rewrites legacy knowledge base articles to match a unified style guide, captures annotated screenshots from a local WordPress site, and publishes finished drafts to production — all driven by AI agents.

## What's Inside

| Component | Purpose |
|-----------|---------|
| **`.agent/workflows/`** | Master orchestration — start here. Guides the agent through rewriting, batch processing, reorganizing, and publishing. |
| **`knowledge_base/`** | Documentation engine — AI-powered article rewriting, batch runner, WordPress client, merge processor, redirect generator, style guides, and all product content. |
| **`universal_screenshot_agent/`** | Screenshot pipeline — parses markdown docs → captures screenshots with Playwright → annotates with red arrows → publishes to WordPress via WebSocket bridge. |

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/bankerrahul/documentation-rewrite-agent.git
cd documentation-rewrite-agent

# 2. Create virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -e . && playwright install chromium

# 4. Set up environment
cp .env.example .env
# Edit .env with your local WordPress URL and credentials

# 5. Try the screenshot agent with the included sample product
screenshot-agent -p thrive_apprentice parse
```

## Prerequisites

- **Python 3.8+**
- **Local WordPress site** with your product installed (for screenshot capture)
- **Chrome browser** (for the publishing step)
- **API key** for Anthropic, OpenAI, or Ollama (for doc rewriting)

## Project Structure

```
documentation_rewrite_agent/
│
├── .agent/workflows/                    # Agent orchestration
│   ├── orchestrator.md                  # Master entry point — start here
│   ├── rewrite_docs.md                  # Single article rewrite workflow
│   ├── batch_process.md                 # Batch processing multiple articles
│   ├── publish_to_wordpress.md          # Publishing workflow
│   └── reorganize_product.md            # Product reorganization planning
│
├── knowledge_base/                      # Documentation engine
│   ├── agent.py                         # Core rewrite agent (Anthropic/OpenAI/Ollama)
│   ├── run_agent.py                     # Single-document CLI processor
│   ├── batch_runner.py                  # Batch processing with state tracking
│   ├── merge_processor.py               # Merge multiple articles into one
│   ├── redirect_generator.py            # Old→new URL redirect CSV generator
│   ├── wordpress_client.py              # WP REST API client (Playwright auth)
│   ├── capture_screenshots.py           # Legacy screenshot capture
│   ├── scan_videos.py                   # Audit articles for embedded videos
│   ├── lib/                             # Config, state management, WP types
│   ├── PILLAR.md                        # Agent persona & documentation standards
│   ├── documentation_master_guide.md    # Primary style reference
│   ├── sop_summary.md                   # SOP for documentation workflow
│   ├── thrive_apprentice/               # TA: rewritten docs, screenshots, batch jobs
│   └── thrive_leads/                    # TL: 15 reorganized docs + redirect map
│
├── universal_screenshot_agent/          # Screenshot pipeline (any WP product)
│   ├── run.py                           # CLI entry point
│   ├── step_parser.py                   # Markdown docs → JSON step specs
│   ├── capture.py                       # Playwright screenshot capture
│   ├── element_finder.py                # Multi-strategy UI element location
│   ├── annotate.py                      # PIL red-arrow annotation
│   ├── product_adapter.py               # ProductAdapter ABC + GenericWebAppAdapter
│   ├── config_loader.py                 # YAML config with env var interpolation
│   ├── publisher.py                     # WebSocket publisher → WP REST API
│   ├── seo_generator.py                # LLM-based SEO metadata generation
│   ├── seo_publisher.py                # WebSocket SEO publisher → AIOSEO REST API
│   └── products/
│       ├── _template/                   # Copy this to create a new product
│       └── thrive_apprentice/           # Working reference (config + Vue.js adapter)
│
├── output/                              # Sample agent output (rewritten doc, review)
├── setup.py                             # pip install -e .
├── requirements.txt                     # Python dependencies
└── .env.example                         # Environment variables template
```

---

## Agent Workflows

The `.agent/workflows/` directory contains markdown guides that orchestrate the full documentation pipeline. Start with **`orchestrator.md`** — it lists all supported Thrive products and offers these actions:

1. **Reorganize** — Restructure a product's knowledge base (merge, split, rename articles)
2. **Rewrite** — Rewrite a single article to match the style guide
3. **Batch rewrite** — Rewrite all articles for a product
4. **Merge** — Combine multiple source articles into one
5. **Generate redirects** — Create old→new URL mapping CSV
6. **Publish** — Push drafts to WordPress
7. **Capture screenshots** — Run the screenshot pipeline
8. **Check status** — View batch progress

### Rewriting a Single Article

The rewrite workflow (`rewrite_docs.md`) produces 4 output files:

| Output | Description |
|--------|-------------|
| `rewritten_doc.md` | The rewritten article matching tone, formatting, and SEO standards |
| `image_mapping.md` | Where to place screenshots in the new article |
| `review.md` | Issues found, improvements made, and editorial notes |
| `screenshot_spec.json` | Spec for the screenshot agent to capture images |

### Batch Processing

`batch_runner.py` manages large-scale rewrites:
- Discovers all articles for a product
- Tracks state per article (pending → in_progress → completed / failed)
- Retries failed articles
- Resumes from where it left off

---

## Knowledge Base

### Core Scripts

| Script | What It Does |
|--------|-------------|
| `agent.py` | Core AI rewrite agent. Loads style guides + product context, calls LLM to rewrite articles. Supports Anthropic, OpenAI, and Ollama. |
| `run_agent.py` | CLI wrapper to rewrite a single article. |
| `batch_runner.py` | Batch-processes all articles for a product with state tracking. |
| `merge_processor.py` | Parses reorganization plans and merges multiple source articles into one. |
| `redirect_generator.py` | Generates redirect CSV from reorganization plans (old URLs → new URLs). |
| `wordpress_client.py` | WP REST API client using Playwright browser session for auth. Uploads media, creates/updates posts. |
| `scan_videos.py` | Audits legacy articles for embedded YouTube/Wistia videos to incorporate into rewrites. |

### Style Guides

The knowledge base includes several style references that the AI agent uses:

- **`PILLAR.md`** — Agent persona, tone rules, formatting standards, grammar conventions
- **`documentation_master_guide.md`** — Primary style reference with examples
- **`content_guide_summary.md`** — Content standards
- **`sop_summary.md`** — Standard operating procedure for the documentation workflow

### Products Covered

| Product | Status | Location |
|---------|--------|----------|
| **Thrive Apprentice** | 60+ rewritten articles, screenshots captured | `knowledge_base/thrive_apprentice/` |
| **Thrive Leads** | 15 reorganized articles + redirect map | `knowledge_base/thrive_leads/` |
| **Thrive Quiz Builder** | Reorganization planned | Via orchestrator |
| Others (Comments, Headline Optimizer, Ovation, Ultimatum) | Planned | Via orchestrator |

---

## Universal Screenshot Agent

A standalone, product-agnostic screenshot pipeline. Point it at any WordPress product's admin panel, give it markdown docs, and it captures annotated screenshots with red arrows.

### CLI Commands

```bash
# List available products
screenshot-agent list-products

# Parse markdown docs into JSON step specs
screenshot-agent -p my_product parse

# Capture screenshots (headless)
screenshot-agent -p my_product capture getting-started

# Capture with visible browser (for debugging)
screenshot-agent -p my_product capture getting-started --headed

# Capture all articles
screenshot-agent -p my_product capture-all

# Publish screenshots to production via WebSocket
screenshot-agent -p my_product publish

# Generate SEO metadata (title, description, keyphrases) via LLM
screenshot-agent -p my_product generate-seo
screenshot-agent -p my_product generate-seo --article getting-started
screenshot-agent -p my_product generate-seo --provider anthropic --model claude-sonnet-4-5-20250929

# Publish SEO metadata to WordPress via AIOSEO REST API
screenshot-agent -p my_product publish-seo
```

### Pipeline

```
Markdown Docs          Step Parser           Playwright            PIL Annotate
  (.md files)    →    (JSON specs)    →    (screenshots)    →    (red arrows)
                                                                       │
                                                                       ▼
                                                             WebSocket Publisher
                                                             (upload to WP + inject
                                                              into draft posts)

Markdown Docs       SEO Generator         SEO Publisher
 (or wp_posts)  →  (LLM → JSON)    →   (WebSocket → AIOSEO REST API)
```

### SEO Metadata Module

Generates and publishes SEO metadata (title, meta description, focus keyphrase, additional keyphrases) for each article using AIOSEO.

**Generate:** Reads article content from `wp_posts.json` (or markdown docs), calls an LLM to produce optimized SEO fields, and writes `seo_meta.json` to the product directory. Existing entries are preserved — regeneration only fills in missing articles.

**Publish:** Uses the same WebSocket bridge as the screenshot publisher. Python sends `update_seo` commands to Chrome, which PUTs `aioseo_meta_data` to the WP REST API. Requires the AIOSEO REST API addon (Plus plan or above).

**Configuration** in `config.yaml`:
```yaml
seo:
  brand_suffix: " - My Brand"           # Appended to SEO titles
  default_keyphrases: ["my product"]     # Added to every article's keyphrases
```

### Adding a New Product

1. **Copy the template:**
   ```bash
   cp -r universal_screenshot_agent/products/_template universal_screenshot_agent/products/my_product
   ```

2. **Edit `config.yaml`** — product info, local site URL, selectors, navigation flows, articles. See the template for full documentation of each section.

3. **Add markdown docs** to `products/my_product/docs/` — use Gutenberg ordered-list blocks with `<strong>` tags around UI element names.

4. **(Optional) Write `adapter.py`** — only needed for complex SPAs. For simple web apps, config.yaml alone is enough.

5. **Run the pipeline:**
   ```bash
   screenshot-agent -p my_product parse
   screenshot-agent -p my_product capture-all --headed
   screenshot-agent -p my_product publish
   ```

See `products/thrive_apprentice/` for a complete working example with a custom SPA adapter.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `WP_URL` | Local WordPress site URL |
| `WP_USERNAME` | WordPress admin username |
| `WP_PASSWORD` | WordPress admin password |

Set in `.env` (copied from `.env.example`) or export in your shell. The knowledge base scripts in `knowledge_base/` may use additional variables — check `knowledge_base/.env` for the full list.

---

## For Team Members

### Working on a new Thrive product?

1. Clone this repo and install (`pip install -e .`)
2. Check `.agent/workflows/orchestrator.md` for the list of products and available actions
3. Create a product directory in `knowledge_base/` for your product's source and output files
4. Add a product config in `universal_screenshot_agent/products/` for screenshot capture
5. Follow the orchestrator workflow to reorganize → rewrite → capture screenshots → publish

### Just need screenshots?

Jump straight to the [Universal Screenshot Agent](#universal-screenshot-agent) section. Copy the template, configure your product, and run `parse` → `capture-all` → `publish`.
