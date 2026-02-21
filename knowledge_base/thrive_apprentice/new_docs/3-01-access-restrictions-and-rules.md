<!-- wp:heading {"level":1} -->
# How to Set Up Access Restrictions and Rules in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to control who can access your course content using Thrive Apprentice's access restriction system. This comprehensive guide covers everything from basic content protection to advanced multi-product restriction rules, dynamic labels, and overrides for non-logged-in users.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## What Are Access Restrictions?
<!-- /wp:heading -->

<!-- wp:paragraph -->
Access restrictions are rules you define to control who can view your courses, lessons, and other protected content. When a visitor doesn't meet the requirements you've set, Thrive Apprentice automatically blocks them from viewing the restricted material and displays a customizable message instead.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
You can use access restrictions to sell courses behind a product, create subscribers-only content, gate premium lessons, or build complex membership tiers—all without additional plugins.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Protecting Course Overview Pages
<!-- /wp:heading -->

<!-- wp:paragraph -->
A course overview page displays key details about your course—learning outcomes, lesson listings, and other important information. By default, this page is visible to everyone. However, you may want to restrict it so only enrolled students or paying members can see the full details.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
To protect a course overview page:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice**.
2. Select **Courses** from the left sidebar and click on the course you want to protect.
3. Open the **Access Restrictions** tab within the course settings.
4. Enable the **Restrict course overview page** toggle.
5. Choose the restriction type—for example, require a product purchase or a logged-in status.
6. Click **Save** to apply your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Protecting the overview page is useful when you want to keep your course catalog private or when course details themselves are part of the premium experience.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Creating Subscribers-Only Courses
<!-- /wp:heading -->

<!-- wp:paragraph -->
One of the most popular access control strategies is offering free preview lessons while gating the rest behind an email subscription. This approach grows your email list while giving visitors a taste of your content.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
To set up a subscribers-only course:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice**.
2. Go to **Products** and create a new product (or select an existing one).
3. Assign the course you want to protect to this product.
4. Under the product's **Access Requirements**, set the requirement to **Email subscription** or the appropriate condition for your setup.
5. Open your course and mark selected introductory lessons as **Free Preview** so they remain accessible to everyone.
6. Save your settings.
<!-- /wp:list -->

<!-- wp:paragraph -->
With this configuration, visitors can view your free preview lessons without restriction. When they try to access the remaining lessons, they'll be prompted to subscribe before gaining access.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Setting Restriction Rules at the Product Level
<!-- /wp:heading -->

<!-- wp:paragraph -->
Product-level restriction rules let you define what happens when a user who hasn't purchased a product tries to access its protected content. These rules control the messaging, redirects, and call-to-action buttons visitors see.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
To access product-level restriction rules:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice** > **Products**.
2. Click on the product you want to configure.
3. Open the **Access Restriction Rules** section.
4. Configure the following options:
<!-- /wp:list -->

<!-- wp:list -->
- **Standard Contexts** — Define what restricted visitors see on course pages, lesson pages, and module pages.
- **Purchase Protection** — Set up messaging that encourages visitors to purchase the product to unlock content.
- **Action Button Display** — Choose whether to show a call-to-action button (such as a "Buy Now" or "Subscribe" button) and configure its destination URL.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** Product-level restriction rules apply to all courses assigned to that product. If you need different rules for specific courses, you can override them at the course level.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Understanding Access Rule Priority with Multiple Products
<!-- /wp:heading -->

<!-- wp:paragraph -->
When a single course is assigned to more than one product, each with its own access rules, Thrive Apprentice uses a priority system to determine which restriction applies. Understanding this hierarchy is essential to avoid unexpected behavior.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
The priority order works as follows:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. **Course-level overrides** — If you've set specific restriction rules directly on a course, those take the highest priority.
2. **Product-level rules** — If no course-level override exists, the rules of the product that the visitor is most likely trying to access apply.
3. **Global default rules** — If neither course-level nor product-level rules are configured, Thrive Apprentice falls back to the global access restriction defaults set in your general settings.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** When a course belongs to multiple products, Thrive Apprentice evaluates the visitor's context—such as the referral link or the page they came from—to determine which product's rules to display. If the context is ambiguous, the first matching product's rules take effect.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Tip:** To keep things simple, avoid assigning the same course to products with conflicting restriction rules. If you must, test the visitor experience from each entry point to ensure the correct messaging appears.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Using Dynamic Access Restriction Labels
<!-- /wp:heading -->

