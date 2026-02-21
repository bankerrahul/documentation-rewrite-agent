<!-- wp:heading {"level":1} -->
# How to Enable the Stripe Customer Portal for Thrive Apprentice Members
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to enable and configure the Stripe Customer Portal so your Thrive Apprentice students can manage their own subscriptions, update payment methods, and view invoices—all without needing to contact you for support.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## What Is the Stripe Customer Portal?
<!-- /wp:heading -->

<!-- wp:paragraph -->
The Stripe Customer Portal is a self-service interface that gives your students direct control over their billing and subscription details. Instead of sending you an email every time they need to update a credit card or cancel a subscription, they can handle it themselves through a secure, Stripe-hosted page.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
When enabled, your students can:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **View active subscriptions** and their renewal dates
- **Update payment methods** (swap credit cards, add new payment sources)
- **Cancel subscriptions** directly
- **View and download invoices** for their payment history
- **Reactivate cancelled subscriptions** (if you allow it)
<!-- /wp:list -->

<!-- wp:paragraph -->
This reduces your support workload and gives students a professional, self-service experience.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Prerequisites
<!-- /wp:heading -->

<!-- wp:list -->
- **Stripe** connected to Thrive Apprentice (see [How to Set Up Stripe in Thrive Apprentice](6-05-setting-up-stripe.md))
- At least one product with Stripe subscription pricing configured
- Students with active Stripe-powered subscriptions
<!-- /wp:list -->

<!-- wp:heading -->
## Step 1: Enable the Customer Portal in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Settings** in the left sidebar.
3. Select **Payment processors** from the settings menu.
4. Find the **Stripe** section and locate the **Customer Portal** toggle.
5. Turn the toggle **On** to enable the Customer Portal.
6. Save your settings.
<!-- /wp:list -->

<!-- wp:paragraph -->
Once enabled, a link to the Customer Portal will become available to your logged-in students.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 2: Configure the Customer Portal in Stripe
<!-- /wp:heading -->

<!-- wp:paragraph -->
You can customize what your students are allowed to do in the Customer Portal directly from your Stripe dashboard.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Log in to your **Stripe dashboard** at [dashboard.stripe.com](https://dashboard.stripe.com).
2. Go to **Settings** > **Billing** > **Customer portal**.
3. Configure the following options:
   - **Payment methods:** Allow customers to update their payment information.
   - **Cancel subscriptions:** Decide whether students can cancel immediately, at end of period, or not at all.
   - **Subscription switching:** Allow or disallow plan changes (e.g., monthly to annual).
   - **Invoice history:** Let customers view and download past invoices.
   - **Promo codes:** Allow customers to apply promotional codes.
4. Save your Customer Portal settings in Stripe.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** If you want to reduce cancellations, consider enabling the "cancel at end of period" option instead of immediate cancellation. This gives students access until their current billing cycle ends, and they may change their mind before then.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 3: Test the Customer Portal
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before your students use it, verify everything works as expected.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Create a test subscription using Stripe's **Test mode** and a test card.
2. Log in to your site as the test student.
3. Navigate to the Customer Portal link within Thrive Apprentice.
4. Verify that the portal loads and displays the correct subscription details.
5. Test updating a payment method and cancelling the subscription.
6. Confirm that Thrive Apprentice updates the student's course access based on the portal actions.
<!-- /wp:list -->

<!-- wp:heading -->
## Where Students Access the Portal
<!-- /wp:heading -->

<!-- wp:paragraph -->
Once the Customer Portal is enabled, students can access it from their account area within Thrive Apprentice. The exact location depends on your site's design, but typically it appears as a **Manage Subscription** or **Billing** link in the student's profile or account page.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Note:** The Customer Portal is hosted by Stripe, so when students click the link, they are taken to a secure Stripe page. After they make any changes, they are redirected back to your website.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## How Portal Actions Affect Course Access
<!-- /wp:heading -->

<!-- wp:paragraph -->
Actions taken in the Customer Portal automatically sync with Thrive Apprentice:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Payment method updated:** No impact on access—the student retains their course access.
- **Subscription cancelled (immediately):** Course access is revoked right away.
- **Subscription cancelled (at end of period):** Course access continues until the end of the current billing cycle, then is revoked.
- **Subscription reactivated:** Course access is restored immediately.
<!-- /wp:list -->

<!-- wp:paragraph -->
That's it! You've successfully enabled the Stripe Customer Portal for your Thrive Apprentice members. Your students can now manage their subscriptions and billing on their own.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Stripe setup:** [How to Set Up Stripe in Thrive Apprentice](6-05-setting-up-stripe.md)
- **Choosing an integration:** [How to Choose the Right Integration for Thrive Apprentice](6-01-choosing-an-integration.md)
- **Square connection:** [How to Connect Square to Thrive Apprentice](6-07-connecting-square.md)
<!-- /wp:list -->
