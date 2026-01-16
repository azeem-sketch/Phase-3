# Phase I Implementation Tasks (Atomic Work Units)

This document breaks down the Phase I Technical Plan into actionable, sequential tasks.

## T1: Models and Core Data Structure
- **Description**: Define the `Task` data class and the storage structure.
- **Preconditions**: None.
- **Expected Output**: A working `Task` class with fields: id, title, description, is_completed, created_at.
- **Artifacts**: `src/todo_app/models/task.py`
- **Spec Ref**: Section 3 (Data Model)

## T2: Service Layer Skeleton
- **Description**: Create the `TodoService` class with a private in-memory list and an ID counter.
- **Preconditions**: T1
- **Expected Output**: `TodoService` instance exists with an empty list and `last_id=0`.
- **Artifacts**: `src/todo_app/services/todo_service.py`
- **Spec Ref**: Section 6 (Architecture)

## T3: Add Task Logic
- **Description**: Implement `TodoService.add_task(title, description)`.
- **Preconditions**: T2
- **Expected Output**: New task is added to the list with an auto-incremented ID and current timestamp.
- **Artifacts**: `src/todo_app/services/todo_service.py`
- **Spec Ref**: Section 2 (User Stories: Add Task), Section 5

## T4: View Tasks Logic
- **Description**: Implement `TodoService.get_all_tasks()`.
- **Preconditions**: T2
- **Expected Output**: Returns the full list of task objects.
- **Artifacts**: `src/todo_app/services/todo_service.py`
- **Spec Ref**: Section 2 (User Stories: View Tasks)

## T5: CLI Menu Loop
- **Description**: Create the main application loop that displays options 1-6 and waits for input.
- **Preconditions**: T2
- **Expected Output**: Terminal shows menu; entering '6' exits the program.
- **Artifacts**: `src/todo_app/cli/menu.py`, `main.py`
- **Spec Ref**: Section 4 (CLI Interaction Flow)

## T6: View Tasks UI Integration
- **Description**: Connect the menu Option 1 to `TodoService.get_all_tasks()`.
- **Preconditions**: T4, T5
- **Expected Output**: Table or list format output in terminal; shows "No tasks found" if empty.
- **Artifacts**: `src/todo_app/cli/menu.py`
- **Spec Ref**: Section 5 (Acceptance Criteria: View)

## T7: Add Task UI Integration
- **Description**: Connect menu Option 2. Prompt user for Title and Description, then call `add_task`.
- **Preconditions**: T3, T5
- **Expected Output**: Successfully adds task and prints confirmation with the new ID.
- **Artifacts**: `src/todo_app/cli/menu.py`
- **Spec Ref**: Section 5 (Acceptance Criteria: Add)

## T8: Update Task Logic and UI
- **Description**: Implement `service.update_task(id, title, desc)` and connect to Option 3.
- **Preconditions**: T5
- **Expected Output**: Modified task details persist in memory during runtime.
- **Artifacts**: `src/todo_app/services/todo_service.py`, `src/todo_app/cli/menu.py`
- **Spec Ref**: Section 2 (Update Task)

## T9: Toggle Completion Logic and UI
- **Description**: Implement `service.toggle_task(id)` and connect to Option 5.
- **Preconditions**: T5
- **Expected Output**: Task status flips (True/False) and is reflected in the list view.
- **Artifacts**: `src/todo_app/services/todo_service.py`, `src/todo_app/cli/menu.py`
- **Spec Ref**: Section 2 (Mark Task Complete)

## T10: Delete Task Logic and UI
- **Description**: Implement `service.delete_task(id)` and connect to Option 4.
- **Preconditions**: T5
- **Expected Output**: Task is removed from list; subsequent attempts to access ID fail.
- **Artifacts**: `src/todo_app/services/todo_service.py`, `src/todo_app/cli/menu.py`
- **Spec Ref**: Section 2 (Delete Task)

## T11: Robustness (Validation & Error Handling)
- **Description**: Update `input_handler.py` to handle non-integers. Add try/except blocks for missing IDs.
- **Preconditions**: All UI tasks
- **Expected Output**: App does not crash on invalid input; informative error messages shown.
- **Artifacts**: `src/todo_app/cli/input_handler.py`
- **Spec Ref**: Section 6 (Error Handling)
