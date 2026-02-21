<!-- wp:heading {"level":1} -->
# How to Use Quizzes in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to integrate Thrive Quiz Builder quizzes into your Thrive Apprentice courses. You'll cover the "Mark as Complete" feature, gating lesson progression behind quiz results, enrolling students after quiz completion, unlocking content after a final exam, and customizing the completion notification message.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Why Use Quizzes in Your Courses?
<!-- /wp:heading -->

<!-- wp:paragraph -->
Adding quizzes to your Thrive Apprentice courses lets you verify that students understand the material before they move on. Quizzes can serve as knowledge checks within lessons, gates that control progression, or even entry requirements for course enrollment. Thrive Quiz Builder provides the quiz functionality, and Thrive Apprentice handles the course progression logic.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Using the "Mark as Complete" Feature on a Quiz
<!-- /wp:heading -->

<!-- wp:paragraph -->
The **Mark as Complete** feature lets students indicate they've finished a lesson. When you add a quiz to a lesson, you can tie this button directly to quiz completion—so students can only mark the lesson as done after they've taken the quiz.
<!-- /wp:paragraph -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=0fAZhli9QGk","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=0fAZhli9QGk
<!-- /wp:embed -->

<!-- wp:paragraph -->
Here's how to set it up:
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice** and open the course you want to edit.
2. Select the lesson that contains your quiz.
3. Open the lesson settings and locate the **Completion** section.
4. Set the **Mark as Complete** behavior to require quiz completion.
5. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
Once configured, the **Mark Lesson as Complete** button will remain inactive until the student finishes the quiz. This keeps your progress tracking accurate and ensures students engage with the assessment before continuing.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Enabling "Mark as Complete" Only After the User Passes the Quiz
<!-- /wp:heading -->

<!-- wp:paragraph -->
You can take the previous setup one step further by requiring students to not just complete the quiz, but actually **pass** it with a minimum score. This prevents students who fail from advancing to the next lesson.
<!-- /wp:paragraph -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=WEAgBQf33jQ","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=WEAgBQf33jQ
<!-- /wp:embed -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice** and open your course.
2. Select the lesson with the quiz.
3. In the lesson's **Completion** settings, set the behavior to **Quiz must be passed**.
4. Define the passing score threshold in Thrive Quiz Builder (e.g., 70% or higher).
5. Save your settings.
<!-- /wp:list -->

<!-- wp:paragraph -->
Now, only students who meet or exceed the passing score will see the **Mark Lesson as Complete** button become active. Students who score below the threshold can retake the quiz until they pass.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Tip:** Set a clear passing threshold that reflects the difficulty of the material. A score between 70% and 80% is common for most educational courses.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Unlocking the Next Lesson Only After a Student Passes the Quiz
<!-- /wp:heading -->

<!-- wp:paragraph -->
Beyond controlling the **Mark as Complete** button, you can lock subsequent lessons behind quiz results using Thrive Apprentice's drip and scheduling features. This ensures students truly master each section before accessing the next one.
<!-- /wp:paragraph -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=oojQhn4spVU","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=oojQhn4spVU
<!-- /wp:embed -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice** and open your course.
2. Go to **Courses** in the sidebar and select your course.
3. Add your quiz to the lesson content using Thrive Quiz Builder.
4. Open the **Drip** settings for the course.
5. Create a new **Drip Schedule** and set the unlock condition to **After previous lesson is completed**.
6. Link the drip schedule to your course's product under the **Access Restrictions** settings.
7. Save and publish.
<!-- /wp:list -->

<!-- wp:paragraph -->
With this configuration, the next lesson in the sequence only becomes available after the student completes (and passes, if required) the current lesson's quiz. This creates a linear, mastery-based learning path.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Enrolling Users in a Course After They Complete a Quiz
<!-- /wp:heading -->

<!-- wp:paragraph -->
You can use a standalone quiz as a gateway to course enrollment. For example, you might offer a free assessment on your website and automatically enroll anyone who completes it into a course. This workflow uses Thrive Automator to connect Thrive Quiz Builder with Thrive Apprentice.
<!-- /wp:paragraph -->

