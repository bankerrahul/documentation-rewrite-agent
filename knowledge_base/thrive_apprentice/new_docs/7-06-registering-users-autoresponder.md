<!-- wp:heading {"level":1} -->
# How to Register Users and Add Them to an Autoresponder Simultaneously
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to set up a registration form that creates a WordPress account for new users and subscribes them to your email autoresponder at the same time. This streamlines your onboarding process—new students register, get site access, and join your mailing list in a single step.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Why Combine Registration with an Autoresponder?
<!-- /wp:heading -->

<!-- wp:paragraph -->
When someone signs up for your Thrive Apprentice courses, you typically want two things to happen: a WordPress account gets created so they can access course content, and their email address gets added to your mailing list so you can send welcome sequences, course updates, and promotional offers. Doing both at once saves the user from filling out multiple forms and ensures no leads slip through the cracks.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Prerequisites
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before setting up the combined registration form, make sure you have:
<!-- /wp:paragraph -->

<!-- wp:list -->
- Thrive Apprentice installed and activated with at least one published course
- An email marketing service (e.g., Mailchimp, ActiveCampaign, ConvertKit, AWeber, or any autoresponder supported by Thrive Themes)
- Your email service connected via the **API Connections** in the Thrive Dashboard
<!-- /wp:list -->

<!-- wp:heading -->
## Step 1: Connect Your Email Service
<!-- /wp:heading -->

<!-- wp:paragraph -->
If you haven't already connected your autoresponder, do that first:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **API Connections**.
2. Click **+ Add New Connection**.
3. Select your email marketing service from the list.
4. Enter the required API credentials (API key, secret, or OAuth authorization—depending on the service).
5. Click **Connect** and wait for the confirmation message.
<!-- /wp:list -->

<!-- wp:paragraph -->
Once connected, your email service will be available as an option in Thrive's form elements.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 2: Create the Registration Form
<!-- /wp:heading -->

<!-- wp:paragraph -->
Thrive provides a **Login & Registration** form element that handles both WordPress user creation and autoresponder subscription. Here's how to set it up:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Open the page where you want the registration form to appear using **Thrive Architect** (or the editor of your choice within the Thrive Suite).
2. Add the **Login & Registration** element to your page by dragging it from the element panel.
3. Select the **Registration Form** tab in the element settings.
4. Configure the form fields:
   - **Name** — the user's display name
   - **Email** — used for both the WordPress account and the autoresponder subscription
   - **Password** — the user's chosen password for site login
5. Under the **After Registration** settings, enable the **Add to autoresponder** option.
6. Select your connected email service from the dropdown.
7. Choose the specific **Mailing List** or **Tag** you want new registrants added to.
8. Optionally, map additional form fields to your autoresponder's custom fields (e.g., first name, last name).
9. Save your page.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** You can also add custom fields to the registration form if your autoresponder supports them. This lets you segment new users based on interests, course preferences, or other criteria right from the start.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 3: Configure Post-Registration Behavior
<!-- /wp:heading -->

<!-- wp:paragraph -->
After the form is set up, decide what happens when a user completes registration:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In the **Login & Registration** element settings, scroll to the **After Successful Registration** section.
2. Choose one of the following options:
   - **Redirect to a page** — send the user to a welcome page, course dashboard, or specific course
   - **Show a success message** — display a confirmation message on the same page
   - **Auto-login** — automatically log the user in and redirect them to the course
3. Save your settings.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** If you choose the redirect option, a good destination is your Thrive Apprentice course overview page so new students can start learning immediately.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 4: Test the Form
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before going live, verify that everything works:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Open the page with the registration form in a private/incognito browser window.
2. Fill out the form with a test email address and submit it.
3. Check that a new WordPress user was created under **Users** in the WordPress admin dashboard.
4. Confirm that the test email address appeared in your autoresponder's mailing list.
5. Verify that the post-registration redirect or success message works as expected.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** Use a real email address you control for testing so you can also confirm that the autoresponder's welcome email arrives correctly.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Conclusion
<!-- /wp:heading -->

<!-- wp:paragraph -->
That's it! You've successfully set up a registration form that creates a WordPress account and adds the user to your email autoresponder in one step. This gives your students a smooth onboarding experience while ensuring your mailing list stays in sync with your course enrollment.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **API connections:** [Managing API Connections in Thrive Dashboard](https://thrivethemes.com/docs/api-connections/)
- **Automator recipes:** [How to Use Thrive Automator Recipes with Thrive Apprentice](7-01-automator-recipes.md)
- **Login & Registration element:** [Thrive Architect Login & Registration Documentation](https://thrivethemes.com/docs/login-registration-element/)
- **Course access setup:** [Setting Up Products and Access in Thrive Apprentice](https://thrivethemes.com/docs/thrive-apprentice-products/)
<!-- /wp:list -->
