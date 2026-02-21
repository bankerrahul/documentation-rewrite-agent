---
description: Full product documentation reorganization — analyze, plan, merge, rewrite.
---

# Product Reorganization Workflow

Guide for analyzing existing documentation and creating a reorganization plan for a Thrive Themes product.

## Phase 1: Discovery

### Gather existing documentation

**Option A: From WordPress (if configured)**
```bash
cd knowledge_base
python wordpress_client.py --test
python wordpress_client.py --list-posts
```

**Option B: From the Thrive Themes website**
Read the existing reorganization plan if one exists, or manually list all articles from:
`https://thrivethemes.com/docs-categories/<product-slug>/`

**Option C: From local files**
Check `knowledge_base/<product>/` for existing source files.

### Create an inventory

For each article, record:
- Title
- URL
- Category
- Approximate word count
- Key topics covered

Save to `knowledge_base/<PRODUCT>_docs_inventory.md`.

## Phase 2: Analysis

Read the following knowledge base files for context:
- `PILLAR.md` — Documentation standards
- `documentation_master_guide.md` — Style and formatting rules
- Any existing reorganization plan for this product

### Identify issues

Analyze the documentation inventory for:
1. **Overlapping content** — Multiple articles covering the same topic
2. **Thin content** — Articles too short to stand alone (< 200 words)
3. **Category imbalance** — Categories with 1-2 articles or 10+ articles
4. **Outdated content** — Features that have changed or been removed
5. **Missing content** — Key features not documented
6. **SEO opportunities** — Better title structures, keyword targeting

### Define merge groups

Group related articles that should be consolidated:
- Articles covering different aspects of the same workflow
- Articles that are too thin to stand alone
- Overlapping/duplicate content

### Define prune list

Identify articles to:
- **Delete** — Outdated, irrelevant, or fully duplicated
- **Merge then prune** — Content folded into another article
- **Relocate** — Move to a different category

## Phase 3: Create the Reorganization Plan

Write the plan to `knowledge_base/<PRODUCT>_REORGANIZATION.md` following this structure:

```markdown
# <Product> Documentation — Reorganization Analysis

**Source:** [<Product> docs](<URL>)
**Total:** <N> articles across <M> categories

## 1. Full List of All Docs (by category)

### <Category Name> (<count> articles)

| # | Title | URL |
|---|-------|-----|
| 1 | ... | ... |

## 2. Merge Ideas

| Merge group | Target article (new or existing) | Source articles | Rationale |
|-------------|----------------------------------|-----------------|-----------|
| ... | ... | ... | ... |

## 3. Delete or Prune Ideas

| Action | Article(s) | Rationale |
|--------|-----------|-----------|
| ... | ... | ... |

## 4. Category Reorganization

### Proposed structure

| Category | Contents | Article count (approx) |
|----------|----------|----------------------|
| ... | ... | ... |

## 5. Final Proposed Doc List (after merges)

### <Category> (<count> articles)
1. Article title
2. Article title (merge: source1 + source2)
...

## 6. Summary

| Metric | Before | After |
|--------|--------|-------|
| Total articles | ... | ... |
| Categories | ... | ... |
```

## Phase 4: Generate Batch State

Once the plan is approved:

```bash
cd knowledge_base
python merge_processor.py <PRODUCT>_REORGANIZATION.md --product-dir <product_dir> --output <product_dir>/batch_state.json
```

This creates a `batch_state.json` with all articles (including merge tasks) ready for batch processing.

## Phase 5: Generate Redirect Map

```bash
cd knowledge_base
python redirect_generator.py <PRODUCT>_REORGANIZATION.md --output <product_dir>/redirect_map.csv
```

Review the redirect map for accuracy. Items marked `# NEEDS_REVIEW` require manual attention.

## Phase 6: Execute

Hand off to the **Batch Process** workflow to process all articles:

```bash
cd knowledge_base
python batch_runner.py <product> --resume
```

## Phase 7: Verify

After batch processing is complete:

1. **Check all outputs** — Read each `rewritten_doc.md` for quality
2. **Cross-check internal links** — Ensure links between articles point to the correct new URLs
3. **Validate redirect map** — Every old URL has a valid new target
4. **Validate categories** — Each article belongs to the correct proposed category
5. **Generate metadata report** — Compile titles, URLs, categories, and meta descriptions

## Reference: Completed Products

Use these as examples of the expected output:

- **Thrive Leads**: `knowledge_base/thrive_leads/` (15 articles, published)
  - Metadata: `thrive_leads_master_metadata.md`
  - Redirects: `redirect_map.csv`
