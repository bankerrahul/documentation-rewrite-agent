<!-- wp:heading {"level":1} -->
# How to Issue Course Completion Certificates in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to create and issue course completion certificates in Thrive Apprentice—from designing your certificate template and inserting dynamic student data, to customizing PDF filenames, enabling verification, adding download buttons, and sharing certificates via email.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Prerequisites
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before you begin, make sure you have:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Thrive Apprentice** installed and activated on your WordPress site.
- At least one published course with content for students to complete.
- **Thrive Architect** available for editing certificate templates and lesson pages.
<!-- /wp:list -->

<!-- wp:heading -->
## Overview of the Certificate System
<!-- /wp:heading -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=q5U4uM59GBk","type":"video","providerNameSlug":"youtube","responsive":true} -->
<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube"><div class="wp-block-embed__wrapper">
https://www.youtube.com/watch?v=q5U4uM59GBk
</div></figure>
<!-- /wp:embed -->

<!-- wp:paragraph -->
Thrive Apprentice allows you to award certificates to students who finish a course. Certificates are generated as PDF files and can include personalized details like the student's name, the course title, and the date of completion. You can deliver them through download buttons, email notifications, or shareable verification pages.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Creating a Certificate Template
<!-- /wp:heading -->

<!-- wp:paragraph -->
To set up certificates, you first need to create a certificate template using the visual editor.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In your WordPress dashboard, navigate to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click the **Certificates** tab in the left sidebar.
3. Click **Add New Certificate** to create a new template.
4. Give your certificate a descriptive name (e.g., "Standard Completion Certificate").
5. Click **Edit Design** to open the certificate in the visual editor.
6. Design your certificate layout using the drag-and-drop builder—add text elements, images, borders, logos, and background colors to match your brand.
7. Click **Save Work** when you're finished, then click **Done** to return to the Certificates screen.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Keep your certificate design clean and professional. A centered layout with your logo at the top, the student's name prominently displayed, and the course title below works well for most use cases.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Using Dynamic Data in Your Certificate
<!-- /wp:heading -->

<!-- wp:paragraph -->
Dynamic data allows you to automatically insert personalized information into each certificate so you don't have to create individual certificates for every student.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. While editing your certificate template in the visual editor, click on a text element where you want to insert dynamic content.
2. Look for the **Dynamic Text** option in the text element toolbar.
3. Select from the available dynamic fields:
   - **Student Name** — inserts the full name of the student who completed the course.
   - **Course Title** — inserts the name of the completed course.
   - **Completion Date** — inserts the date the student finished the course.
   - **Certificate ID** — inserts a unique identifier for verification purposes.
4. Position and style the dynamic text elements to fit your certificate design.
5. Click **Save Work** to preserve your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** Dynamic text fields appear as placeholder tags while editing. They are automatically replaced with real student data when the PDF certificate is generated.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Assigning a Certificate to a Course
<!-- /wp:heading -->

<!-- wp:paragraph -->
After creating your certificate template, you need to assign it to the course that should award it upon completion.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to the **Courses** tab and open the course you want to add a certificate to.
2. In the course settings, locate the **Certificate** section.
3. Select your certificate template from the dropdown list.
4. Click **Save** to apply the certificate to the course.
<!-- /wp:list -->

<!-- wp:paragraph -->
Students who complete all required lessons in this course will now be eligible to receive the certificate.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Customizing the PDF File Name
<!-- /wp:heading -->

<!-- wp:paragraph -->
By default, certificate PDFs are generated with a generic filename. You can customize this to include meaningful information for your students.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to the **Certificates** tab and open the certificate template you want to modify.
2. Locate the **PDF File Name** setting.
3. Enter a custom filename pattern using dynamic placeholders. For example:
   - `{student_name}-{course_title}-certificate` would generate a file like "John-Smith-Email-Marketing-certificate.pdf".