<!-- wp:embed {"url":"https://www.youtube.com/watch?v=r9pBH3FpjDM","type":"video","providerNameSlug":"youtube","responsive":true} -->
https://www.youtube.com/watch?v=r9pBH3FpjDM
<!-- /wp:embed -->

<!-- wp:list {"ordered":true} -->
1. Create your quiz in Thrive Quiz Builder and add a **WordPress account connection** to the quiz's opt-in gate. This ensures quiz takers are registered as WordPress users.
2. Go to **Thrive Dashboard** > **Thrive Automator** and click **+ Add New**.
3. Set the **Start Trigger** to **User completes quiz**.
4. Select the specific quiz from the dropdown.
5. Add an **Action** and select **Grant access to product**.
6. Choose the Thrive Apprentice product that contains the course you want to enroll them in.
7. Click **Save and Activate**.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Important:** The quiz must have an active WordPress account connection in its opt-in gate. Without this, quiz takers won't have WordPress accounts, and the automation won't be able to grant them course access.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Unlocking Lesson Content After Students Pass the Final Exam
<!-- /wp:heading -->

<!-- wp:paragraph -->
If your course includes a final exam, you can unlock bonus content, certificates, or additional resources only after a student passes it. This uses a combination of Thrive Automator and Thrive Apprentice's drip feature.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Create the final exam quiz in Thrive Quiz Builder with a defined passing score.
2. In Thrive Apprentice, add the bonus content as a separate lesson or module that is initially locked.
3. Set up a **Drip Schedule** with an unlock condition tied to quiz completion.
4. Go to **Thrive Dashboard** > **Thrive Automator** and create an automation where:
   - **Start Trigger:** User completes quiz (select your final exam)
   - **Filter:** Score meets the passing threshold
   - **Action:** Grant access to the locked content or update the student's progress
5. Save and activate the automation.
<!-- /wp:list -->

<!-- wp:paragraph -->
This approach rewards students who complete the entire course and pass the final assessment, motivating them to engage thoroughly with your material.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Changing the "Mark Lesson as Complete" Notification Message
<!-- /wp:heading -->

<!-- wp:paragraph -->
When students interact with the **Mark Lesson as Complete** button—especially when it's tied to a quiz—they see a notification message. You can customize this message to match your brand voice or provide specific instructions.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to **Thrive Dashboard** > **Thrive Apprentice**.
2. Open the course and select the lesson whose notification you want to change.
3. Go to the lesson's **Completion** settings.
4. Locate the **Notification Message** field.
5. Edit the text to display your preferred message. For example, you might change it from the default to something like "Great job! You've passed the quiz. Click below to continue to the next lesson."
6. Save your changes.
<!-- /wp:list -->

<!-- wp:paragraph -->
You can set different messages depending on the quiz outcome:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Passed:** A congratulatory message with instructions to proceed.
- **Failed:** An encouraging message prompting the student to review the material and retake the quiz.
- **Completed (no pass/fail):** A neutral confirmation message.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** Keep notification messages short, positive, and actionable. Students should immediately understand what to do next.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Conclusion
<!-- /wp:heading -->

<!-- wp:paragraph -->
That's it! You've successfully learned how to integrate quizzes into your Thrive Apprentice courses using Thrive Quiz Builder. From simple completion tracking to advanced enrollment automations, quizzes give you powerful tools to create structured, mastery-based learning experiences for your students.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Thrive Quiz Builder basics:** [Getting Started with Thrive Quiz Builder](https://thrivethemes.com/docs/thrive-quiz-builder/)
- **Automator recipes for courses:** [How to Use Thrive Automator Recipes with Thrive Apprentice](7-01-automator-recipes.md)
- **Drip content setup:** [Setting Up Drip Schedules in Thrive Apprentice](https://thrivethemes.com/docs/thrive-apprentice-drip/)
- **Enabling assessments:** [How to Enable Assessments in Thrive Apprentice](7-03-enabling-assessments.md)
<!-- /wp:list -->