<!-- wp:paragraph -->
Dynamic access restriction labels are visual indicators that appear on your course listings to inform visitors about access limitations. These labels update automatically based on the viewer's status—whether they're logged out, logged in but haven't purchased, or already have access.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
To configure dynamic access restriction labels:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice**.
2. Go to the **Design** section and open the course listing or course card template in Thrive Architect.
3. Select the **Access Restriction Label** element on your course card.
4. Customize the label text for each access state:
<!-- /wp:list -->

<!-- wp:list -->
- **Restricted** — Shown to visitors who don't have access (e.g., "Premium Course" or "Members Only").
- **Enrolled** — Shown to visitors who already have access (e.g., "You're Enrolled" or "Start Learning").
- **Locked** — Shown when the course requires a login (e.g., "Log In to Access").
<!-- /wp:list -->

<!-- wp:paragraph -->
These labels work alongside **dynamic buttons** that adapt to the viewer's access state—for example, showing a "Buy Now" button to non-members and a "Continue Learning" button to enrolled students.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Tip:** Keep your label text short and clear. Visitors should immediately understand what action they need to take to gain access.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Overriding Restrictions for Non-Logged-In Users
<!-- /wp:heading -->

<!-- wp:paragraph -->
In some cases, you may want to allow non-logged-in visitors to access specific lessons even when the rest of the course is restricted. This is useful for offering free previews, sample lessons, or promotional content without requiring a login.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
To override restrictions for non-logged-in users:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice**.
2. Open the course that contains the lesson you want to make publicly accessible.
3. Click on the specific lesson you want to override.
4. In the lesson settings, enable the **Free Preview** or **Public Access** toggle.
5. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
When this override is active, the selected lesson bypasses all product-level and course-level restrictions. Non-logged-in visitors can view it freely, while the remaining lessons stay protected.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Note:** Overrides apply only to the individual lessons you've explicitly marked. The rest of the course continues to follow its standard restriction rules.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Advanced Access Control Scenarios
<!-- /wp:heading -->

<!-- wp:paragraph -->
Thrive Apprentice supports a hierarchical three-tier access control system that gives you granular control over your content:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Global settings** — Default rules that apply to all content unless overridden at a lower level.
- **Course-level controls** — Rules that apply to a specific course and all its lessons, overriding global defaults.
- **Individual page restrictions** — Rules that apply to a specific lesson, module, or page, overriding both global and course-level settings.
<!-- /wp:list -->

<!-- wp:paragraph -->
Here are some advanced scenarios you can configure:
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Gating individual pages separately from courses** — You can restrict specific WordPress pages or posts independently from your course content. This is helpful when you have bonus content, community pages, or resource libraries that should only be accessible to certain product owners.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Limiting dashboard visibility to authenticated users** — Restrict the Thrive Apprentice student dashboard so only logged-in users can see their enrolled courses and progress. Non-logged-in visitors are redirected to a login page or a sales page instead.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Building complex rules with multiple conditions** — Combine multiple access requirements to create sophisticated restriction logic. For example, require both a product purchase and an active email subscription before granting access to premium content.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Troubleshooting common access control issues** — If visitors are seeing unexpected restriction messages or gaining access they shouldn't have, check the following:
<!-- /wp:paragraph -->

<!-- wp:list -->
- Verify the priority order of your rules (course-level overrides product-level, which overrides global).
- Confirm that the correct product is assigned to the course.
- Test the experience as a logged-out user, a logged-in user without access, and a logged-in user with access.
- Clear any caching plugins to ensure restriction changes take effect immediately.
<!-- /wp:list -->

<!-- wp:heading -->
## Conclusion
<!-- /wp:heading -->

<!-- wp:paragraph -->
That's it! You've successfully learned how to set up and manage access restrictions in Thrive Apprentice. From protecting course overview pages and creating subscribers-only content to configuring product-level rules, understanding priority hierarchies, using dynamic labels, and handling advanced scenarios—you now have the tools to control exactly who sees your content and what experience they have.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Products in Thrive Apprentice** — [How to Use the Products Section in Thrive Apprentice](3-02-using-the-products-section.md)
- **Access Expiry** — [How to Manage Product Access Expiry in Thrive Apprentice](3-03-managing-product-access-expiry.md)
- **File Protection** — [How to Protect Files and Grant Access in Thrive Apprentice](3-04-protecting-files-and-granting-access.md)
- **Custom Payment Links** — [How to Set Up Custom Payment Links in Thrive Apprentice](3-05-custom-payment-links.md)
<!-- /wp:list -->
