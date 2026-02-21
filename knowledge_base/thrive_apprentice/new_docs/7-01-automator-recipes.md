<!-- wp:heading {"level":1} -->
# How to Use Thrive Automator Recipes with Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to use Thrive Automator alongside Thrive Apprentice to build powerful automation workflows. From enrolling students after a quiz to revoking access after a trial period, these ready-made recipes cover the most common scenarios you'll encounter as a course creator.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
Each recipe below includes the trigger, the action, and the steps you need to set it up. Pick the one that matches your use case and follow along.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Getting Started with Thrive Automator + Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
Thrive Automator is the automation engine that connects Thrive Apprentice with other plugins and services on your WordPress site. It works on a simple principle: a **Start Trigger** fires when something happens, and one or more **Actions** execute automatically in response.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
To access Thrive Automator, navigate to **Thrive Dashboard** > **Thrive Automator**. From there, click **+ Add New** to create a new automation. Every recipe in this guide follows that same starting point.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Note:** Make sure you have at least one published Thrive Apprentice course linked to a product before creating automations. The triggers and actions below rely on your courses and products being properly configured.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Recipe 1: Enroll Users in a Course Only After They Pass a Quiz
<!-- /wp:heading -->

<!-- wp:paragraph -->
**What it does:** Automatically grants course access to students who achieve a passing score on a Thrive Quiz Builder test. This ensures only qualified learners move forward.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Trigger:** User completes a quiz (Thrive Quiz Builder)
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Action:** Grant access to a Thrive Apprentice product
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Automator** and click **+ Add New**.
2. Set the **Start Trigger** to **User completes quiz**.
3. Choose the specific quiz from the dropdown.
4. Add a **Filter** to check that the user's score meets your passing threshold.
5. Add an **Action** and select **Grant access to product**.
6. Choose the Thrive Apprentice product that contains your course.
7. Click **Save and Activate** to enable the automation.
<!-- /wp:list -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=pYUROK7nKnE","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=pYUROK7nKnE
<!-- /wp:embed -->

<!-- wp:heading -->
## Recipe 2: Notify Students When New Content Is Unlocked
<!-- /wp:heading -->

<!-- wp:paragraph -->
**What it does:** Sends an email notification to students whenever new lessons become available through a drip schedule. This keeps learners engaged and coming back to your course.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Trigger:** Thrive Apprentice lesson becomes available (via drip schedule)
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Action:** Send email notification or tag user in autoresponder
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. First, ensure your course uses a **Drip Schedule** to release content over time. Configure this under **Thrive Dashboard** > **Thrive Apprentice** > **Courses** > your course > **Drip**.
2. Go to **Thrive Dashboard** > **Thrive Automator** and click **+ Add New**.
3. Set the **Start Trigger** to **Lesson becomes available**.
4. Select the course from the dropdown.
5. Add an **Action** and choose **Send email notification** or tag the user in your connected autoresponder to trigger a campaign.
6. Customize the email content or tag name.
7. Click **Save and Activate**.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Set up a campaign in your autoresponder ahead of time so that tagging the user automatically sends a well-designed email with a link back to the newly unlocked lesson.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Recipe 3: Revoke Course Access After a Certain Period
<!-- /wp:heading -->

<!-- wp:paragraph -->
**What it does:** Automatically removes a student's access to a course after a set number of days. This is ideal for time-limited courses, seasonal programs, or subscription-based access models.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Trigger:** User receives access to a Thrive Apprentice product
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Action:** Delay + Remove access from product
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Automator** and click **+ Add New**.
2. Set the **Start Trigger** to **User receives access to product**.
3. Select the relevant Thrive Apprentice product.
4. Add a **Delay** action and set the duration (e.g., 30 days, 90 days).
5. After the delay, add an **Action** and select **Remove access from product**.
6. Choose the same product you selected in the trigger.
7. Click **Save and Activate**.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** Once access is revoked, the student will no longer see the course content. If you want to offer a renewal option, consider sending a reminder email a few days before the access period ends using a separate automation.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Recipe 4: Grant Access to Multiple Free Courses at Once
<!-- /wp:heading -->

<!-- wp:paragraph -->
**What it does:** Enrolls a new user in several free courses simultaneously when they register on your site or complete a specific action. This is perfect for onboarding sequences or free course bundles.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Trigger:** User registers on site (or a custom trigger of your choice)
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Action:** Grant access to multiple Thrive Apprentice products
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Automator** and click **+ Add New**.
2. Set the **Start Trigger** to **User registers** (or another trigger that fits your workflow).
3. Add an **Action** and select **Grant access to product**. Choose your first free course product.
4. Click **+ Add another action** and select **Grant access to product** again. Choose your second free course product.
5. Repeat for each additional free course you want to include.
6. Click **Save and Activate**.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** You can also bundle multiple courses into a single Thrive Apprentice product. However, using separate actions gives you more flexibility to add or remove individual courses from the bundle later.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Recipe 5: Unlock a Premium Lesson When a User Completes a Free Course
<!-- /wp:heading -->

<!-- wp:paragraph -->
**What it does:** When a student finishes a free course, this automation automatically grants them access to the first lesson of a premium course—giving them a taste of paid content and encouraging an upgrade.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Trigger:** User completes a course in Thrive Apprentice
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Action:** Grant access to a premium product (with restricted content)
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Create a premium course with its first lesson accessible and remaining content locked behind a purchase.
2. Go to **Thrive Dashboard** > **Thrive Automator** and click **+ Add New**.
3. Set the **Start Trigger** to **User completes course**.
4. Select the free course from the dropdown.
5. Add an **Action** and select **Grant access to product**.
6. Choose the premium course product. Configure it so the user receives access only to the introductory content.
7. Click **Save and Activate**.
<!-- /wp:list -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=AgOkqLlKqUE","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=AgOkqLlKqUE
<!-- /wp:embed -->

