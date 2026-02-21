# How to Understand Quiz Types in Thrive Quiz Builder

Choosing the right quiz type is essential for delivering the correct results and feedback to your users. In this article, you'll learn about the five available quiz types, how they calculate scores, and when to use each one.

## Overview of Quiz Types

Thrive Quiz Builder offers five ways to evaluate user answers. You can choose your quiz type during the initial setup or change it later from the **Quiz Type** card on your dashboard.

---

## 1. The Number Quiz Type

The **Number** quiz type assigns points to each answer. The final result is the total sum of all points earned throughout the quiz.

* **Best for:** Personality tests where specific traits are weighted, or simple "points-based" games.
* **How it works:** When adding answers to your questions, you assign a numerical value (points) to each option.
* **Result:** The user sees a final number (e.g., "You scored 45 points!").

---

## 2. The Percentage Quiz Type

The **Percentage** quiz type calculates how well a user performed relative to the maximum possible score.

* **Best for:** Knowledge tests, exams, or any quiz where a score out of 100 is expected.
* **How it works:** You assign points to answers similar to the Number quiz. The system automatically identifies the maximum possible points available in the quiz path the user takes.
* **Calculation Formula:**
    Thrive Quiz Builder uses a precise formula to calculate the percentage, even if your minimum score isn't zero:
    `[(Points obtained - Minimum possible points) * 100] / (Maximum possible points - Minimum possible points)`
* **Result:** The user sees a percentage (e.g., "Your score: 85%").

---

## 3. The Category Quiz Type

The **Category** quiz type assigns users to a specific group or "bucket" (e.g., "Which Star Wars Character are you?").

* **Best for:** Segmentation, personality profiles, or product recommendations.
* **How it works:**
    1. Create your categories (e.g., Category A, Category B).
    2. Link each answer to one or more categories.
    3. Assign "weights" to answers to make certain choices more impactful.
* **Handling Tie-Breaks:**
    If a user scores equally in two or more categories, the system uses the **Result Order** to break the tie. The category listed **highest** in your **Quiz Settings** list will be the one displayed as the result.

---

## 4. The Right/Wrong Quiz Type

The **Right/Wrong** quiz type tracks correct answers and is designed for traditional quizzes and tests.

* **Best for:** Knowledge assessments and certifications.
* **How it works:**
  * You define which answer(s) are correct for each question.
  * You can enable **Highlighted Answers** to give users immediate feedback (Green for correct, Red for incorrect) after they make a choice.
* **Navigation:** In this type, question navigation is often simplified to a binary "Next" flow.
* **Result:** The score is displayed as a fraction (e.g., "7/10 Correct").

---

## 5. The Survey Quiz Type

The **Survey** quiz type is unique because it does not assign any score, points, or categories.

* **Best for:** Market research, gathering feedback, or lead generation where segmentation isn't required.
* **How it works:** It simply records the user's input for every question.
* **Result:** Users typically see a "Thank You" page or a customized message once they complete the questions.

---

## Technical Logic & Navigation Settings

No matter which quiz type you choose, you can customize the user's progress through the **Settings** gear icon in the Questions editor:

* **Feedback:** Choose if users see immediate feedback after each question (Timed or until they click "Next").
* **Feedback:** Choose if users see immediate feedback after each question (Timed or until they click "Next").
* **Navigation:** Enable or disable the "Back" button to allow or prevent users from changing previous answers.

---

## Related Resources

* **Getting Started:** [How to Build Your First Quiz Using Thrive Quiz Builder](how-to-build-your-first-quiz-using-thrive-quiz-builder)
* **Templates:** [Choosing and Customizing Quiz Templates](how-to-choose-and-customize-quiz-templates)
* **GDPR:** [GDPR Compliance and User Profiling in Quizzes](gdpr-compliance-and-user-profiling-in-quizzes)

**Thrive Quiz Builder Documentation:** Explore the full [Thrive Quiz Builder knowledge base](https://thrivethemes.com/docs-categories/thrive-quiz-builder/)
