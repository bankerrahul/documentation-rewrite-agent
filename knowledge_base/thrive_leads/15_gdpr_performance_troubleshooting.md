# How to Manage GDPR Compliance, Performance, and Troubleshooting

In this article, you'll learn how to keep your Thrive Leads installation compliant, fast, and error-free.

## GDPR Compliance

To ensure your forms are GDPR compliant, you may need to add an explicit consent checkbox or "Legal text" to your forms.

1. Open your form in **Thrive Architect**.
2. Click the **Lead Generation** element.
3. In the left sidebar, add a new field type: **Checkbox**.
4. Label it "I agree to the Terms & Conditions" (link to your privacy policy).
5. Mark it as **Required**.
6. This ensures no one can sign up without explicitly checking the box.

## Performance Optimization

Thrive Leads is built for speed, but you can optimize it further.

### Lazy Load Forms

This is the most impactful setting for Core Web Vitals.

1. Go to **Thrive Leads Dashboard** > **Settings** > **Lazy Load Forms**.
2. Toggle it **ON**.
3. **What it does:** It waits until your website's main content is fully loaded before loading the Thrive Leads scripts and forms. This prioritizes your content and improves PageSpeed scores.

### Caching Compatibility

If you use caching plugins (like WP Rocket or W3 Total Cache):

* **HTML Forms:** Thrive Leads forms are compatible by default.
* **A/B Testing:** If you are running tests, ensure your caching plugin is not caching the specific form output, or rely on Thrive Leads' AJAX loading (which Lazy Load handles) to ensure the correct variation is shown to each visitor.

## Troubleshooting

### "My Form Isn't Showing Up"

Check these common culprits:

1. **Display Settings:** Did you select the correct posts/pages?
2. **Display Frequency:** Is it set to "Show every 7 days"? Set it to **0** for testing.
3. **Active Status:** Is the switch for **Desktop/Mobile** toggled ON? Is the **Lead Group** itself toggled ON?
4. **Already Subscribed:** Are you testing from a browser where you already subscribed? (Thrive Leads might be hiding the form). Test in Incognito mode.

### Leads Export

If your autoresponder connection fails, your leads are safe.

1. Go to **Advanced Features** > **Leads Export**.
2. Filter by date or source.
3. Click **Export** to download a CSV file of all collected data.

That's it! You can now maintain a healthy and compliant Thrive Leads setup.

### Related Resources

* **Dashboard:** [Understanding the Thrive Leads Dashboard](./3_understanding_the_thrive_leads_dashboard.md)
* **Autoresponders:** [Connecting Autoresponders and Email Services](./6_connecting_autoresponders.md)
