<!-- wp:heading {"level":1} -->
# How to Set Up Stripe in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to connect your Stripe account to Thrive Apprentice so you can accept payments and sell courses directly from your website—no extra plugins required.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
Stripe is the built-in payment solution for Thrive Apprentice. It's the simplest way to start selling courses because everything is managed from within the Thrive Apprentice dashboard—payment processing, product creation, and access control.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Prerequisites
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before you begin, make sure you have:
<!-- /wp:paragraph -->

<!-- wp:list -->
- A **Stripe account** (create one for free at [stripe.com](https://stripe.com) if you don't have one)
- **Thrive Apprentice** installed and activated on your WordPress site
- At least one course created in Thrive Apprentice
<!-- /wp:list -->

<!-- wp:heading -->
## Step 1: Connect Your Stripe Account
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Settings** in the left sidebar.
3. Select **Payment processors** from the settings menu.
4. Click the **Connect with Stripe** button.
5. You'll be redirected to Stripe's authorization page. Log in to your Stripe account (or create one if needed).
6. Authorize the connection by granting Thrive Apprentice access to your Stripe account.
7. Once authorized, you'll be redirected back to Thrive Apprentice. A success message confirms the connection.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** You can connect in either **Live mode** or **Test mode**. Use Test mode first to verify everything works before accepting real payments. You can switch modes at any time from the payment processor settings.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 2: Create a Product with Stripe Pricing
<!-- /wp:heading -->

<!-- wp:paragraph -->
With Stripe connected, you can now add pricing directly to your Thrive Apprentice products.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Products** in the left sidebar.
3. Select an existing product or click **Add New** to create one.
4. Click the **Access requirements** tab.
5. Choose **Stripe** as the payment method.
6. Configure your pricing:
   - **One-time payment:** Set a single price for lifetime access.
   - **Subscription:** Set a recurring price (monthly, yearly, or custom interval).
   - **Free trial:** Optionally add a trial period before billing begins.
7. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
You can create multiple pricing options for the same product—for example, a monthly subscription and an annual subscription—giving your customers the flexibility to choose.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 3: Configure Payment Settings
<!-- /wp:heading -->

<!-- wp:paragraph -->
Fine-tune how payments are handled in your Thrive Apprentice setup.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Settings** > **Payment processors** in Thrive Apprentice.
2. Review the following settings:
   - **Currency:** Set the currency you want to charge in (USD, EUR, GBP, etc.).
   - **Success page:** Choose where customers are redirected after a successful payment.
   - **Cancellation behavior:** Decide what happens when a subscription is cancelled—immediate access revocation or access until the end of the billing period.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** Stripe handles all PCI compliance, secure card processing, and payment security. You don't need to worry about storing sensitive payment data on your server.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## How Access Works with Stripe
<!-- /wp:heading -->

<!-- wp:paragraph -->
Once Stripe is set up, the customer experience looks like this:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. A visitor clicks the purchase button on your course or product page.
2. A Stripe checkout form appears (either embedded on your page or as a Stripe-hosted page).
3. The customer enters their payment information and completes the purchase.
4. Stripe processes the payment and notifies Thrive Apprentice.
5. Thrive Apprentice automatically creates a user account (if needed) and grants course access.
6. The customer can immediately start learning.
<!-- /wp:list -->

<!-- wp:paragraph -->
For subscriptions, Stripe automatically handles recurring billing. If a payment fails or a subscription is cancelled, Thrive Apprentice updates the customer's access accordingly.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Testing Your Setup
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before going live, test the entire purchase flow:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Switch your Stripe connection to **Test mode** in the payment processor settings.
2. Use Stripe's test card number (4242 4242 4242 4242) with any future expiration date and any CVC.
3. Complete a test purchase on your site.
4. Verify that course access was granted to the test account.
5. Switch back to **Live mode** when you're ready to accept real payments.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** Always test in Test mode before enabling Live mode. This ensures your checkout flow, access rules, and email notifications all work correctly without processing real charges.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Troubleshooting
<!-- /wp:heading -->

<!-- wp:list -->
- **Stripe connection failed:** Make sure you're logged in to the correct Stripe account and that you've authorized the connection. Try disconnecting and reconnecting.
- **Payment not processing:** Verify you're in Live mode (not Test mode) if you're trying to accept real payments. Check that your Stripe account is fully activated with all required verification completed.
- **Customer didn't receive access:** Confirm the product has Stripe pricing configured in the **Access requirements** tab. Check the Stripe dashboard to verify the payment was successful.
- **Webhook errors:** Thrive Apprentice relies on Stripe webhooks to receive payment notifications. If your hosting provider has a strict firewall, you may need to whitelist Stripe's webhook IP addresses.
<!-- /wp:list -->

<!-- wp:paragraph -->
That's it! You've successfully connected Stripe to Thrive Apprentice and can now sell courses with automated payment processing and access management.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Stripe Customer Portal:** [How to Enable the Stripe Customer Portal for Thrive Apprentice Members](6-06-stripe-customer-portal.md)
- **Choosing an integration:** [How to Choose the Right Integration for Thrive Apprentice](6-01-choosing-an-integration.md)
- **WooCommerce setup:** [How to Get Started with WooCommerce and Thrive Apprentice](6-03-getting-started-woocommerce.md)
- **ThriveCart connection:** [How to Connect ThriveCart to Thrive Apprentice](6-04-connecting-thrivecart.md)
<!-- /wp:list -->
