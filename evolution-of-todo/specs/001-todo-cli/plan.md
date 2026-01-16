# Phase I Technical Plan: In-Memory CLI

## 1. Architectural Strategy
To ensure a smooth transition to future phases (FastAPI, SQLModel), we will use a **Clean Architecture** approach even in this simple CLI.

- **Models Layer**: POBOs (Plain Old Python Objects) using TypedDict or Classes.
- **Service Layer**: Contains the business logic (CRUD operations on the in-memory list).
- **CLI/Presentation Layer**: Handles user input and terminal output.

## 2. Component Design
### 2.1 Service (`TodoService`)
- Encapsulates a Python `list` of `Task` objects.
- Methods: `add_task`, `get_tasks`, `update_task`, `delete_task`, `toggle_completion`.
- Responsibility: Validate business rules (e.g., non-empty titles) and manage auto-incrementing IDs.

### 2.2 CLI (`input_handler` & `menu`)
- `menu.py`: Displays the text-based UI.
- `input_handler.py`: Validates user input types (e.g., ensuring an ID is an integer).

## 3. Implementation Patterns
- **Dependency Injection**: The CLI will be initialized with an instance of `TodoService`.
- **Exception Handling**: Use custom exceptions (e.g., `TaskNotFoundError`) to communicate between service and CLI layers.
- **Type Hinting**: Full type hinting for better maintainability and alignment with future SQLModel/Pydantic use.

## 4. Phase Constraints Compliance
- **Data storage**: Global list within the `TodoService` instance.
- **No external libs**: Only standard library (e.g., `datetime`, `typing`).
- **Entry point**: `main.py` in the project root.
