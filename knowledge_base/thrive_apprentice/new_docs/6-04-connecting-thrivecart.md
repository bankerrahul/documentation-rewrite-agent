<!-- wp:heading {"level":1} -->
# How to Connect ThriveCart to Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to connect your ThriveCart account to Thrive Apprentice using an API key, and then set up access restriction rules so that ThriveCart purchases automatically grant course access to your customers.
<!-- /wp:paragraph -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=oDPQy94Nl3E","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=oDPQy94Nl3E
<!-- /wp:embed -->

<!-- wp:paragraph -->
**Important:** ThriveCart is an independent company and is not affiliated with Thrive Themes. You need a paid ThriveCart account to use this integration.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Part 1: Generate an API Key in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
The connection between ThriveCart and Thrive Apprentice is powered by an API key. You'll generate this key inside Thrive Apprentice and then add it to ThriveCart.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Settings** in the left sidebar.
3. Select **API keys** from the settings menu.
4. Click **Add API** to generate a new API key.
5. Copy the generated API key—you'll need it in the next step.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Give your API key a descriptive name like "ThriveCart Connection" so you can identify it later if you create multiple keys.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Part 2: Add the API Key in ThriveCart
<!-- /wp:heading -->

<!-- wp:paragraph -->
Now take the API key you just generated and enter it into your ThriveCart account to establish the connection.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Log in to your **ThriveCart** account.
2. Navigate to **Settings** > **API & Webhooks** (or the equivalent section in your ThriveCart dashboard).
3. Look for the Thrive Apprentice integration option.
4. Paste the API key you copied from Thrive Apprentice.
5. Enter your website URL when prompted.
6. Save the connection.
<!-- /wp:list -->

<!-- wp:paragraph -->
Once saved, ThriveCart and Thrive Apprentice can communicate with each other. When a customer completes a purchase through ThriveCart, the system will notify Thrive Apprentice to grant course access.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Note:** Some older video tutorials may show a toggle labeled "Gives access based on your ThriveCart setup." This toggle has been removed from the current interface. The connection works automatically once the API key is configured.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Part 3: Set Up Access Restriction Rules
<!-- /wp:heading -->

<!-- wp:paragraph -->
With the connection established, you now need to tell Thrive Apprentice which ThriveCart products should grant access to which courses.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Products** in the left sidebar.
3. Select the product that contains the course(s) you want to protect.
4. Click the **Access requirements** tab.
5. In the access requirements panel, locate the ThriveCart protection options.
6. Select the ThriveCart product that should grant access to this Thrive Apprentice product.
7. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
This links the two products together. When a customer buys the ThriveCart product, they'll automatically receive access to the associated Thrive Apprentice course.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## How the Access Flow Works
<!-- /wp:heading -->

<!-- wp:paragraph -->
Once everything is configured, here's what happens from your customer's perspective:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. The customer visits your ThriveCart checkout page and completes the purchase.
2. ThriveCart processes the payment and sends a notification to Thrive Apprentice via the API.
3. Thrive Apprentice creates a user account (if one doesn't exist) and grants access to the linked course(s).
4. The customer receives an email with login details and can access the course immediately.
<!-- /wp:list -->

<!-- wp:paragraph -->
The entire process is automatic—no manual enrollment needed on your end.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Managing Access
<!-- /wp:heading -->

<!-- wp:paragraph -->
ThriveCart handles billing, refunds, and cancellations. When billing events occur:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Refund processed in ThriveCart:** Course access is revoked in Thrive Apprentice.
- **Subscription cancelled:** Access is removed based on your cancellation settings.
- **Subscription renewed:** Access continues automatically.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Test the full flow by making a test purchase through ThriveCart to confirm that access is granted correctly in Thrive Apprentice.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Troubleshooting
<!-- /wp:heading -->

<!-- wp:list -->
- **ThriveCart products not appearing in access settings:** Make sure the API key is correctly entered in both systems and that the connection is active. Try regenerating the API key if needed.
- **Customer didn't receive access:** Check that the ThriveCart product is linked to the correct Thrive Apprentice product in the **Access requirements** tab. Also verify the customer's email matches in both systems.
- **API connection failed:** Confirm your website URL is entered correctly in ThriveCart and that your site is accessible (not in maintenance mode).
<!-- /wp:list -->

<!-- wp:paragraph -->
That's it! You've successfully connected ThriveCart to Thrive Apprentice and configured access restriction rules so your customers get instant course access after purchase.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Choosing an integration:** [How to Choose the Right Integration for Thrive Apprentice](6-01-choosing-an-integration.md)
- **Stripe setup:** [How to Set Up Stripe in Thrive Apprentice](6-05-setting-up-stripe.md)
- **WooCommerce setup:** [How to Get Started with WooCommerce and Thrive Apprentice](6-03-getting-started-woocommerce.md)
- **Square connection:** [How to Connect Square to Thrive Apprentice](6-07-connecting-square.md)
<!-- /wp:list -->