4. Click **Save** to apply the changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Using descriptive filenames helps students find and organize their certificates after downloading them.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Enabling Certificate Verification
<!-- /wp:heading -->

<!-- wp:paragraph -->
Certificate verification allows anyone to confirm the authenticity of a certificate by visiting a unique verification URL. This is especially useful for professional or accredited courses.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Go to the **Certificates** tab and open your certificate template.
2. Find the **Verification** toggle and enable it.
3. Once enabled, each generated certificate will include a unique verification URL.
4. Students and employers can visit this URL to confirm the certificate is valid and view details like the student's name, course title, and completion date.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** The verification page is automatically created and hosted on your WordPress site. You don't need to set up any additional pages.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Adding a Download Certificate Button
<!-- /wp:heading -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=WyaeVQSUypQ","type":"video","providerNameSlug":"youtube","responsive":true} -->
<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube"><div class="wp-block-embed__wrapper">
https://www.youtube.com/watch?v=WyaeVQSUypQ
</div></figure>
<!-- /wp:embed -->

<!-- wp:paragraph -->
You can place a download button on your course completion page or within any lesson so students can easily retrieve their certificate as a PDF.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Open the page or lesson where you want to add the download button in **Thrive Architect**.
2. From the element panel, drag and drop the **Download Certificate** button element onto the page.
3. Customize the button text (e.g., "Download Your Certificate"), style, and placement.
4. The button automatically links to the student's personalized certificate PDF—no manual linking needed.
5. Click **Save Work** to apply your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** The download button only appears to students who have completed the course. Students who haven't finished will not see the button, so you can safely place it on any course-related page.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Sending Certificates via Email
<!-- /wp:heading -->

<!-- wp:paragraph -->
You can automatically send certificates to students by email when they complete a course. This uses the Thrive Apprentice email notification system.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Apprentice** > **Settings** > **Email Templates**.
2. Locate or create a **Course Completion** email template.
3. In the email body, add the certificate download link using the available dynamic shortcodes.
4. Customize the subject line and body text to congratulate the student and provide instructions for downloading their certificate.
5. Save the email template.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Mention the verification URL in the email as well, so students can share a link that proves their achievement without needing to send the actual PDF.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Sharing Course Completion Certificates
<!-- /wp:heading -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=lXZ-a6PH3lo","type":"video","providerNameSlug":"youtube","responsive":true} -->
<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube"><div class="wp-block-embed__wrapper">
https://www.youtube.com/watch?v=lXZ-a6PH3lo
</div></figure>
<!-- /wp:embed -->

<!-- wp:paragraph -->
Students can share their certificates on social media or with employers directly from your site.
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Social Sharing** — If you enable sharing options on the certificate or verification page, students can post their achievement to platforms like LinkedIn, Facebook, or Twitter.
- **Verification Link** — Students can copy and share the unique verification URL, allowing anyone to confirm the certificate's authenticity online.
- **PDF Download** — Students can download the PDF and attach it to job applications, portfolios, or emails.
<!-- /wp:list -->

<!-- wp:paragraph -->
To enable sharing, make sure the verification page is active and that your certificate template includes the relevant dynamic data (student name, course title, and completion date) so shared links display meaningful information.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
That's it! You've successfully set up course completion certificates in Thrive Apprentice—from creating the template and adding dynamic data, to enabling downloads, verification, email delivery, and social sharing.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Course Completion Behavior:** Learn how to [set up course completion behavior](8-02-course-completion-behavior.md) including redirects, messages, and next course suggestions.
- **Email Templates:** Customize your [email notification templates](2-08-email-templates.md) for certificate delivery and other course events.
- **Visual Editor Basics:** Get started with the [Thrive Apprentice visual editor](4-01-getting-started-visual-editor.md) for designing certificates and course pages.
- **Managing Courses:** Review how to [manage your courses](2-03-managing-courses.md) and assign certificates to specific courses.
<!-- /wp:list -->