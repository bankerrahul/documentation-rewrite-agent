<!-- wp:heading {"level":1} -->
# How to Switch to Thrive Apprentice From Another LMS
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to migrate from another learning management system to Thrive Apprentice—including a step-by-step migration checklist, platform-specific tips for switching from LearnDash and Teachable, and how Thrive Apprentice 4.0 features make the transition worthwhile.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Overview of the Migration Process
<!-- /wp:heading -->

<!-- wp:paragraph -->
Switching from another LMS to Thrive Apprentice requires rebuilding your courses within the platform. You cannot directly import course content or structure from another system. However, you can export your existing students and import them into Thrive Apprentice—so your customers won't need to re-register.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Note:** While rebuilding courses may sound like a lot of work, the process is straightforward when you follow a structured approach. The checklist below breaks the migration into seven manageable steps.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Why Switch to Thrive Apprentice?
<!-- /wp:heading -->

<!-- wp:paragraph -->
Thrive Apprentice 4.0 introduced several features that make it a compelling alternative to other LMS platforms:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Products framework** — Protect and sell courses, pages, posts, and custom content as bundled products, enabling full membership site functionality.
- **Drip content scheduling** — Release lessons and modules on a schedule to keep students engaged over time.
- **Conditional display rules** — Show or hide content based on a student's access level, progress, or login status.
- **Built-in design tools** — Customize your entire online school's appearance without code, using the integrated visual editor.
- **No platform fees** — Unlike hosted platforms, Thrive Apprentice runs on your own WordPress site with no per-student or transaction fees.
<!-- /wp:list -->

<!-- wp:heading -->
## The 7-Step Migration Checklist
<!-- /wp:heading -->

<!-- wp:paragraph -->
Follow these seven steps in order to ensure a smooth transition from your current LMS to Thrive Apprentice:
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### Step 1: Create Your Course Content
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click the **Courses** tab and create a new course for each course you're migrating.
3. Recreate your modules, chapters, and lessons within each course.
4. Copy and paste your lesson content from the old platform into each lesson's editor in **Thrive Architect**.
5. Re-upload any media files (images, videos, downloadable resources) that were hosted on the previous platform.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Work through one course at a time to stay organized. Open your old LMS in one browser tab and Thrive Apprentice in another for easy side-by-side content transfer.
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### Step 2: Design Your Online School
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Click the **Design** tab in Thrive Apprentice.
2. Choose a school design template or customize your own.
3. Configure the layout for your course overview pages, lesson pages, and navigation elements.
4. Set up your branding—logo, colors, and typography—to match your existing school's look.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Step 3: Set Up Products and Course Bundles
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Click the **Products** tab in Thrive Apprentice.
2. Create a product for each course or course bundle you want to sell.
3. Associate the appropriate courses with each product.
4. Connect your payment gateway (e.g., ThriveCart, WooCommerce, or SendOwl) to handle purchases.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Step 4: Configure Access Restrictions
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Within each product's settings, define the **Access Requirements**.
2. Set rules for who can access the content—paid students, free users, or specific membership levels.
3. Review your content protection priority to ensure rules don't conflict.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Step 5: Set Up Drip Schedules
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Open the course you want to drip-release.
2. Navigate to the **Drip** settings within the course.
3. Configure when each lesson or module becomes available—based on enrollment date, specific dates, or completion of previous content.
4. Save your drip schedule.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Step 6: Configure Login and Authentication
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Set up a **Login Page** for your students (or use the default WordPress login).
2. Optionally, create a **Registration Page** if you want new students to sign up directly on your site.
3. Configure any SSO (Single Sign-On) integrations if your old platform used external authentication.
4. Test the login flow from a student's perspective.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Step 7: Import Your Existing Customers
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Export your student list from your current LMS (typically as a CSV file).
2. In Thrive Apprentice, go to the **Members** tab and click the **Import member** button.
3. Upload the CSV file containing your student data.
4. Map the CSV fields to Thrive Apprentice fields (name, email, purchased products, etc.).
5. Run the import and verify that students appear with the correct product access.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** After importing, send an email to your existing students letting them know about the platform change. Include their new login URL and instructions for accessing their courses.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Switching From LearnDash
<!-- /wp:heading -->

<!-- wp:paragraph -->
If you're currently using LearnDash, the migration to Thrive Apprentice has a notable advantage: since both platforms run on WordPress, your student accounts already exist as WordPress users. This simplifies the process significantly.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Platform-specific tips for LearnDash users:**
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Student transfer is straightforward** — You can pull in all your students from LearnDash to Thrive Apprentice without requiring them to re-register, since they already have WordPress user accounts on your site.
- **Content lives on the same site** — Your lesson content (text, images, embedded videos) is already in WordPress, so copying it into Thrive Apprentice lessons is faster than migrating from an external platform.
- **Course structure mapping** — LearnDash uses Courses, Lessons, Topics, and Quizzes. Map these to Thrive Apprentice's Courses, Modules, Chapters, and Lessons respectively.
- **Payment integration** — If you used WooCommerce with LearnDash, you can continue using it with Thrive Apprentice for payment processing.
- **Deactivate LearnDash last** — Keep LearnDash active until your Thrive Apprentice courses are fully set up and tested. Once you've verified everything works, deactivate the LearnDash plugin.
<!-- /wp:list -->

<!-- wp:heading -->
## Switching From Teachable
<!-- /wp:heading -->

<!-- wp:paragraph -->
Teachable is a hosted platform, which means your course content lives on Teachable's servers—not on your WordPress site. This requires a few extra steps during migration.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Platform-specific tips for Teachable users:**
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Export your student list** — Teachable allows you to export your student data as a CSV file. Download this before starting the migration, as you'll need it to import students into Thrive Apprentice.
- **Download all media** — Since your videos, images, and files are hosted on Teachable, download everything to your computer before cancelling your Teachable subscription.
- **Recreate course content manually** — You'll need to transfer your lesson content by copying text and re-uploading media into Thrive Apprentice's lesson editor via Thrive Architect.
- **Redirect your domain** — If you used a custom domain on Teachable, update your DNS settings to point to your WordPress site instead.
- **No per-student fees** — One of the biggest advantages of switching is eliminating Teachable's transaction fees. With Thrive Apprentice, you keep 100% of your revenue (minus payment processor fees).
- **Maintain access during transition** — Keep your Teachable account active until all content is migrated and all students have been notified of the change.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Warning:** Do not cancel your Teachable subscription until you have exported all student data, downloaded all media files, and verified that your Thrive Apprentice courses are fully operational.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
That's it! You've successfully learned how to plan and execute a migration from another LMS to Thrive Apprentice—using the 7-step checklist for a structured approach, with platform-specific guidance for LearnDash and Teachable users.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Creating Your First Course:** Learn how to [create your first Thrive Apprentice course](#) from scratch.
- **Course Bundles:** Learn how to [create course bundles](#) to package multiple courses together.
- **Access Restrictions:** Explore how to [set up access restrictions and rules](#) to protect your content.
- **Student Profile Pages:** Learn how to [create a student profile page](#) so migrated students can manage their accounts.
- **Thrive Apprentice Knowledge Base:** Browse the full [Thrive Apprentice Knowledge Base](https://thrivethemes.com/docs-categories/thrive-apprentice/) for more tutorials.
<!-- /wp:list -->
