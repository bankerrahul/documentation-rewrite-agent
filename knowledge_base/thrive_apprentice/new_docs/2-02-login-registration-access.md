<!-- wp:heading {"level":1} -->
# How to Set Up Login, Registration, and Access Restrictions
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to configure login and registration pages, set up access restriction rules, manage what non-logged-in visitors see when they encounter restricted content, and register new users in Thrive Apprentice.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Prerequisites
<!-- /wp:heading -->

<!-- wp:list -->
- At least one course created in Thrive Apprentice.
- At least one product set up, since access restrictions are applied at the product level.
<!-- /wp:list -->

<!-- wp:heading -->
## Understanding How Access Restrictions Work
<!-- /wp:heading -->

<!-- wp:paragraph -->
Access restrictions in Thrive Apprentice operate at the **product level**, not at the individual course level. You create products that contain one or more courses, then apply restriction rules to those products. This approach gives you flexible control—you can bundle multiple courses into a single product and manage access for all of them at once.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
When a visitor tries to access a course or lesson they don't have permission to view, Thrive Apprentice displays a customizable message based on the restriction settings you've configured. The **Login & Access Restriction** settings apply globally to all Thrive Apprentice products on your website.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Setting Up a Login and Registration Page
<!-- /wp:heading -->

<!-- wp:paragraph -->
A dedicated login and registration page gives your students a clear entry point to access course content. Here's how to set one up:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Settings** in the left sidebar.
3. Select the **Login & Access Restriction** tab.
4. In the **Login Page** section, click **Add a Login Page** (or select an existing page from the dropdown).
5. Customize your login page settings—including form fields, branding, and redirect behavior.
6. In the **Registration** section, enable registration if you want new users to create accounts on their own.
7. Configure registration fields and any welcome email preferences.
8. Click **Save** to apply your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Use the Thrive Architect visual editor to design a professional-looking login and registration page that matches your site's branding.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Configuring Access Restriction Rules
<!-- /wp:heading -->

<!-- wp:paragraph -->
Access restriction rules determine who can view your course content. You can restrict access so that only subscribers, purchasers, or specific user roles can access your products.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice** > **Settings**.
2. Open the **Login & Access Restriction** tab.
3. Scroll to the **Access Restriction Rules** section.
4. Choose how you want to restrict content. Common options include:
<!-- /wp:list -->

<!-- wp:list -->
- **Logged-in users only** — Only users with a WordPress account can view the content.
- **Product purchasers** — Only users who have purchased or been granted access to a specific product.
- **Specific user roles** — Restrict access based on WordPress user roles such as Subscriber, Customer, or a custom role.
<!-- /wp:list -->

<!-- wp:list {"ordered":true} -->
5. Configure the **restriction message** that visitors see when they don't have access. This message can include a link to your login or purchase page.
6. Click **Save** to apply the rules.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** These global restriction rules apply to all products. If you need different rules for individual products, you can override them at the product level by navigating to the specific product's settings.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## What Non-Logged-In Users See
<!-- /wp:heading -->

<!-- wp:paragraph -->
When a visitor who isn't logged in—or doesn't have the right permissions—tries to access restricted content, Thrive Apprentice shows them a restriction message. You have full control over what this message says and where it directs the visitor.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
To customize the restriction message:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Open **Settings** > **Login & Access Restriction**.
2. Locate the **Restricted Content Message** area.
3. Edit the text to communicate what the visitor needs to do—whether that's logging in, registering, or purchasing access.
4. Optionally, include a link or button that directs visitors to your login page, registration form, or sales page.
5. Click **Save**.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Keep your restriction message helpful rather than generic. Instead of "Access denied," try something like "This course is available to members. Log in or sign up to get started!"
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Registering New Users
<!-- /wp:heading -->

<!-- wp:paragraph -->
There are two primary ways to register new learners in Thrive Apprentice:
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### Self-Registration
<!-- /wp:heading -->

<!-- wp:paragraph -->
When registration is enabled, visitors can sign up directly from your login/registration page. After registering, they receive a welcome email with their login credentials and can immediately begin accessing any courses included in their product access.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Ensure registration is enabled under **Settings** > **Login & Access Restriction**.
2. Verify that your registration page is published and accessible.
3. When a visitor registers, Thrive Apprentice creates a new WordPress user account for them.
4. The new user receives a welcome email with their login details.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Manually Granting Access
<!-- /wp:heading -->

<!-- wp:paragraph -->
As an administrator, you can also manually add users and grant them access to specific products:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to the **Members** section in Thrive Apprentice.
2. Click **Add Member** or locate an existing WordPress user.
3. Select the products you want to grant them access to.
4. Save the changes. The user now has access to all courses within those products.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** When you grant access manually, the user must already have a WordPress account. If they don't, create one first under **Users** > **Add New** in your WordPress admin dashboard.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Conclusion
<!-- /wp:heading -->

<!-- wp:paragraph -->
That's it! You've successfully set up login and registration pages, configured access restriction rules, customized restriction messages, and learned how to register new users. Your Thrive Apprentice courses are now properly secured and accessible to the right audience.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Settings overview** — [How to Navigate and Configure Thrive Apprentice Settings](2-01-settings-guide.md)
- **Member management** — [How to Manage Members in Thrive Apprentice](2-04-managing-members.md)
- **Course management** — [How to Manage Course Status and Bulk Actions](2-03-managing-courses.md)
<!-- /wp:list -->
