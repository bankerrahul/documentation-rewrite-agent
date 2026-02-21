# Feature: Disable Quiz Stat Collection in Thrive Quiz Builder

## Overview
We are introducing a new feature to help users control database size and performance by allowing them to disable quiz statistics collection. This is particularly useful for high-traffic sites where stats tables can grow extremely large.

## New Settings
A new section "Quiz stats and data" has been added to the Thrive Quiz Builder General Settings.

### 1. Enable stats tracking for all quizzes
*   **Type:** Toggle Switch
*   **Default:** On (for existing users to maintain behavior)
*   **Function:**
    *   When **ON**: Quiz statistics are collected as usual.
    *   When **OFF**: No new statistics will be recorded for any quiz. The "Automatically clear old stats" option will be hidden.

### 2. Automatically clear old stats
*   **Type:** Toggle Switch + Duration Selector
*   **Visibility:** Only visible when "Enable stats tracking" is ON.
*   **Function:**
    *   Allows users to set a retention period for statistics (e.g., keep data for X days/weeks/months).
    *   Old data beyond this period will be automatically deleted to save space.

## Notes for Documentation
*   This is a global setting that affects ALL quizzes.
*   Disabling tracking does NOT delete existing data immediately; it just stops collecting new data.
*   The automatic cleanup is a separate process that runs to prune old data.
