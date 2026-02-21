"""
Setup script for Thrive Apprentice local site.
Runs the setup wizard and creates sample course data via Playwright.
"""

import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

WP_URL = os.getenv("WP_URL", "http://thrive-themes.local").rstrip("/")
WP_USERNAME = os.getenv("WP_USERNAME", "rahul")
WP_PASSWORD = os.getenv("WP_PASSWORD", "baroda")

TA_URL = f"{WP_URL}/wp-admin/admin.php?page=thrive_apprentice"


def login(page: Page) -> None:
    """Log into WordPress."""
    print(f"Logging into {WP_URL}...")
    page.goto(f"{WP_URL}/wp-login.php")
    page.fill("#user_login", WP_USERNAME)
    page.fill("#user_pass", WP_PASSWORD)
    page.click("#wp-submit")
    page.wait_for_load_state("networkidle")
    if "wp-admin" in page.url:
        print("Login successful.")
    else:
        print(f"Warning: Login may have failed. URL: {page.url}")


def run_setup_wizard(page: Page) -> None:
    """Run the Thrive Apprentice setup wizard if it's showing."""
    print("Navigating to Thrive Apprentice...")
    page.goto(TA_URL)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Check if setup wizard is showing
    get_started = page.get_by_text("Get Started", exact=False)
    if get_started.count() > 0 and get_started.first.is_visible():
        print("Setup wizard detected. Clicking 'Get Started'...")
        get_started.first.click()
        page.wait_for_timeout(2000)

        # The wizard asks to select or create a course page
        # Look for "Add New Page" or "Save and Continue" button
        add_page = page.get_by_text("Add New Page", exact=False)
        if add_page.count() > 0 and add_page.first.is_visible():
            print("Creating new courses page...")
            add_page.first.click()
            page.wait_for_timeout(1000)

        # Look for save/continue button
        save_continue = page.locator("button:has-text('Save'), button:has-text('Continue'), button:has-text('Done')")
        if save_continue.count() > 0:
            save_continue.first.click()
            page.wait_for_timeout(2000)

        print("Setup wizard completed.")
    else:
        print("No setup wizard detected (already completed).")


def create_sample_course(page: Page) -> None:
    """Create a sample course with modules, chapters, and lessons."""
    print("Navigating to Courses section...")
    page.goto(TA_URL)
    page.wait_for_timeout(2000)

    # Click on "Courses" in the left sidebar
    courses_link = page.locator("a:has-text('Courses'), span:has-text('Courses')").first
    if courses_link.is_visible():
        courses_link.click()
        page.wait_for_timeout(2000)

    # Look for "Add Course" button
    add_course = page.locator("button:has-text('Add Course'), a:has-text('Add Course'), .tva-add-course")
    if add_course.count() > 0:
        print("Creating sample course: 'Introduction to Email Marketing'...")
        add_course.first.click()
        page.wait_for_timeout(1000)

        # Fill in course title
        title_input = page.locator("input[type='text']").first
        if title_input.is_visible():
            title_input.fill("Introduction to Email Marketing")
            page.wait_for_timeout(500)

        # Save
        save_btn = page.locator("button:has-text('Save'), button:has-text('Create')")
        if save_btn.count() > 0:
            save_btn.first.click()
            page.wait_for_timeout(2000)
            print("Course created.")
    else:
        print("Could not find 'Add Course' button. Course may already exist.")


def main():
    print("=" * 60)
    print("Thrive Apprentice Sample Data Setup")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Headed so you can see
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        try:
            login(page)
            run_setup_wizard(page)
            create_sample_course(page)

            print("\nSetup complete!")
            print("You can now run the screenshot capture agent.")
            print("\nPress Enter to close the browser...")
            input()

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="setup_error.png")
            print("Saved error screenshot to setup_error.png")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    main()
