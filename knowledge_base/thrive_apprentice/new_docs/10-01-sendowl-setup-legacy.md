<!-- wp:heading {"level":1} -->
# How to Set Up SendOwl with Thrive Apprentice (Legacy)
<!-- /wp:heading -->

<!-- wp:paragraph -->
**Important: SendOwl integration is a legacy feature.** Thrive Apprentice now offers built-in payment processing through Stripe and WooCommerce integration. We recommend using these modern alternatives for new setups. This guide is maintained as a reference for existing SendOwl users.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
In this article, you'll learn how to set up the SendOwl integration with Thrive Apprentice—from creating your SendOwl account to configuring products, API keys, and course access protection.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## What Is SendOwl?
<!-- /wp:heading -->

<!-- wp:paragraph -->
SendOwl is a third-party digital product delivery platform that handles checkout, payment processing, and product delivery. When integrated with Thrive Apprentice, SendOwl processes payments and automatically grants students access to your courses after purchase.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Setting Up the SendOwl Listener
<!-- /wp:heading -->

<!-- wp:paragraph -->
The SendOwl listener is the connection point between SendOwl and your WordPress site. It listens for purchase notifications and triggers course access.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Settings** in the left sidebar.
3. Navigate to the **SendOwl** tab.
4. You'll see a **Listener URL**—copy this URL.
5. Log in to your **SendOwl account**.
6. Go to **Settings** > **Webhooks/Notifications**.
7. Paste the Listener URL into the webhook field.
8. Save your SendOwl settings.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** The listener URL is unique to your WordPress installation. If you change your site's domain or permalink structure, you'll need to update the webhook in SendOwl.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Configuring API Key Permissions
<!-- /wp:heading -->

<!-- wp:paragraph -->
Thrive Apprentice needs API access to communicate with your SendOwl account.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In your **SendOwl account**, go to **Settings** > **API**.
2. Locate your **API Key** and **API Secret**.
3. Back in **Thrive Apprentice** > **Settings** > **SendOwl**, enter your API credentials.
4. Click **Connect** to verify the connection.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** Make sure your API key has the necessary permissions for product management and order processing. Read-only keys will not work for course access provisioning.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Creating Products in SendOwl
<!-- /wp:heading -->

<!-- wp:paragraph -->
Each course (or bundle) you sell needs a corresponding product in SendOwl.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In **SendOwl**, go to **Products** > **Add Product**.
2. Set the product **Name** to match your course title.
3. Set the **Price** and payment options (one-time or subscription).
4. Under **Product Type**, select **Digital Product**.
5. Save the product.
6. Back in **Thrive Apprentice**, go to **Products** and link the SendOwl product to the corresponding course.
<!-- /wp:list -->

<!-- wp:heading -->
## Assigning Course Access and Protection
<!-- /wp:heading -->

<!-- wp:paragraph -->
Once your products are linked, configure which courses each product unlocks.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In **Thrive Apprentice**, go to the **Products** section.
2. Click on the product linked to your SendOwl item.
3. Under **Course Access**, select which courses this product grants access to.
4. Configure **Access Rules** to restrict content to purchasers only.
5. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** You can assign multiple courses to a single SendOwl product to create a bundle deal—students gain access to all selected courses with one purchase.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## The Purchasing Process
<!-- /wp:heading -->

<!-- wp:paragraph -->
Here's how the end-to-end flow works once everything is configured:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. A visitor clicks a **Buy** button on your course page.
2. They're redirected to the **SendOwl checkout** page.
3. The student completes payment through SendOwl.
4. SendOwl sends a webhook notification to your **Listener URL**.
5. Thrive Apprentice receives the notification and **grants course access** to the student.
6. The student receives a confirmation email with login details.
<!-- /wp:list -->

<!-- wp:paragraph -->
That's it! You've successfully set up SendOwl with Thrive Apprentice to sell and deliver online courses.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **SendOwl Operations:** Learn about managing customers, discounts, and troubleshooting in the [SendOwl Operations and Troubleshooting guide](#).
- **Modern Alternative — Stripe:** Set up native payment processing with the [Stripe Integration Guide](#).
- **Modern Alternative — WooCommerce:** Use WooCommerce for flexible checkout with the [WooCommerce Integration Guide](#).
- **Access Control:** Understand access rules in the [Access Restrictions and Rules guide](#).
<!-- /wp:list -->
