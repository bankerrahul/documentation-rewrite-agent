<!-- wp:heading {"level":1} -->
# How to Connect Square to Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to connect your Square payment processor to Thrive Apprentice so you can sell courses and restrict access to paying customers. This guide covers connecting your Square account, setting up a sandbox for testing, creating items, configuring webhooks, and displaying the buy button.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Prerequisites
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before you begin, make sure you have:
<!-- /wp:paragraph -->

<!-- wp:list -->
- A **Square account** (create one at [squareup.com](https://squareup.com) if you don't have one)
- **Thrive Apprentice** installed and activated on your WordPress site
- At least one course created in Thrive Apprentice
<!-- /wp:list -->

<!-- wp:heading -->
## Step 1: Connect Your Square Account
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Settings** in the left sidebar.
3. Select **Payment processors** from the settings menu.
4. Find the **Square** option and click **Connect**.
5. You'll be redirected to Square's authorization page. Log in to your Square account.
6. Authorize the connection by granting Thrive Apprentice the required permissions.
7. Once authorized, you'll be redirected back to Thrive Apprentice with a confirmation message.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Square offers both a live environment and a sandbox environment. Start with the sandbox to test your setup before accepting real payments.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 2: Connect Your Square Sandbox (Optional but Recommended)
<!-- /wp:heading -->

<!-- wp:paragraph -->
Testing with Square's sandbox lets you simulate purchases without processing real transactions.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Log in to the **Square Developer Dashboard** at [developer.squareup.com](https://developer.squareup.com).
2. Create or select a sandbox application.
3. Copy your **Sandbox Application ID** and **Sandbox Access Token**.
4. In Thrive Apprentice, go to **Settings** > **Payment processors** > **Square**.
5. Toggle to **Sandbox mode** and enter your sandbox credentials.
6. Save your settings.
<!-- /wp:list -->

<!-- wp:paragraph -->
You can now test the full purchase flow with sandbox credentials before going live.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 3: Create an Item in Your Square Account
<!-- /wp:heading -->

<!-- wp:paragraph -->
You need to create an item in Square that corresponds to your Thrive Apprentice course product.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Log in to your **Square dashboard**.
2. Go to **Items** (or **Item Library**).
3. Click **Create an Item**.
4. Enter a name and description that matches your course product.
5. Set the price for the item.
6. Save the item.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** The item you create in Square is what your customers will be charged for. Make sure the name and price align with the course product you've set up in Thrive Apprentice.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 4: Create a Webhook in Square
<!-- /wp:heading -->

<!-- wp:paragraph -->
Webhooks allow Square to notify Thrive Apprentice when a payment is completed, so course access can be granted automatically.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to the **Square Developer Dashboard**.
2. Select your application.
3. Navigate to **Webhooks** in the left sidebar.
4. Click **Add Webhook** (or **Subscribe to Events**).
5. Enter the webhook URL provided by Thrive Apprentice. You'll find this in **Settings** > **Payment processors** > **Square** within Thrive Apprentice.
6. Select the relevant events to subscribe to—at minimum, subscribe to **payment.completed** events.
7. Save the webhook.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** The webhook URL must be accessible from the internet. If your site is behind a firewall or in maintenance mode, Square won't be able to send notifications, and course access won't be granted.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 5: Configure Access Restrictions
<!-- /wp:heading -->

<!-- wp:paragraph -->
Now link your Square item to a Thrive Apprentice product so that purchases trigger access.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Products** in the left sidebar.
3. Select the product you want to protect.
4. Click the **Access requirements** tab.
5. Choose **Square** as the payment method.
6. Select the Square item you created in Step 3.
7. Save your changes.
<!-- /wp:list -->

<!-- wp:heading -->
## Step 6: Display the Square Buy Button
<!-- /wp:heading -->

<!-- wp:paragraph -->
To let your customers make purchases, you need to display a buy button on your course or product page.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Open the course or product page in **Thrive Architect** (or your page editor).
2. Add or configure the purchase button element.
3. Link the button to the Square checkout for the item you've set up.
4. Save and publish the page.
<!-- /wp:list -->

<!-- wp:paragraph -->
When a customer clicks the buy button, they'll be taken through the Square checkout process. After successful payment, Thrive Apprentice grants them access to the course.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 7: Set Up Transactional Emails
<!-- /wp:heading -->

<!-- wp:paragraph -->
Make sure your customers receive confirmation emails after their purchase.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In Thrive Apprentice, go to **Settings** > **Email notifications** (or your email settings).
2. Verify that transactional emails are enabled for new enrollments and purchases.
3. Customize the email content if needed—include the course name, login link, and any getting-started instructions.
4. Send a test email to confirm everything looks correct.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** A well-crafted welcome email improves the student experience and reduces support questions about how to access the course.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Troubleshooting
<!-- /wp:heading -->

<!-- wp:list -->
- **Square connection failed:** Verify you're logged in to the correct Square account and that you've granted all required permissions. Try disconnecting and reconnecting.
- **Webhook not firing:** Confirm the webhook URL is correct in the Square Developer Dashboard and that your site is publicly accessible. Check the webhook logs in Square for error details.
- **Customer didn't receive access:** Verify that the Square item is linked to the correct Thrive Apprentice product in the **Access requirements** tab. Check Square's transaction history to confirm the payment was successful.
- **Sandbox not working:** Make sure you've entered the correct sandbox credentials and that you're testing with Square's sandbox test data.
<!-- /wp:list -->

<!-- wp:paragraph -->
That's it! You've successfully connected Square to Thrive Apprentice and configured it to sell courses with automatic access provisioning.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Choosing an integration:** [How to Choose the Right Integration for Thrive Apprentice](6-01-choosing-an-integration.md)
- **Stripe setup:** [How to Set Up Stripe in Thrive Apprentice](6-05-setting-up-stripe.md)
- **Stripe Customer Portal:** [How to Enable the Stripe Customer Portal for Thrive Apprentice Members](6-06-stripe-customer-portal.md)
- **WooCommerce setup:** [How to Get Started with WooCommerce and Thrive Apprentice](6-03-getting-started-woocommerce.md)
<!-- /wp:list -->
