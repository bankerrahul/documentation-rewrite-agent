<!-- wp:heading {"level":1} -->
# How to Set Up Custom Payment Links in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to use the Custom Payments feature in Thrive Apprentice to connect your products to external checkout pages and third-party payment processors. This gives you the flexibility to sell courses through any payment platform while still managing access within Thrive Apprentice.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## What Are Custom Payment Links?
<!-- /wp:heading -->

<!-- wp:paragraph -->
Custom payment links let you connect a Thrive Apprentice product to an external checkout or sales page instead of using a built-in payment integration. When a visitor clicks the "Buy" or "Enroll" button on a restricted course, they're directed to your external checkout page where the transaction is processed by a third-party service.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
After a successful payment, the third-party service communicates with Thrive Apprentice (typically through a webhook or integration) to grant the student access to the product.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## When to Use Custom Payment Links
<!-- /wp:heading -->

<!-- wp:paragraph -->
Custom payment links are the right choice when:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **You use a third-party payment processor** — Services like ThriveCart, SamCart, Paddle, or any checkout platform that isn't natively integrated with Thrive Apprentice.
- **You have a dedicated sales page** — You've built a standalone sales page (on your site or elsewhere) and want to direct buyers there instead of a generic checkout.
- **You sell through an external marketplace** — Your courses are listed on platforms that handle their own payment processing.
- **You need a custom checkout flow** — Your sales funnel includes upsells, order bumps, or multi-step checkout processes handled outside of WordPress.
<!-- /wp:list -->

<!-- wp:heading -->
## Setting Up Custom Payment Links
<!-- /wp:heading -->

<!-- wp:paragraph -->
To configure a custom payment link on a product:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice** > **Products**.
2. Click on the product you want to connect to an external checkout.
3. Open the **Access Requirements** section of the product settings.
4. Select **Custom Payments** as the access method.
5. In the **Payment Link URL** field, enter the full URL of your external checkout page or sales page.
6. Click **Save** to apply.
<!-- /wp:list -->

<!-- wp:paragraph -->
Once configured, any call-to-action buttons associated with this product—such as "Buy Now" or "Enroll"—will direct visitors to the URL you specified.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Obtaining and Using the Custom Payment Link
<!-- /wp:heading -->

<!-- wp:paragraph -->
After setting up the custom payment link, Thrive Apprentice generates a unique product URL that you can share or embed:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In the product settings under **Custom Payments**, locate the **Product Access Link** section.
2. Copy the generated link.
3. Use this link on your sales page, in email campaigns, or anywhere you promote your course.
<!-- /wp:list -->

<!-- wp:paragraph -->
This link ensures that when a student completes a purchase through your external processor, their access is correctly mapped back to the Thrive Apprentice product.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Tip:** Pair your custom payment link with a webhook from your payment processor to automate access granting. Most third-party checkout tools support webhook notifications that can trigger Thrive Apprentice to grant product access immediately after purchase.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Testing the Checkout Flow
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before going live, always test the complete checkout experience:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Visit a restricted course page as a logged-out user.
2. Click the call-to-action button (e.g., **Buy Now** or **Enroll**).
3. Verify that you're redirected to the correct external checkout page.
4. Complete a test purchase using your payment processor's test or sandbox mode.
5. Confirm that product access is granted in Thrive Apprentice after the test purchase.
6. Log in as the test student and verify that all course content is accessible.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** If access isn't granted after a test purchase, check your webhook configuration in both your payment processor and Thrive Apprentice. Ensure the product IDs or access triggers are correctly mapped.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Note:** If you're using a third-party integration that requires an API connection, make sure the API credentials are correctly entered in **Thrive Dashboard** > **Thrive Apprentice** > **Settings** > **API Connections** before testing.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Conclusion
<!-- /wp:heading -->

<!-- wp:paragraph -->
That's it! You've successfully learned how to set up custom payment links to connect your Thrive Apprentice products to external checkout pages and third-party payment processors. This gives you full flexibility over your sales process while keeping access management centralized in Thrive Apprentice.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Products** — [How to Use the Products Section in Thrive Apprentice](3-02-using-the-products-section.md)
- **Access Restrictions** — [How to Set Up Access Restrictions and Rules in Thrive Apprentice](3-01-access-restrictions-and-rules.md)
- **Access Expiry** — [How to Manage Product Access Expiry in Thrive Apprentice](3-03-managing-product-access-expiry.md)
- **File Protection** — [How to Protect Files and Grant Access in Thrive Apprentice](3-04-protecting-files-and-granting-access.md)
<!-- /wp:list -->
