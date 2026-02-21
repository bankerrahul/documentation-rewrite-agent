---
description: Rewrite a single documentation article using OptinMonster/Thrive Themes style guidelines.
---

# Documentation Rewrite Workflow

This workflow guides the agent in rewriting a single documentation article to match the OptinMonster style guide. Uses Claude API by default.

## 1. Analyze the Source

*   Read the provided source file or URL.
*   Identify the core goal of the document.
*   Extract key steps and technical details.
*   Check the knowledge base for relevant reorganization plans.

## 2. Rewrite Rules

Apply the following rules to the new draft:

### Tone & Voice
*   **Friendly & Helpful:** Use a conversational tone.
*   **User-Centric:** Address the user as "**you**".
*   **Concise:** Focus on actionable "how-to" steps.

### Formatting
*   **UI Elements:** **Bold** all buttons, labels, tabs, and menu items (e.g., Click **Save**).
*   **Headings:** Use **Title Case** for H1, H2, H3.
*   **Lists:** Use Numbered Lists for steps, Bulleted Lists for options.
*   **Alerts:** Use **Note:**, **Tip:**, **Important:**, **Warning:** for emphasis.

### Grammar & Terminology
*   **Capitalization:** Match UI exactly. Capitalize **OptinMonster**.
*   **Punctuation:** Use **Oxford Comma**. Use **Em Dashes (—)** without spaces.
*   **Spelling:** American English (e.g., "color").
*   **Terms:** Use "log in" (verb), "website", "email" (no hyphen).

### Standard Snippets
*   **Intro:** "In this article, you'll learn how to..."
*   **Steps:** "Next, you'll need to...", "Once you've done that..."
*   **Outro:** "That's it! You've successfully..."
*   **Related Resources:**
    *   Add 3-5 **highly relevant** links (avoid generic ones).
    *   Include a link to the **Product Knowledge Base** (e.g., "Explore the full Thrive Leads knowledge base").

## 3. SEO & Technical Checks
*   **Keywords:** Include target keywords in Title, H1, and first paragraph.
*   **Meta Description:** Write a meta description (max 160 chars).
*   **Images:** Ensure all images have descriptive Alt Text.
*   **Links:** **CRITICAL:** Check all links in the original doc. Fix broken links and list them in the review.
*   **Video Content:** Audit the legacy article for any embedded YouTube or Wistia videos and incorporate them into the new draft.

## 4. Deliverables (Output)

For each document, generate FOUR (4) files:

1.  **`rewritten_doc.md`**: The final, polished content.
2.  **`image_mapping.md`**: A guide for image placement (Standard: 800px width, None alignment).
3.  **`review.md`**: A summary of:
    *   Issues found (broken links, casual tone).
    *   Improvements made.
    *   List of fixed links.
4.  **`screenshot_spec.json`**: A JSON spec for headless screenshot capture with:
    *   `base_url`: Staging site URL
    *   `captures`: Array of `{image_id, url, steps, selector, full_page}`

## 5. Running the Agent

To process a single document using the Python agent:

```bash
cd knowledge_base
python run_agent.py <path_to_source.md> --provider anthropic
```

Or with a specific model:
```bash
python run_agent.py <path_to_source.md> --provider anthropic --model claude-sonnet-4-5-20250929
```

## 6. Screenshot Capture

After the rewrite, capture screenshots using the generated spec:

```bash
python scripts/screenshot_runner.py <path_to_screenshot_spec.json>
```

## 7. Final Verification
*   Check against the rules above.
*   Ensure the walkthrough is logically sound and easy to follow.
*   Verify all 4 output files are generated and non-empty.
