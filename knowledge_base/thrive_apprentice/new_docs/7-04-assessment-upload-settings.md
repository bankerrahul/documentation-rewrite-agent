<!-- wp:heading {"level":1} -->
# How to Manage Assessment Upload Settings in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to configure the upload settings for assessments in Thrive Apprentice. This includes connecting a cloud storage service, selecting allowed file types, setting size limits, and managing student submissions through the review process.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Why You Need Upload Settings
<!-- /wp:heading -->

<!-- wp:paragraph -->
When you enable upload-type assessments, students submit files directly through your course. Those files need a storage destination. Thrive Apprentice integrates with **Google Drive** and **Dropbox** to securely store submitted files, so you'll need an active API connection with one of these services before students can upload anything.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Prerequisites
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before configuring upload settings, make sure you have:
<!-- /wp:paragraph -->

<!-- wp:list -->
- Thrive Apprentice version 5.8 or later
- Assessments enabled for at least one lesson (see [How to Enable Assessments](7-03-enabling-assessments.md))
- A Google Drive or Dropbox account ready for API connection
<!-- /wp:list -->

<!-- wp:heading -->
## Step 1: Connect Your Cloud Storage Service
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click **Settings** in the left sidebar.
3. Locate the **Assessment Uploads** section.
4. Click **Connect Service** and choose either **Google Drive** or **Dropbox**.
5. Follow the on-screen prompts to authorize Thrive Apprentice to access your cloud storage account.
6. Once connected, you'll see a confirmation message with the connected service name.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** For detailed instructions on setting up the Google Drive or Dropbox API connection, refer to the respective API connection guides in the Thrive Apprentice knowledge base.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 2: Configure File Type and Size Limits
<!-- /wp:heading -->

<!-- wp:paragraph -->
After connecting your storage service, you can control what students are allowed to upload:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In the **Assessment Uploads** section, locate the **Allowed File Types** setting.
2. Select the file extensions you want to accept. Common options include:
   - **Documents:** .pdf, .doc, .docx, .txt
   - **Spreadsheets:** .xls, .xlsx, .csv
   - **Presentations:** .ppt, .pptx
   - **Images:** .jpg, .png, .gif
   - **Archives:** .zip
3. Set the **Maximum File Size** limit. Choose a value that accommodates your expected submissions without overloading your storage (e.g., 10 MB, 25 MB, or 50 MB).
4. Click **Save** to apply the settings.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** If you're accepting video or large project files, consider using the **YouTube Link** or **External Link** assessment types instead. These avoid large file uploads while still letting students share their work.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Step 3: Choose a Storage Destination Folder
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
1. In the **Assessment Uploads** section, click **Select Folder**.
2. Browse your connected Google Drive or Dropbox account and choose the folder where you want student submissions stored.
3. Click **Confirm** to set the destination.
<!-- /wp:list -->

<!-- wp:paragraph -->
All student uploads will be saved to this folder. Thrive Apprentice organizes files by course and student name, making it easy to locate specific submissions.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Managing Student Submissions
<!-- /wp:heading -->

<!-- wp:paragraph -->
Once students begin submitting assessments, you can manage their uploads from the Thrive Apprentice dashboard:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice** > **Assessments**.
2. You'll see a list of all submissions with their current status: **Pending**, **Passed**, or **Failed**.
3. Click on any submission to open the review panel.
4. From the review panel, you can:
   - **View or download** the uploaded file directly from your connected cloud storage
   - **Mark as Passed** or **Mark as Failed**
   - **Add feedback** comments for the student
5. Click **Save** to finalize the review.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** Students cannot proceed past an assessment-gated lesson until you review their submission and assign a passing grade. Make sure to check the **Assessments** panel regularly.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Troubleshooting Common Issues
<!-- /wp:heading -->

<!-- wp:list -->
- **Upload button is grayed out:** The cloud storage API connection is missing or expired. Reconnect your Google Drive or Dropbox under **Settings** > **Assessment Uploads**.
- **File rejected on upload:** The student's file type or size exceeds the limits you configured. Adjust the settings or ask the student to compress/convert their file.
- **Files not appearing in storage:** Verify the destination folder still exists and that the API connection has the correct permissions.
<!-- /wp:list -->

<!-- wp:heading -->
## Conclusion
<!-- /wp:heading -->

<!-- wp:paragraph -->
That's it! You've successfully configured assessment upload settings in Thrive Apprentice. With cloud storage connected and file limits in place, your students can submit their work and you can review it—all from within your WordPress dashboard.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Enabling assessments:** [How to Enable Assessments in Thrive Apprentice](7-03-enabling-assessments.md)
- **Template refresh:** [How to Refresh Templates After Adding Assessments](7-05-refreshing-templates-after-assessments.md)
- **Google Drive API setup:** [Connecting Google Drive to Thrive Apprentice](https://thrivethemes.com/docs/google-drive-api-connection/)
- **Dropbox API setup:** [Connecting Dropbox to Thrive Apprentice](https://thrivethemes.com/docs/dropbox-api-connection/)
<!-- /wp:list -->
