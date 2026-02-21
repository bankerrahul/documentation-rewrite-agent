"""Scan all Thrive Apprentice source article URLs for embedded videos."""
import re
import sys
import time
import requests

# All source article URLs from the reorganization plan
URLS = [
    # Getting Started
    "https://thrivethemes.com/docs/creating-your-first-thrive-apprentice-course/",
    "https://thrivethemes.com/docs/using-course-content-types-navigation-structure-and-progress-section-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/creating-course-bundles-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/creating-a-free-online-course-funnel/",
    "https://thrivethemes.com/docs/creating-a-student-profile-page-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/using-dynamic-text-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/thrive-apprentice-4-0-introducing-drip-products-and-conditional-display/",
    "https://thrivethemes.com/docs/switching-from-a-learning-management-system-platform-to-thrive-apprentice/",
    "https://thrivethemes.com/docs/switching-from-learndash-to-thrive-apprentice/",
    "https://thrivethemes.com/docs/switching-from-teachable-to-thrive-apprentice/",
    "https://thrivethemes.com/docs/attaching-downloadable-files-to-lessons-in-thrive-apprentice/",
    # Settings
    "https://thrivethemes.com/docs/getting-started-with-the-thrive-apprentice-general-settings/",
    "https://thrivethemes.com/docs/navigating-the-thrive-apprentice-settings-page/",
    "https://thrivethemes.com/docs/configuring-the-login-access-restriction-rules-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/login-and-access-restriction-settings-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/setting-up-login-and-registration-page-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/registering-a-new-user-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/forcing-students-to-watch-a-video-before-marking-a-lesson-complete/",
    "https://thrivethemes.com/docs/changing-the-thrive-apprentice-lesson-type/",
    "https://thrivethemes.com/docs/protecting-the-course-overview-page-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/organizing-the-lessons-in-chapters-with-thrive-apprentice/",
    "https://thrivethemes.com/docs/hiding-premium-courses-in-the-list-of-courses/",
    "https://thrivethemes.com/docs/using-the-thrive-apprentice-widget-area/",
    "https://thrivethemes.com/docs/removing-members-from-thrive-apprentice/",
    "https://thrivethemes.com/docs/scheduling-thrive-apprentice-to-publish-at-a-specific-date/",
    "https://thrivethemes.com/docs/accessing-thrive-apprentice-course-after-purchase/",
    "https://thrivethemes.com/docs/importing-existing-members-to-thrive-apprentice/",
    "https://thrivethemes.com/docs/adding-a-progress-bar-to-your-thrive-apprentice-lesson/",
    "https://thrivethemes.com/docs/using-dynamic-labels-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/setting-up-thrive-apprentice-email-templates/",
    "https://thrivethemes.com/docs/customizing-the-thrive-apprentice-template-using-the-legacy-editor/",
    "https://thrivethemes.com/docs/setting-up-a-menu-for-your-courses-and-lessons/",
    "https://thrivethemes.com/docs/how-to-no-index-thrive-apprentice-content-with-yoast-seo/",
    "https://thrivethemes.com/docs/structuring-managing-your-courses-using-the-bulk-actions/",
    "https://thrivethemes.com/docs/using-the-members-section-of-thrive-apprentice/",
    "https://thrivethemes.com/docs/enabling-course-level-grading-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/using-the-dynamic-access-restriction-labels-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/using-the-access-requirements-to-create-subscribers-only-courses/",
    "https://thrivethemes.com/docs/managing-course-status-in-thrive-apprentice-publish-unpublish-hide-archive-schedule/",
    # Designing
    "https://thrivethemes.com/docs/getting-started-with-new-thrive-apprentice-visual-editor/",
    "https://thrivethemes.com/docs/switching-from-the-legacy-thrive-apprentice-editor-to-the-new-visual-editor/",
    "https://thrivethemes.com/docs/switching-back-to-the-legacy-thrive-apprentice-editor/",
    "https://thrivethemes.com/docs/using-the-design-section-of-thrive-apprentice/",
    "https://thrivethemes.com/docs/creating-and-using-thrive-apprentice-templates/",
    "https://thrivethemes.com/docs/managing-thrive-apprentice-templates-using-the-basic-template-options/",
    "https://thrivethemes.com/docs/applying-a-template-to-a-thrive-apprentice-content/",
    "https://thrivethemes.com/docs/editing-a-thrive-apprentice-pre-built-design/",
    "https://thrivethemes.com/docs/adding-a-new-thrive-apprentice-design/",
    "https://thrivethemes.com/docs/adding-a-new-course-overview-template-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/adding-a-new-lesson-template-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/creating-a-thrive-apprentice-module-template/",
    "https://thrivethemes.com/docs/adding-a-new-course-completion-template/",
    "https://thrivethemes.com/docs/adding-an-access-restricted-template-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/adding-a-new-certificate-verification-template/",
    "https://thrivethemes.com/docs/adding-a-new-school-homepage-in-thrive-architect/",
    "https://thrivethemes.com/docs/using-the-thrive-apprentice-elements-on-a-thrive-apprentice-template/",
    "https://thrivethemes.com/docs/integrating-lesson-and-course-list-elements-in-your-thrive-apprentice/",
    "https://thrivethemes.com/docs/adding-a-video-description-for-your-thrive-apprentice-course/",
    "https://thrivethemes.com/docs/moving-the-video-description-from-its-default-placement-on-a-template/",
    "https://thrivethemes.com/docs/displaying-lesson-resources-depending-on-the-progress-status-of-each-user/",
    "https://thrivethemes.com/docs/making-the-first-lesson-of-a-paid-thrive-apprentice-course-free/",
    "https://thrivethemes.com/docs/creating-and-publishing-a-thrive-apprentice-lesson/",
    # Drip
    "https://thrivethemes.com/docs/using-the-drip-campaign-templates-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/understanding-the-new-drip-behavior-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/setting-up-the-unlock-conditions-for-drip-schedules/",
    "https://thrivethemes.com/docs/selling-a-dripped-content-course/",
    "https://thrivethemes.com/docs/setting-up-a-sequential-unlock-drip-template/",
    "https://thrivethemes.com/docs/setting-up-an-evergreen-repeating-drip-template/",
    "https://thrivethemes.com/docs/setting-up-a-scheduled-repeating-drip-template/",
    "https://thrivethemes.com/docs/setting-up-a-day-of-the-week-or-month-drip-template/",
    "https://thrivethemes.com/docs/setting-up-a-drip-on-specific-dates-drip-template/",
    "https://thrivethemes.com/docs/setting-up-a-start-from-scratch-drip-campaign-template/",
    "https://thrivethemes.com/docs/setting-up-a-thrive-automator-unlock-drip-template/",
    "https://thrivethemes.com/docs/creating-cohort-based-classes-with-thrive-apprentice-and-drip/",
    "https://thrivethemes.com/docs/dripping-course-content-only-on-weekdays/",
    "https://thrivethemes.com/docs/how-to-start-a-course-on-the-first-monday-of-the-month/",
    "https://thrivethemes.com/docs/using-decoupled-drip-schedules/",
    "https://thrivethemes.com/docs/excluding-lessons-from-a-drip-campaign/",
    "https://thrivethemes.com/docs/hiding-locked-lessons-from-lesson-list/",
    "https://thrivethemes.com/docs/unlocking-course-contents-at-different-time-intervals/",
    # Products
    "https://thrivethemes.com/docs/using-the-products-section-of-thrive-apprentice/",
    "https://thrivethemes.com/docs/understanding-the-priority-of-access-rules-when-a-course-is-protected-by-multiple-restrictions/",
    "https://thrivethemes.com/docs/overriding-access-restrictions-for-non-logged-in-users/",
    "https://thrivethemes.com/docs/accessing-restriction-rules-at-product-level/",
    "https://thrivethemes.com/docs/managing-product-access-expiry-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/protecting-files-and-granting-access-for-customers-or-students/",
    # Integrations
    "https://thrivethemes.com/docs/should-i-integrate-with-a-checkout-tool-a-membership-plugin-or-both/",
    "https://thrivethemes.com/docs/should-i-integrate-wishlist-member-with-thrive-apprentice/",
    "https://thrivethemes.com/docs/should-i-integrate-memberpress-with-thrive-apprentice/",
    "https://thrivethemes.com/docs/should-i-use-woocommerce-with-thrive-apprentice/",
    "https://thrivethemes.com/docs/should-i-use-sendowl-with-thrive-apprentice/",
    "https://thrivethemes.com/docs/should-i-use-thrivecart-with-thrive-apprentice/",
    "https://thrivethemes.com/docs/working-of-thrive-apprentice-with-wishlist-member-plugin/",
    "https://thrivethemes.com/docs/working-of-thrive-apprentice-with-memberpress-plugin/",
    "https://thrivethemes.com/docs/working-of-thrive-apprentice-with-membermouse/",
    "https://thrivethemes.com/docs/integrating-thrive-apprentice-with-membermouse/",
    "https://thrivethemes.com/docs/getting-started-with-thrive-apprentice-and-woocommerce/",
    "https://thrivethemes.com/docs/setting-up-stripe-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/enabling-the-stripe-customer-portal-for-your-thrive-apprentice-members/",
    "https://thrivethemes.com/docs/connecting-thrive-apprentice-with-square/",
    "https://thrivethemes.com/docs/linking-thrive-apprentice-to-external-checkout-or-sales-page-using-custom-payment-links/",
    "https://thrivethemes.com/docs/registering-users-to-your-site-and-adding-them-to-an-autoresponder-simultaneously/",
    "https://thrivethemes.com/docs/how-to-no-index-thrive-apprentice-content-with-all-in-one-seo-plugin-aioseo/",
    "https://thrivethemes.com/docs/setting-thrive-apprentice-content-to-no-index-using-rankmath/",
    # Automator
    "https://thrivethemes.com/docs/enrolling-users-in-a-course-only-after-they-pass-a-test/",
    "https://thrivethemes.com/docs/notifying-students-when-new-content-is-unlocked/",
    "https://thrivethemes.com/docs/enrolling-users-in-a-course-after-they-complete-a-quiz/",
    "https://thrivethemes.com/docs/revoking-course-access-after-a-certain-period/",
    "https://thrivethemes.com/docs/using-the-product-identifier-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/granting-access-to-multiple-free-thrive-apprentice-courses-using-thrive-automator/",
    "https://thrivethemes.com/docs/unlocking-lesson-content-after-the-students-pass-the-final-exam-quiz/",
    "https://thrivethemes.com/docs/sending-discount-code-to-user-after-a-course-is-purchased/",
    "https://thrivethemes.com/docs/user-accesses-a-free-course-and-unlocks-the-first-lesson-of-a-premium-course/",
    "https://thrivethemes.com/docs/removing-users-from-a-premium-course-after-the-free-trial-expires/",
    "https://thrivethemes.com/docs/sending-a-thank-you-email-after-users-purchase-a-thrive-apprentice-product/",
    "https://thrivethemes.com/docs/creating-automations-to-grant-user-access-to-thrive-apprentice-products-purchasing-different-digistore24-products/",
    "https://thrivethemes.com/docs/sending-course-certificate-through-email/",
    # ThriveCart
    "https://thrivethemes.com/docs/connecting-thrivecart-to-thrive-apprentice/",
    "https://thrivethemes.com/docs/setting-access-restriction-rules-for-thrivecart-in-thrive-apprentice/",
    # Quiz Builder
    "https://thrivethemes.com/docs/enabling-the-mark-as-complete-button-only-after-the-user-has-passed-completed-the-quiz/",
    "https://thrivethemes.com/docs/changing-the-notification-for-the-mark-lesson-as-complete-behavior/",
    "https://thrivethemes.com/docs/using-the-mark-as-complete-feature-on-a-quiz-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/sharing-a-course-completion-certificate-when-a-member-finishes-a-course/",
    "https://thrivethemes.com/docs/unlocking-the-next-lesson-only-after-a-student-has-passed-the-quiz/",
    # Use Cases
    "https://thrivethemes.com/docs/unlocking-a-lesson-from-the-next-course-after-completing-first-course-module/",
    "https://thrivethemes.com/docs/granting-access-to-different-thrive-apprentice-courses-using-custom-user-roles/",
    "https://thrivethemes.com/docs/unlocking-a-lesson-once-the-previous-lesson-is-marked-as-completed/",
    # Translation
    "https://thrivethemes.com/docs/translating-your-online-school/",
    "https://thrivethemes.com/docs/translating-thrive-apprentice-using-legacy-editor/",
    "https://thrivethemes.com/docs/translating-the-checkout-form-in-thrive-architect/",
    "https://thrivethemes.com/docs/translating-plugin-amp-theme-strings-using-say-what-plugin/",
    # Certificates
    "https://thrivethemes.com/docs/issuing-student-certificates-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/using-the-dynamic-thrive-apprentice-certificate-data/",
    "https://thrivethemes.com/docs/using-dynamic-text-in-the-course-completion-certificate/",
    "https://thrivethemes.com/docs/changing-the-pdf-file-name-of-a-completion-certificate/",
    "https://thrivethemes.com/docs/enabling-certificate-verification-for-thrive-apprentice-courses/",
    "https://thrivethemes.com/docs/using-a-download-certificate-button-on-a-course-completed-template/",
    "https://thrivethemes.com/docs/setting-up-course-completion-behavior-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/using-the-qr-code-element-in-thrive-architect/",
    # Assessments
    "https://thrivethemes.com/docs/enabling-assessments-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/managing-assessment-upload-settings-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/refreshing-templates-in-thrive-apprentice-after-adding-assessments/",
    # Reporting
    "https://thrivethemes.com/docs/using-the-reports-section-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/viewing-member-related-data-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/sorting-students-by-enrollment-date-in-thrive-apprentice/",
    "https://thrivethemes.com/docs/unlocking-a-lesson-for-users-manually/",
    "https://thrivethemes.com/docs/recording-video-events-in-thrive-apprentice/",
    # Advanced Access Control
    "https://thrivethemes.com/docs/advanced-access-control-guide-for-thrive-apprentice/",
    # SendOwl (sample — check a few)
    "https://thrivethemes.com/docs/selling-your-thrive-apprentice-course-with-sendowl/",
    "https://thrivethemes.com/docs/setting-up-the-sendowl-listener/",
    "https://thrivethemes.com/docs/purchasing-process-in-the-sendowl-integration/",
]

