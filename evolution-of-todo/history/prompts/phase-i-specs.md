# Prompt: Generate Phase I Specification

This prompt is designed to generate the "WHAT" for Phase I, adhering strictly to the Global Constitution.

```markdown
/sp.specify Create the Phase I specification for the "Evolution of Todo" project.

Phase I Scope:
- In-memory Python console application
- Single user
- No persistence beyond runtime (stateless between executions)

Required Features (Basic Level ONLY):
1. Add Task: Capture title and optional description.
2. View Task List: Display all tasks with their IDs, titles, and statuses.
3. Update Task: Modify existing task title or description.
4. Delete Task: Remove a task by ID.
5. Mark Task Complete / Incomplete: Toggle status.

Specification must include:
- Clear user stories for each feature (As a user, I want to...)
- Task data model (ID, Title, Description, Is_Completed, Created_At)
- CLI interaction flow (Simple menu-driven loop: 1. Add, 2. View, etc.)
- Acceptance criteria for each feature (e.g., "ID must be unique", "Title cannot be empty")
- Error cases (e.g., invalid ID selection, non-numeric input for menu)

Strict Constraints (Constitution Compliance):
- No databases (Neon/SQLModel concepts forbidden in this phase)
- No files (no JSON/TXT storage)
- No authentication or multi-user support
- No web, FastAPI, or API concepts
- No advanced features (no tags, priorities, or categories)
- No references to future phases except to acknowledge phase boundaries

Deliver the result as `specs/001-todo-cli/specification.md`.
This specification must comply with the global constitution and fully define WHAT Phase I must deliver.
```