<!-- wp:heading -->
## Recipe 6: Remove Users from a Premium Course After a Free Trial Expires
<!-- /wp:heading -->

<!-- wp:paragraph -->
**What it does:** Gives users temporary access to a premium course for a trial period, then automatically removes them when the trial ends. This is a great way to let prospects preview your paid content.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Trigger:** User receives access to a Thrive Apprentice product
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Action:** Delay + Remove access from product
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Automator** and click **+ Add New**.
2. Set the **Start Trigger** to **User receives access to product**.
3. Select the premium course product you're offering as a trial.
4. Add a **Delay** action and specify the trial duration (e.g., 7 days, 14 days).
5. After the delay, add an **Action** and select **Remove access from product**.
6. Choose the same premium product.
7. Click **Save and Activate**.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Pair this with a separate automation that sends a reminder email 1–2 days before the trial expires, encouraging the user to purchase full access.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Recipe 7: Send a Thank-You Email After a Course Purchase
<!-- /wp:heading -->

<!-- wp:paragraph -->
**What it does:** Automatically sends a personalized thank-you email when someone purchases a Thrive Apprentice product. This improves the customer experience and builds trust right from the start.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Trigger:** User purchases a Thrive Apprentice product
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Action:** Send email notification
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Automator** and click **+ Add New**.
2. Set the **Start Trigger** to **User purchases product**.
3. Select the Thrive Apprentice product from the dropdown.
4. Add an **Action** and select **Send email notification**.
5. Write your thank-you message in the email body. Include the course name, login link, and any getting-started instructions.
6. Click **Save and Activate**.
<!-- /wp:list -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=I9YzC0-kgD0","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=I9YzC0-kgD0
<!-- /wp:embed -->

<!-- wp:paragraph -->
**Tip:** You can also tag the user in your autoresponder and trigger a full welcome email sequence instead of a single message.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Recipe 8: Send a Discount Code After a Course Is Purchased
<!-- /wp:heading -->

<!-- wp:paragraph -->
**What it does:** Rewards buyers with a discount code for another course immediately after they complete a purchase. This drives upsells and increases customer lifetime value.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Trigger:** User purchases a Thrive Apprentice product
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Action:** Tag user in autoresponder + Send email with discount code
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Create a discount code in your payment or coupon system for the upsell course.
2. Set up an email in your autoresponder that contains the discount code and a link to the upsell course sales page.
3. Go to **Thrive Dashboard** > **Thrive Automator** and click **+ Add New**.
4. Set the **Start Trigger** to **User purchases product**.
5. Select the Thrive Apprentice product from the dropdown.
6. Add an **Action** and choose **Tag user in autoresponder**. Select the tag that triggers your discount email campaign.
7. Click **Save and Activate**.
<!-- /wp:list -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=7B46GBmqNXU","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=7B46GBmqNXU
<!-- /wp:embed -->

<!-- wp:heading -->
## Recipe 9: Grant Access via Digistore24 Purchases
<!-- /wp:heading -->

<!-- wp:paragraph -->
**What it does:** Connects Digistore24 product purchases to Thrive Apprentice enrollment. When a customer buys a product through Digistore24, they automatically receive access to the corresponding Thrive Apprentice course.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Trigger:** Digistore24 purchase (via IPN or webhook)
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Action:** Grant access to a Thrive Apprentice product
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Ensure the Digistore24 integration is connected in **Thrive Dashboard** > **Thrive Automator** > **Connections**.
2. Click **+ Add New** to create a new automation.
3. Set the **Start Trigger** to the Digistore24 purchase event.
4. Use **Advanced Data Mapping** to map the Digistore24 product to the correct Thrive Apprentice product. This is especially important if you sell multiple products through Digistore24.
5. Add an **Action** and select **Grant access to product**.
6. Choose the corresponding Thrive Apprentice product.
7. Click **Save and Activate**.
<!-- /wp:list -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=IVAk9XtFtEI","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=IVAk9XtFtEI
<!-- /wp:embed -->

<!-- wp:paragraph -->
**Note:** If you sell multiple Digistore24 products that each map to a different Thrive Apprentice course, you'll need to create a separate automation for each product-to-course mapping—or use advanced data mapping to handle multiple mappings within a single automation.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Conclusion
<!-- /wp:heading -->

<!-- wp:paragraph -->
That's it! You've successfully explored nine Thrive Automator recipes for Thrive Apprentice. Whether you're gating courses behind quizzes, offering free trials, or automating post-purchase emails, these workflows save you time and deliver a seamless experience for your students.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
Mix and match these recipes to fit your specific course business model. You can always duplicate and modify an existing automation to create new variations.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Getting started with Thrive Automator:** [Thrive Automator documentation](https://thrivethemes.com/docs/thrive-automator/)
- **Using quizzes with Thrive Apprentice:** [How to Use Quizzes in Thrive Apprentice](7-02-using-quizzes.md)
- **Setting up drip schedules:** [Thrive Apprentice Drip Content documentation](https://thrivethemes.com/docs/thrive-apprentice-drip/)
- **Digistore24 integration:** [Connecting Digistore24 to Thrive Automator](https://thrivethemes.com/docs/digistore24-thrive-automator/)
<!-- /wp:list -->
