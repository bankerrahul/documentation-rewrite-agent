---
description: Batch process all documentation articles for a Thrive Themes product.
---

# Batch Processing Workflow

Process multiple documentation articles through the rewrite agent in sequence, with progress tracking and resume support.

## Phase 1: Initialize

### Option A: Initialize from existing source files

If the product directory already has source markdown files (like `thrive_leads/`):

```bash
cd knowledge_base
python batch_runner.py <product> --init
```

This scans the product directory for `*.md` files and creates `batch_state.json`.

### Option B: Initialize from a reorganization plan

If you want to include merge tasks from a reorganization plan:

```bash
cd knowledge_base
python merge_processor.py <PRODUCT_REORGANIZATION.md> --product-dir <product_dir> --output <product_dir>/batch_state.json
```

This parses the reorganization plan and generates a batch state with merge groups.

### Check existing state

```bash
cd knowledge_base
python batch_runner.py <product> --status
```

## Phase 2: Process Articles

### Process all pending articles

```bash
cd knowledge_base
python batch_runner.py <product> --resume
```

The batch runner will:
1. Pick the next pending article from `batch_state.json`
2. Read the source file(s)
3. For merge tasks, combine sources and call `agent.process_merge()`
4. For single articles, call `agent.process_document()`
5. Write 4 output files to `<product>/output/<article_id>/`
6. Update `batch_state.json` with status and output paths
7. Wait `BATCH_DELAY_SECONDS` (default 2s) between articles
8. Continue until all articles are processed

### Process a specific article

```bash
cd knowledge_base
python batch_runner.py <product> --article <article_id>
```

### Retry failed articles

```bash
cd knowledge_base
python batch_runner.py <product> --retry-failed
```

## Phase 3: Review Outputs

For each completed article, review the outputs:

1. **Read `rewritten_doc.md`** — Verify it follows the style guide, has proper formatting, correct UI element bolding, and logical flow.

2. **Read `review.md`** — Check for flagged issues, broken links, and recommendations.

3. **Read `image_mapping.md`** — Verify image descriptions and alt text are accurate.

4. **Read `screenshot_spec.json`** — Validate the JSON structure and URLs.

If an article needs revision:
- Edit the source file or adjust merge instructions in `batch_state.json`
- Manually set the article's status back to `"pending"` in `batch_state.json`
- Re-run the batch processor for that article

## Phase 4: Post-Processing

After all articles are processed:

### Generate redirect map

```bash
cd knowledge_base
python redirect_generator.py <PRODUCT_REORGANIZATION.md> --output <product>/redirect_map.csv
```

### Capture screenshots

For each article's `screenshot_spec.json`:
```bash
cd knowledge_base
python scripts/screenshot_runner.py <product>/output/<article_id>/screenshot_spec.json
```

### Generate SEO metadata

Generate SEO-optimized titles, meta descriptions, and keyphrases for all articles:

```bash
# Generate SEO for all articles (reads from wp_posts.json)
screenshot-agent -p <product> generate-seo

# Generate for a single article
screenshot-agent -p <product> generate-seo --article <slug>

# Use a specific LLM provider
screenshot-agent -p <product> generate-seo --provider anthropic
```

This creates `seo_meta.json` in the product directory with:
- SEO title (< 60 chars, with optional brand suffix from config)
- Meta description (140-160 chars)
- Focus keyphrase
- Additional keyphrases (2-3)

Existing entries are preserved — re-running only fills in missing articles.

### Generate metadata report

Review all articles and compile:
- Master metadata table (title, URL, category, meta description)
- Redirect map summary
- Screenshot completion status
- SEO metadata completion status

## Phase 5: Summary

Check final status:
```bash
cd knowledge_base
python batch_runner.py <product> --status
```

Expected output shows all articles as `completed` or `skipped`.

## Output Directory Structure

After batch processing, the product directory will look like:

```
<product>/
  batch_state.json
  redirect_map.csv
  output/
    <article_1_id>/
      rewritten_doc.md
      image_mapping.md
      review.md
      screenshot_spec.json
    <article_2_id>/
      ...
```
