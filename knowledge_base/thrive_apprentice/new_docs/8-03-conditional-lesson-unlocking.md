<!-- wp:heading {"level":1} -->
# How to Set Up Conditional Lesson Unlocking in Thrive Apprentice
<!-- /wp:heading -->

<!-- wp:paragraph -->
In this article, you'll learn how to set up conditional lesson unlocking in Thrive Apprentice—including requiring previous lesson completion, unlocking lessons across courses after a module is finished, and granting access based on custom user roles.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Prerequisites
<!-- /wp:heading -->

<!-- wp:paragraph -->
Before you begin, make sure you have:
<!-- /wp:paragraph -->

<!-- wp:list -->
- **Thrive Apprentice** installed and activated on your WordPress site.
- At least one published course with multiple lessons.
- An understanding of your desired course progression structure.
<!-- /wp:list -->

<!-- wp:heading -->
## Why Use Conditional Lesson Unlocking
<!-- /wp:heading -->

<!-- wp:paragraph -->
Conditional lesson unlocking ensures that students progress through your course content in a specific order. Instead of allowing students to skip ahead, you can require them to complete each lesson sequentially, finish a module before accessing the next one, or meet specific role-based criteria before gaining access. This helps maintain the intended learning experience and ensures students build knowledge step by step.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Unlocking Lessons After Previous Completion
<!-- /wp:heading -->

<!-- wp:paragraph -->
The most common conditional unlock method requires students to complete the previous lesson before the next one becomes available. This creates a linear course progression.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. In your WordPress dashboard, navigate to **Thrive Dashboard** > **Thrive Apprentice**.
2. Click the **Courses** tab and open the course you want to configure.
3. In the course structure panel, locate the lesson you want to restrict.
4. Click on the lesson to open its settings.
5. Find the **Access Restriction** or **Unlock Condition** setting.
6. Select **Unlock after previous lesson is completed**.
7. Click **Save** to apply the setting.
8. Repeat for each lesson that should follow a sequential order.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Tip:** You can apply this setting to all lessons in a course at once by configuring the course-level setting to enforce sequential progression. This saves time if your entire course should be completed in order.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
When this is enabled, students will see locked lessons in the course navigation but won't be able to access them until they complete the preceding lesson. A visual indicator (such as a lock icon) tells students the lesson is not yet available.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Unlocking Lessons Across Courses After Module Completion
<!-- /wp:heading -->

<!-- wp:paragraph -->
In some learning paths, completing a module in one course should unlock content in a different course. This is useful when you have multi-course curricula where courses build on each other.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to the course that contains the lesson you want to conditionally unlock.
2. Open the lesson settings for the target lesson.
3. In the **Unlock Condition** settings, look for the option to set a cross-course condition.
4. Select the source course and the specific module that must be completed.
5. Define the condition: the student must complete all lessons in the selected module.
6. Click **Save** to apply.
<!-- /wp:list -->

<!-- wp:paragraph -->
**Note:** Cross-course unlocking requires that students are enrolled in both courses. If a student hasn't been granted access to the source course, the condition cannot be met.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
This approach works well when you have a prerequisite course that covers foundational material. For example, you might require students to complete "Module 3: Advanced Concepts" in your introductory course before they can access lessons in your advanced course.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Granting Access Using Custom User Roles
<!-- /wp:heading -->

<!-- wp:paragraph -->
You can also control lesson access based on WordPress user roles. This allows you to create role-based learning paths where certain lessons are only available to students with specific roles.
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
1. Navigate to the course and open the lesson you want to restrict.
2. In the lesson settings, locate the **Access Restriction** options.
3. Select the option to restrict by **User Role**.
4. Choose the WordPress user role(s) that should have access to this lesson (e.g., "Premium Student", "VIP Member", or any custom role you've created).
5. Click **Save** to apply the restriction.
<!-- /wp:list -->

<!-- wp:paragraph -->
Students who don't have the required role will see the lesson as locked. You can assign roles manually through the WordPress user management screen, or automatically through a membership plugin or automation tool.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Important:** Custom user roles must be created separately in WordPress (using a plugin like Members or User Role Editor) before they appear as options in Thrive Apprentice. The default WordPress roles (Administrator, Editor, Subscriber, etc.) are available by default.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Combining Multiple Conditions
<!-- /wp:heading -->

<!-- wp:paragraph -->
You can layer multiple conditions on a single lesson for more complex access scenarios. For example, you could require that a student both completes the previous lesson and holds a specific user role. When multiple conditions are applied, all conditions must be met before the lesson unlocks.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
**Tip:** Start with simple sequential unlocking for most courses, and only add role-based or cross-course conditions when your curriculum genuinely requires them. Overly complex unlock rules can confuse students.
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
That's it! You've successfully set up conditional lesson unlocking in Thrive Apprentice, giving you full control over how students progress through your course content.
<!-- /wp:paragraph -->

<!-- wp:heading -->
## Related Resources
<!-- /wp:heading -->

<!-- wp:list -->
- **Course Completion Behavior:** Configure what happens when students [complete a course](8-02-course-completion-behavior.md), including redirects and next course suggestions.
- **Manual Lesson Unlocking:** Learn how to [manually unlock lessons for individual students](8-07-unlocking-lesson-manually.md) when exceptions are needed.
- **Access Restrictions and Rules:** Review the full [access restrictions and rules guide](3-01-access-restrictions-and-rules.md) for product-level access control.
- **Drip Scheduling:** Set up [time-based drip schedules](5-01-getting-started-with-drip.md) to release lessons on a schedule.
<!-- /wp:list -->