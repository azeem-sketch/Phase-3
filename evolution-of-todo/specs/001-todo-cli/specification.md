# Phase I Specification: In-Memory Todo CLI

## 1. Overview
Phase I of the "Evolution of Todo" project focus on building a fundamental, in-memory Python console application. This version is strictly limited to runtime execution with no data persistence.

## 2. User Stories
- **Add Task**: As a user, I want to add a new task with a title and optional description so I can track my work.
- **View Tasks**: As a user, I want to see a list of all my tasks with their IDs and statuses so I can see what is pending.
- **Update Task**: As a user, I want to edit a task's title or description if I made a mistake or my plans changed.
- **Delete Task**: As a user, I want to remove a task from my list once it is no longer relevant.
- **Toggle Completion**: As a user, I want to mark a task as completed or incomplete to track my progress.

## 3. Data Model
Each `Task` object must contain:
| Field | Type | Constraints |
| :--- | :--- | :--- |
| `id` | Integer | Unique, auto-incrementing during runtime |
| `title` | String | Required, non-empty, max 100 characters |
| `description` | String | Optional |
| `is_completed` | Boolean | Defaults to `False` |
| `created_at` | DateTime | Timestamp of creation (runtime only) |

## 4. CLI Interaction Flow
The application will operate in a continuous loop with the following menu:
1. View Tasks
2. Add Task
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Exit

## 5. Acceptance Criteria
- **Add**: Task is assigned a unique ID; Title validation prevents empty strings.
- **View**: If no tasks exist, a "No tasks found" message is displayed.
- **Update**: User must provide a valid ID; only changed fields are updated.
- **Delete**: User must provide a valid ID; record is removed from the in-memory list.
- **Toggle**: Status flips between Complete and Incomplete based on current state.

## 6. Error Handling
- **Invalid ID**: Display error if the user enters an ID that does not exist.
- **Input Validation**: Menu selection must be a number between 1-6. Non-numeric input should be caught and the menu re-displayed.
- **Empty Title**: Prevent creation of tasks without a title.

## 7. Constitution & Phase Constraints
- **Architecture**: Logic must be separated (e.g., Service layer for logic, CLI layer for I/O).
- **No Persistence**: Data is lost when the program exits. No `sqlite`, `json`, or `txt` files.
- **No Networking**: No FastAPI, no HTTP, no external dependencies outside standard library.
- **Strict Scope**: No priority levels, no categories, no due dates.
