<!-- wp:heading {"level":1} -->
# How to No-Index Thrive Apprentice Content with SEO Plugins
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to prevent search engines from indexing your Thrive Apprentice course content using three popular SEO plugins: Yoast SEO, All in One SEO (AIOSEO), and Rank Math. This is especially useful if you sell paid courses and don't want their content appearing in Google search results.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Why No-Index Your Course Content?
<!-- /wp:heading -->

<!-- wp:paragraph -->
When you create courses in Thrive Apprentice, the lessons, modules, and chapters are published as WordPress content—which means search engines can discover and index them. For free courses, this might be fine. But if you're selling premium courses, you likely don't want that content showing up in search results for a few important reasons:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Protect premium content:** Prevent non-paying visitors from previewing your paid material in search snippets.
- **Avoid thin content issues:** Restricted pages that show a login prompt instead of real content can hurt your SEO if search engines index them.
- **Keep your search presence clean:** Only show pages in search results that provide value to visitors who click through.
<!-- /wp:list -->

<!-- wp:paragraph -->
You can no-index the following Thrive Apprentice content types:
<!-- /wp:paragraph -->

<!-- wp:list -->
- Courses
- Modules
- Chapters
- Lessons
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** You don't need to no-index your main course sales pages. Only no-index the restricted content that sits behind a paywall.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Option 1: No-Index with Yoast SEO
<!-- /wp:heading -->

<!-- wp:paragraph -->
Yoast SEO is one of the most widely used WordPress SEO plugins. Here's how to use it to no-index your Thrive Apprentice content.
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### No-Index Individual Lessons, Modules, or Chapters
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Open the lesson, module, or chapter you want to no-index in the WordPress editor.
2. Scroll down to the **Yoast SEO** meta box below the content area.
3. Click the **Advanced** tab (the gear icon) within the Yoast SEO box.
4. Find the **Allow search engines to show this content in search results?** dropdown.
5. Select **No** to set the page to no-index.
6. Update or publish the page.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### No-Index All Content of a Specific Type
<!-- /wp:heading -->

<!-- wp:paragraph -->
If you want to no-index all lessons or all modules at once, you can do this from the Yoast SEO settings:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In your WordPress admin, go to **Yoast SEO** > **Settings**.
2. Navigate to the **Content types** section.
3. Find the Thrive Apprentice content types (Lessons, Modules, Chapters).
4. For each content type you want to hide, set the **Show in search results** toggle to **Off**.
5. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** Setting a content type to no-index in bulk will affect all existing and future content of that type. If you only want to no-index specific items, use the individual method above.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Option 2: No-Index with All in One SEO (AIOSEO)
<!-- /wp:heading -->

<!-- wp:paragraph -->
AIOSEO provides similar no-index functionality through a slightly different interface.
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### No-Index Individual Lessons, Modules, or Chapters
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Open the lesson, module, or chapter in the WordPress editor.
2. Scroll down to the **AIOSEO Settings** section below the content area.
3. Click the **Advanced** tab.
4. Find the **Robots Setting** section.
5. Toggle the **Use Default Settings** switch to **Off** to reveal custom options.
6. Check the **No Index** checkbox.
7. Update or publish the page.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### No-Index All Content of a Specific Type
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. In your WordPress admin, go to **All in One SEO** > **Search Appearance**.
2. Click the **Content Types** tab.
3. Find the Thrive Apprentice content types (Lessons, Modules, Chapters).
4. Click on the content type you want to configure.
5. Under the **Advanced** tab, select **No Index** in the Robots meta settings.
6. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** Like Yoast, changing the setting at the content type level affects all existing and future content of that type.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Option 3: No-Index with Rank Math
<!-- /wp:heading -->

<!-- wp:paragraph -->
Rank Math is a popular SEO plugin known for its clean interface and powerful features. Here's how to no-index Thrive Apprentice content with it.
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
### No-Index Individual Lessons, Modules, or Chapters
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Open the lesson, module, or chapter in the WordPress editor.
2. Click the **Rank Math** icon in the top-right corner of the editor (or scroll down to the Rank Math meta box).
3. Click the **Advanced** tab.
4. Find the **Robots Meta** section.
5. Select **No Index** from the available directives.
6. Update or publish the page.
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
### No-Index All Content of a Specific Type
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. In your WordPress admin, go to **Rank Math** > **Titles & Meta**.
2. Find the tabs for Thrive Apprentice content types (Lessons, Modules, Chapters).
3. Click on the content type you want to configure.
4. In the **Robots Meta** section, check the **No Index** option.
5. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Rank Math also lets you set up custom robots meta for individual posts, which overrides the global setting. This is useful if you want most lessons no-indexed but a few specific ones visible in search results as teasers.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Verifying Your No-Index Settings
<!-- /wp:heading -->

<!-- wp:paragraph -->
After applying no-index settings, verify they're working correctly:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Open the lesson or course page you've set to no-index in your browser.
2. Right-click on the page and select **View Page Source**.
3. Search for `noindex` in the page source code.
4. You should find a meta tag like: `<meta name="robots" content="noindex"/>` in the `<head>` section of the page.
<!-- /wp:list -->

<!-- wp:paragraph -->
If you see the `noindex` meta tag, the setting is working. Search engines will honor this directive and exclude the page from their index.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Note:** It may take time for search engines to re-crawl your pages and remove them from existing search results. If a page was previously indexed, you can request removal through Google Search Console for faster de-indexing.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Which Content Should You No-Index?
<!-- /wp:heading -->

<!-- wp:paragraph -->
Here's a quick guide to help you decide:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **No-index:** Paid lessons, restricted modules, protected chapters—any content behind a paywall
- **Keep indexed:** Course sales pages, free preview lessons, your main course catalog page
- **Consider carefully:** Free course lessons (these can drive organic traffic, but may also clutter search results)
<!-- /wp:list -->

<!-- wp:paragraph -->
That's it! You've successfully learned how to no-index Thrive Apprentice content using Yoast SEO, AIOSEO, and Rank Math. Your paid course content is now protected from appearing in search engine results.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Choosing an integration:** [How to Choose the Right Integration for Thrive Apprentice](6-01-choosing-an-integration.md)
- **Stripe setup:** [How to Set Up Stripe in Thrive Apprentice](6-05-setting-up-stripe.md)
- **WooCommerce setup:** [How to Get Started with WooCommerce and Thrive Apprentice](6-03-getting-started-woocommerce.md)
<!-- /wp:list -->
