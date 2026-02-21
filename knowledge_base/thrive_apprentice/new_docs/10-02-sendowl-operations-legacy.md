<!-- wp:heading {"level":1} -->
# SendOwl Operations and Troubleshooting (Legacy)
<!-- /wp:heading -->

<!-- wp:paragraph -->
**Important: SendOwl integration is a legacy feature.** Thrive Apprentice now offers built-in payment processing through Stripe and WooCommerce integration. We recommend using these modern alternatives for new setups. This guide is maintained as a reference for existing SendOwl users.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
In this article, you'll learn how to manage day-to-day SendOwl operations—from customizing the checkout experience to managing customers, applying discounts, and troubleshooting common issues.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Managing the Checkout Process
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
### Customizing Checkout Templates
<!-- /wp:heading -->

<!-- wp:paragraph -->
SendOwl provides customizable checkout templates to match your brand:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In **SendOwl**, go to **Settings** > **Checkout Templates**.
2. Select an existing template or click **Create New**.
3. Customize the layout, colors, logo, and text fields.
4. Assign the template to your products under each product's settings.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Sending Customers Directly to Checkout
<!-- /wp:heading -->

<!-- wp:paragraph -->
You can bypass your sales page and send visitors straight to the SendOwl checkout form:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In **SendOwl**, open the product you want to link.
2. Copy the **Direct Checkout URL** from the product's sharing options.
3. Use this URL in your buttons, emails, or landing pages to send customers directly to payment.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Configuring the Registration and Thank You Pages
<!-- /wp:heading -->

<!-- wp:list -->
- **Registration Page** — After purchase, students are prompted to create a WordPress account. Configure this in **Thrive Apprentice** > **Settings** > **Login & Registration**.
- **Thank You Page** — Set a custom redirect URL in SendOwl under the product's **After Purchase** settings. Point it to a WordPress page with enrollment confirmation and next steps.
<!-- /wp:list -->

<!-- wp:heading -->
## Managing Customers
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
### Viewing the Customer List
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. In **SendOwl**, go to **Orders** to see all completed purchases.
2. Filter by product, date range, or payment status.
3. Click on any order to view customer details, purchase history, and payment information.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Finding Specific Customers
<!-- /wp:heading -->

<!-- wp:paragraph -->
To locate a specific customer:
<!-- /wp:paragraph -->

<!-- wp:list -->
- Use the **search bar** in SendOwl's Orders section to search by name or email.
- In **Thrive Apprentice**, go to the **Members** section and search for the student by name or email to view their course enrollment status.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Customer Login After Purchase
<!-- /wp:heading -->

<!-- wp:paragraph -->
After completing a SendOwl purchase, students need to log in to access their courses:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. The student receives a confirmation email with login credentials (or a link to set their password).
2. They visit your site's **Login** page.
3. After logging in, they're redirected to their course dashboard with access to purchased content.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Make sure your login page URL is correctly configured in **Thrive Apprentice** > **Settings** > **Login & Registration** so students land on the right page.
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### Customer Login After Completing a Course
<!-- /wp:heading -->

<!-- wp:paragraph -->
Students who return after completing a course will see their progress preserved. Course completion status, certificates, and grade data are stored in Thrive Apprentice—independent of SendOwl.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Mailing List Integration
<!-- /wp:heading -->

<!-- wp:paragraph -->
You can automatically add SendOwl customers to your email marketing list:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In **SendOwl**, go to **Settings** > **Integrations**.
2. Connect your email service provider (Mailchimp, ConvertKit, AWeber, etc.).
3. Map the product to a specific email list or tag.
4. When a purchase completes, the customer is automatically added to your list.
<!-- /wp:list -->

<!-- wp:heading -->
## Applying Discounts
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. In **SendOwl**, go to **Marketing** > **Discount Codes**.
2. Click **Create Discount Code**.
3. Set the code name, discount type (percentage or fixed amount), and expiration date.
4. Optionally restrict the code to specific products.
5. Share the discount code with your audience—students enter it at checkout.
<!-- /wp:list -->

<!-- wp:heading -->
## Viewing SendOwl Logs
<!-- /wp:heading -->

<!-- wp:paragraph -->
SendOwl logs help you troubleshoot purchase and access issues:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In **Thrive Apprentice**, go to **Settings** > **SendOwl**.
2. Check the **Connection Log** for recent webhook events.
3. Each entry shows the timestamp, order ID, product, and whether access was successfully granted.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** If a student reports they don't have access after purchasing, check the logs first. Common issues include webhook delivery failures, mismatched product IDs, or the student using a different email address.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Selling Subscriber-Only Courses
<!-- /wp:heading -->

<!-- wp:paragraph -->
To sell courses exclusively to existing subscribers or members:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Create a product in **SendOwl** for the subscriber-only course.
2. In **Thrive Apprentice**, assign the course to this product.
3. Set access rules so only users with the correct product access can view the course.
4. Share the **Direct Checkout URL** only with your subscriber list through email campaigns.
<!-- /wp:list -->

<!-- wp:heading -->
## Troubleshooting Common Issues
<!-- /wp:heading -->

<!-- wp:list -->
- **Student can't access course after purchase** — Check SendOwl logs for webhook errors. Verify the student's email matches their WordPress account. Manually grant access in the **Members** section if needed.
- **Webhook not firing** — Confirm the Listener URL in SendOwl matches the one shown in Thrive Apprentice settings. Test with a $0 product to verify the connection.
- **Duplicate orders** — Check for duplicate webhook entries in the logs. SendOwl occasionally retries failed webhooks, which can create duplicate access records.
- **Checkout page not loading** — Verify your SendOwl subscription is active and the product is published.
<!-- /wp:list -->

<!-- wp:paragraph -->
That's it! You've learned how to manage SendOwl operations including checkout customization, customer management, discounts, and troubleshooting for your Thrive Apprentice integration.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **SendOwl Setup:** Review the initial configuration in the [SendOwl Setup Guide (Legacy)](#).
- **Modern Alternative — Stripe:** Migrate to native payments with the [Stripe Integration Guide](#).
- **Modern Alternative — WooCommerce:** Use WooCommerce for checkout with the [WooCommerce Integration Guide](#).
- **Managing Members:** Learn about member management in the [Managing Members guide](#).
<!-- /wp:list -->
