# Screenshot spec schema

Machine-readable spec for the headless screenshot runner (`scripts/screenshot_runner.py`). Use this when you want repeatable, CI-friendly screenshot capture without the Cursor browser MCP.

## Format: JSON

### Top-level fields

| Field      | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `base_url` | string | Yes      | Base URL for the site (e.g. `https://staging.example.com`). Paths in `captures[].url` are resolved against this. |
| `login`   | object | No       | If omitted, the runner uses `WP_USERNAME` and `WP_PASSWORD` from the environment. |
| `login.user` | string | No     | WordPress admin username (prefer env `WP_USERNAME` in CI). |
| `login.password` | string | No  | WordPress admin password (prefer env `WP_PASSWORD`; never commit secrets). |
| `captures` | array | Yes     | List of screenshot capture definitions. |

### Capture object

Each element of `captures` has:

| Field       | Type    | Required | Description |
|-------------|---------|----------|-------------|
| `image_id` | string  | Yes      | Identifier matching `image_mapping.md` (e.g. `generate-course-selection`). Used as filename: `{image_id}.png`. |
| `url`      | string  | Yes      | Path or full URL to open (e.g. `/wp-admin/admin.php?page=tva_admin_dashboard` or full URL). |
| `steps`    | array   | No       | List of actions to run after navigation (see below). |
| `selector` | string  | No       | CSS selector for element-only screenshot. If omitted, the full viewport or full page is captured (see `full_page`). |
| `full_page`| boolean | No       | If `true`, capture the full scrollable page. Default `false`. Ignored if `selector` is set. |

### Step object (inside `steps`)

Each step is an object with one of:

- **Click:** `{ "click": "<css-selector>" }`
- **Wait:** `{ "wait": <milliseconds> }` (e.g. `{ "wait": 1000 }`)
- **Fill:** `{ "fill": { "selector": "<css-selector>", "text": "<value>" } }`

Steps run in order after the page has loaded.

## Example

```json
{
  "base_url": "https://staging.example.com",
  "captures": [
    {
      "image_id": "generate-course-selection",
      "url": "/wp-admin/admin.php?page=tva_admin_dashboard",
      "steps": [
        { "click": ".tva-add-course-button" },
        { "wait": 500 },
        { "click": "[data-action=generate-with-ai]" }
      ],
      "selector": ".tva-add-course-modal",
      "full_page": false
    },
    {
      "image_id": "prompt-input-settings",
      "url": "/wp-admin/admin.php?page=tva_admin_dashboard",
      "steps": [
        { "click": ".tva-add-course-button" },
        { "click": "[data-action=generate-with-ai]" },
        { "wait": 1000 }
      ],
      "full_page": false
    }
  ]
}
```

## Usage

- Pass the spec file to the runner: `python scripts/screenshot_runner.py screenshot_spec.json --output docs/features/assets`.
- Base URL can be overridden with env `WP_URL` (runner uses `WP_URL` if set, else `base_url` from spec).
- Login: use env `WP_USERNAME` and `WP_PASSWORD`, or set `login.user` / `login.password` in the spec (avoid committing passwords).
