# How to Use ThriveBoxes and Shortcode Forms

While Lead Groups automate form placement, sometimes you need manual control. That's where **ThriveBoxes** and **Lead Shortcodes** come in.

## ThriveBoxes (2-Step Opt-ins)

A **ThriveBox** is a popup (lightbox) that is hidden by default and only appears when a user clicks a specific link, button, or image. This "2-step" process often leads to higher conversion rates because the user has shown intent.

### Creating a ThriveBox

1. Go to **Thrive Dashboard >> Thrive Leads**.
2. Scroll down to **ThriveBoxes**.
3. Click **Add New**.
4. Name it and click **Add ThriveBox**.
5. Click **Edit** (pencil icon) to design the form in Thrive Architect.

### Triggering a ThriveBox

### Triggering via Shortcode

1. Copy the shortcode provided next to the ThriveBox name (e.g., `[thrive_leads id='123']`).
2. Paste it around your text or image in the WordPress editor:
    `[thrive_leads id='123']Click Here to Subscribe[/thrive_leads]`

### Triggering via Thrive Architect

1. In Thrive Architect, select any Button, Text, or Image.
2. Go to **Animation & Action**.
3. Select **Popups** > **Open Thrive Leads ThriveBox**.
4. Search for and select your ThriveBox.
5. Click **Apply**.

## Lead Shortcodes

**Lead Shortcodes** are inline forms that you manually place inside your content. They are perfect for in-depth guides where you want a specific offer mid-content.

### Creating a Shortcode Form

1. Go to the **Lead Shortcodes** section in the Thrive Leads dashboard.
2. Click **Add New**.
3. Name it and click **Add Lead Shortcode**.
4. Click **Edit** to design the form (Shortcode forms typically use the "Post Footer" or "In-Content" templates).

### Content Locking

A specialized feature of Lead Shortcodes is **Content Locking**, where you hide part of your post content until the user subscribes.

1. Create a new Lead Shortcode.
2. Toggle **Content Locking** to **ON**.
3. Design the form (this is the "gate" that users will see).
4. In the dashboard, choose a **Lock Mode**:
    * **Hide**: Content is invisible.
    * **Blur**: Content is blurred (great for teaser effect).
5. Copy the shortcode. It will look like this:
    `[tve_leads_shortcode_123] Hidden Content Goes Here [/tve_leads_shortcode_123]`
6. Paste it into your post, wrapping the text you want to lock.
