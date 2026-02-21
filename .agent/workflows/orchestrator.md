---
description: Master workflow for Thrive Themes documentation agent. Start here to pick a product and action.
---

# Documentation Agent Orchestrator

This is the master entry point for all documentation reorganization work. Follow the steps below to choose a product and action.

## Step 1: Check Current State

Before starting, review what products have documentation and what state they're in:

**Products with reorganization plans:**

| Product | Source Articles | Target | Plan File | Status |
|---------|---------------|--------|-----------|--------|
| Thrive Leads | 40 | ~15 | `THRIVE_LEADS_DOCS_REORGANIZATION.md` | COMPLETED |
| Thrive Quiz Builder | 48 | ~20 | `THRIVE_QUIZ_BUILDER_REORGANIZATION.md` | Drafts ready |
| Thrive Comments | 16 | 6 | `THRIVE_COMMENTS_REORGANIZATION_SUMMARY.md` | Plan ready |
| Thrive Headline Optimizer | 6 | 4 | `THRIVE_HEADLINE_OPTIMIZER_REORGANIZATION_ANALYSIS.md` | Plan ready |
| Thrive Ovation | 8 | 5-6 | `THRIVE_OVATION_DOCS_REORGANIZATION.md` | Plan ready |
| Thrive Ultimatum | 28 | ~22 | `THRIVE_ULTIMATUM_DOCS_REORGANIZATION.md` | Plan ready |

All plan files are in `knowledge_base/`.

## Step 2: Choose a Product

Ask the user which product they want to work on. Read the corresponding reorganization plan to understand the scope.

## Step 3: Choose an Action

Present these options to the user:

1. **Reorganize** — Analyze existing docs, create or refine a reorganization plan
   → Use workflow: `reorganize_product.md`

2. **Batch Rewrite** — Process all articles for this product through the agent
   → Use workflow: `batch_process.md`

3. **Single Rewrite** — Rewrite one specific article
   → Use workflow: `rewrite_docs.md`

4. **Merge Articles** — Combine multiple source articles into one consolidated guide
   → Run: `python knowledge_base/merge_processor.py <plan_file> --dry-run`
   → Then use `batch_runner.py` with merge-enabled batch state

5. **Generate Redirects** — Create redirect map from reorganization plan
   → Run: `python knowledge_base/redirect_generator.py <plan_file>`

6. **Publish to WordPress** — Push rewritten docs to WordPress
   → Use workflow: `publish_to_wordpress.md`

7. **Capture Screenshots** — Run headless screenshot capture for a product
   → Run: `python knowledge_base/scripts/screenshot_runner.py <spec.json>`

8. **Check Status** — View batch progress for a product
   → Run: `python knowledge_base/batch_runner.py <product> --status`

## Step 4: Execute

Based on the user's choice, either:
- Invoke the appropriate sub-workflow
- Run the appropriate Python script
- Guide the user through the process interactively

## Key Files Reference

**Python Scripts (in `knowledge_base/`):**
- `agent.py` — Core documentation agent (supports Anthropic, OpenAI, Ollama)
- `run_agent.py` — Single document processing CLI
- `batch_runner.py` — Batch processing engine
- `merge_processor.py` — Parse reorg plans, generate merge batches
- `redirect_generator.py` — Generate redirect CSV maps
- `wordpress_client.py` — WordPress REST API client
- `capture_screenshots.py` — Screenshot capture with annotations
- `scripts/screenshot_runner.py` — Headless screenshot runner

**Configuration:**
- `.env` — API keys, WordPress credentials
- `requirements.txt` — Python dependencies
- `PILLAR.md` — Agent persona and documentation standards
- `documentation_master_guide.md` — Primary style reference