VIDEO_PATTERNS = [
    re.compile(r'<iframe[^>]*src=["\']([^"\']*(?:youtube\.com|youtu\.be|wistia\.[a-z]+|vimeo\.com)[^"\']*)["\']', re.I),
    re.compile(r'<video[^>]*src=["\']([^"\']+)["\']', re.I),
    re.compile(r'class="wistia_embed[^"]*wistia_async_([a-z0-9]+)', re.I),
    re.compile(r'//fast\.wistia\.\w+/medias/([a-z0-9]+)', re.I),
]

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
})

results = {}
for i, url in enumerate(URLS):
    try:
        resp = session.get(url, timeout=15)
        found = []
        for pat in VIDEO_PATTERNS:
            matches = pat.findall(resp.text)
            found.extend(matches)
        if found:
            slug = url.rstrip("/").split("/")[-1]
            results[slug] = found
            print(f"[{i+1}/{len(URLS)}] FOUND {len(found)} video(s): {slug}")
        else:
            if (i + 1) % 20 == 0:
                print(f"[{i+1}/{len(URLS)}] scanned... no videos so far in last batch")
    except Exception as e:
        print(f"[{i+1}/{len(URLS)}] ERROR: {url} - {e}")
    time.sleep(0.3)  # be polite

print(f"\n=== RESULTS: {len(results)} articles with videos ===")
for slug, vids in results.items():
    print(f"  {slug}:")
    for v in vids:
        print(f"    {v}")
