# Configuring Quiz Redirect Settings

Instead of showing a results page on your site, you can redirect users to an external URL or a custom landing page. In this article, you'll learn how to set up redirects and forward quiz results as URL parameters.

## Enabling URL Redirects

By default, every quiz has a results page. To change this to a redirect:

1. In the **Quiz Structure** dashboard, click the **Settings** (gear icon) on the **Results Page** card.
2. Change the **Results Page Type** to **URL Redirect**.
3. Click **Manage** to define your destination URLs.

---

## Setting Up Redirect Logic

You can redirect users to different pages based on their score or category.

1. **Define Intervals:** Create score ranges (e.g., 0-10, 11-20) or specific categories.
2. **Enter URLs:** provide the specific URL for each result.
3. **Default Redirect:** Make sure to set a default URL for any results that don't fall into your specified intervals.

---

## Forwarding Results to the Destination URL

If you want to use the quiz data on the page you're redirecting to, you can "forward" the results.

1. On the Redirect settings page, toggle the **Forward Results to URL** switch to **ON**.
2. This will append the user's score, category name, and other data to the end of the URL as query parameters (e.g., `?result=Beginner&score=42`).
3. **Dynamic Display:** On the destination page, you can use **Thrive Architect's Dynamic Text** feature to grab these parameters and display them (e.g., "Welcome, [result] specialist!").

---

## The Redirect Message

To improve the user experience, you can show a brief message before the redirect occurs.

1. Enable the **Display Redirect Message** toggle.
2. Customize the text (e.g., "Calculating your results... please wait while we redirect you").
3. Set the duration (in seconds) that the message should be visible.

---

## Related Resources

* **Results Page:** [How to Customize Your Quiz Results Page](how-to-customize-your-quiz-results-page)
* **Opt-in Gates:** [Using the Opt-in Gate in Thrive Quiz Builder](how-to-use-the-opt-in-gate-in-thrive-quiz-builder)
* **Publishing:** [How to Publish and Display Your Quiz](how-to-publish-and-display-your-quiz)

**Thrive Quiz Builder Documentation:** Explore the full [Thrive Quiz Builder knowledge base](https://thrivethemes.com/docs-categories/thrive-quiz-builder/)
