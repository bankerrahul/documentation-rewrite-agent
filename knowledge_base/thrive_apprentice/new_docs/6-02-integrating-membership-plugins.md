<!-- wp:heading {"level":1} -->
# How to Integrate Membership Plugins with Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to connect the three most popular WordPress membership plugins—WishList Member, MemberPress, and MemberMouse—to Thrive Apprentice so you can control course access based on membership levels.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Note:** Thrive Apprentice has a built-in membership and payment system powered by Stripe. You only need a membership plugin if you already run a membership site or require advanced multi-tier access control beyond what the native tools provide.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## How Membership Plugins Work with Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
All three membership plugins follow the same general pattern when integrated with Thrive Apprentice:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. The membership plugin manages your users, membership levels, and payments.
2. Users sign up or purchase a membership through the membership plugin.
3. Thrive Apprentice reads the membership level data from the plugin.
4. You configure access requirements on your Thrive Apprentice products to restrict courses to specific membership levels.
5. When a user logs in, Thrive Apprentice checks their membership status and grants or denies course access automatically.
<!-- /wp:list -->

<!-- wp:paragraph -->
This means you manage members in one place (the membership plugin) and manage courses in another (Thrive Apprentice), while the two systems communicate seamlessly behind the scenes.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## WishList Member
<!-- /wp:heading -->

<!-- wp:paragraph -->
WishList Member is a WordPress membership plugin that offers access control, multiple membership levels, payment processing, and marketing tools. When connected to Thrive Apprentice, it lets you restrict course access based on WishList Member membership levels.
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### Prerequisites
<!-- /wp:heading -->

<!-- wp:list -->
- WishList Member plugin installed and activated on your WordPress site
- At least one membership level created in WishList Member
- At least one product created in Thrive Apprentice with a course assigned to it
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### How to Set Up WishList Member Access
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Products** in the left sidebar.
3. Select the product you want to protect.
4. Click the **Access requirements** tab.
5. In the access requirements panel on the right, look for the WishList Member protection options.
6. Select the WishList Member membership level(s) that should grant access to this product.
7. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
Once configured, only users with the selected WishList Member membership level will be able to access the courses inside that product. Users without the correct level will see a restricted access message or be redirected to a registration page—depending on your settings.
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### Key Settings
<!-- /wp:heading -->

<!-- wp:list -->
- **Membership levels:** You can assign one or multiple levels to a single product, giving you flexible tiered access.
- **Access requirements panel:** This is where you'll see all available WishList Member levels pulled directly from the plugin.
- **Restricted content behavior:** Configure what non-members see when they try to access protected content in your Thrive Apprentice design settings.
<!-- /wp:list -->

<!-- wp:heading -->
## MemberPress
<!-- /wp:heading -->

<!-- wp:paragraph -->
MemberPress is a premium WordPress membership plugin known for its advanced features—coupons, access rules, reminders, and drip content. When integrated with Thrive Apprentice, your MemberPress membership levels are imported directly and used to control course access.
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### Prerequisites
<!-- /wp:heading -->

<!-- wp:list -->
- MemberPress plugin installed and activated on your WordPress site
- At least one membership level (called "Memberships" in MemberPress) created
- At least one product created in Thrive Apprentice
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### How to Set Up MemberPress Access
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Products** in the left sidebar.
3. Select the product you want to protect.
4. Click the **Access requirements** tab.
5. In the access requirements panel, locate the MemberPress protection options.
6. Choose the MemberPress membership level(s) that should grant access.
7. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
The membership level entries are imported straight from MemberPress, so any levels you create there will automatically appear in Thrive Apprentice's access settings.
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### Key Settings
<!-- /wp:heading -->

<!-- wp:list -->
- **Membership levels:** Directly imported from MemberPress—no manual syncing required.
- **Restricted access behavior:** When a user without the required membership tries to access a course, they can be redirected to a login or registration page, or shown custom restricted content.
- **Coupons and rules:** These are managed inside MemberPress itself. Thrive Apprentice reads the resulting membership status.
<!-- /wp:list -->

<!-- wp:heading -->
## MemberMouse
<!-- /wp:heading -->

<!-- wp:html -->
<script src="https://fast.wistia.com/embed/medias/ifx3hglo3j.jsonp" async></script>
<script src="https://fast.wistia.com/assets/external/E-v1.js" async></script>
<div class="wistia_responsive_padding"><div class="wistia_responsive_wrapper"><div class="wistia_embed wistia_async_ifx3hglo3j videoFoam=true"></div></div></div>
<!-- /wp:html -->

<!-- wp:paragraph -->
MemberMouse is a subscription and membership plugin that offers content restriction, billing, customer management, and membership tier creation. When connected to Thrive Apprentice, you can restrict course access based on MemberMouse membership levels or bundle purchases.
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### Prerequisites
<!-- /wp:heading -->

<!-- wp:list -->
- MemberMouse plugin installed and activated on your WordPress site
- At least one MemberMouse product created
- Membership levels established in MemberMouse
- A bundle configured in MemberMouse (if using bundle-based access)
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### How to Set Up MemberMouse Access
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Go to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Products** in the left sidebar.
3. Select the product you want to protect.
4. Click the **Access requirements** tab.
5. In the access requirements panel, find the MemberMouse protection options.
6. Choose the MemberMouse membership level(s) or bundle(s) that should grant access.
7. Save your changes.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### Key Settings
<!-- /wp:heading -->

<!-- wp:list -->
- **Membership levels:** Select which MemberMouse membership levels grant access to the product.
- **Bundles:** You can also grant access based on bundle purchases, giving you an additional layer of flexibility.
- **Access control:** MemberMouse verifies the user's membership status or bundle ownership before Thrive Apprentice grants course access.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** If you use bundles in MemberMouse, you can create course packages that give users access to multiple Thrive Apprentice products with a single purchase.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Troubleshooting Common Issues
<!-- /wp:heading -->

<!-- wp:paragraph -->
If your membership plugin integration isn't working as expected, check these common issues:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Membership levels not appearing:** Make sure the membership plugin is activated and that you have created at least one membership level. Refresh the Thrive Apprentice settings page.
- **Users can't access courses:** Verify that the user's membership level matches the access requirement set on the product. Check that the user's membership is active and not expired.
- **Changes not taking effect:** After updating access requirements, ask affected users to log out and log back in so their session refreshes.
<!-- /wp:list -->

<!-- wp:paragraph -->
That's it! You've successfully learned how to integrate WishList Member, MemberPress, and MemberMouse with Thrive Apprentice to control course access through membership levels.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Choosing an integration:** [How to Choose the Right Integration for Thrive Apprentice](6-01-choosing-an-integration.md)
- **Stripe setup:** [How to Set Up Stripe in Thrive Apprentice](6-05-setting-up-stripe.md)
- **WooCommerce setup:** [How to Get Started with WooCommerce and Thrive Apprentice](6-03-getting-started-woocommerce.md)
- **ThriveCart connection:** [How to Connect ThriveCart to Thrive Apprentice](6-04-connecting-thrivecart.md)
<!-- /wp:list -->
