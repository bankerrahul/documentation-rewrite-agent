<!-- wp:heading {"level":1} -->
# How to Get Started with WooCommerce and Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to connect WooCommerce to Thrive Apprentice so you can sell your online courses through WooCommerce's e-commerce platform. By the end, you'll have a WooCommerce product linked to a Thrive Apprentice course with proper access restrictions in place.
<!-- /wp:paragraph -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=xzw4YMMox2w","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=xzw4YMMox2w
<!-- /wp:embed -->

<!-- wp:heading -->
## Prerequisites
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before you begin, make sure you have the following ready:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **WooCommerce** plugin installed and activated on your WordPress site
- **Thrive Apprentice** installed and activated
- At least one payment method configured in WooCommerce (e.g., Stripe, PayPal)
- A course created in Thrive Apprentice that you want to sell
<!-- /wp:list -->

<!-- wp:heading -->
## Step 1: Create a Product in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
First, you need a Thrive Apprentice product that contains the course you want to sell.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Products** in the left sidebar.
3. Click **Add New** to create a new product.
4. Name your product and add a description.
5. Assign the course(s) you want to include in this product.
6. Save your product.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** A single product can contain multiple courses if you want to sell them as a bundle.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 2: Create a Product in WooCommerce
<!-- /wp:heading -->

<!-- wp:paragraph -->
Next, create a corresponding product in WooCommerce that your customers will purchase.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In your WordPress admin, go to **WooCommerce** > **Products** > **Add New**.
2. Enter a product name and description that matches your course.
3. Set the product type. For a one-time purchase, use **Simple product**. For recurring payments, use **Subscription** (requires the WooCommerce Subscriptions extension).
4. Set your price in the **Product data** section.
5. Under the **General** tab, configure any additional pricing options as needed.
6. Publish the product.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** You do not need to set up shipping or inventory for digital course products. Keep your WooCommerce product simple to avoid confusing your customers at checkout.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 3: Configure Access Restrictions in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
Now, connect the WooCommerce product to your Thrive Apprentice product so that purchasing grants course access.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Products** in the left sidebar.
3. Select the product you created in Step 1.
4. Click the **Access requirements** tab.
5. In the access requirements panel, look for the WooCommerce protection options.
6. Select the WooCommerce product you created in Step 2.
7. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
This tells Thrive Apprentice that only users who have purchased the linked WooCommerce product should get access to the course content.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 4: Redirect Users to Course Pages After Purchase
<!-- /wp:heading -->

<!-- wp:paragraph -->
For a smooth customer experience, redirect buyers to their course after completing a WooCommerce purchase.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In WooCommerce, consider adding a custom thank-you page or redirect that points to the course page in Thrive Apprentice.
2. You can use WooCommerce's built-in order confirmation page to include a link to the course.
3. Alternatively, set up an automated email through WooCommerce that includes the direct course URL.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Test the full purchase flow yourself by placing a test order to make sure customers are directed to the right place after checkout.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## How Access Works
<!-- /wp:heading -->

<!-- wp:paragraph -->
Once everything is connected, the workflow looks like this:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. A customer visits your WooCommerce product page and completes a purchase.
2. WooCommerce processes the payment and creates a customer account.
3. Thrive Apprentice detects the completed purchase and grants the customer access to the linked course(s).
4. The customer logs in and sees the course in their Thrive Apprentice dashboard.
<!-- /wp:list -->

<!-- wp:paragraph -->
Access is managed automatically—you don't need to manually enroll students after each purchase.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Troubleshooting
<!-- /wp:heading -->

<!-- wp:list -->
- **Customer can't access the course after purchasing:** Make sure the WooCommerce order status is set to **Completed** or **Processing**. Pending or failed orders won't grant access.
- **WooCommerce product not appearing in access settings:** Verify that WooCommerce is active and that the product is published. Refresh the Thrive Apprentice settings page.
- **Subscription access lost:** If you use WooCommerce Subscriptions, access is tied to the subscription status. Expired or cancelled subscriptions will revoke course access.
<!-- /wp:list -->

<!-- wp:paragraph -->
That's it! You've successfully connected WooCommerce to Thrive Apprentice and created a product that grants course access upon purchase.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Choosing an integration:** [How to Choose the Right Integration for Thrive Apprentice](6-01-choosing-an-integration.md)
- **Stripe setup:** [How to Set Up Stripe in Thrive Apprentice](6-05-setting-up-stripe.md)
- **ThriveCart connection:** [How to Connect ThriveCart to Thrive Apprentice](6-04-connecting-thrivecart.md)
- **Membership plugins:** [How to Integrate Membership Plugins with Thrive Apprentice](6-02-integrating-membership-plugins.md)
<!-- /wp:list -->
