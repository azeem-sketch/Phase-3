# Prompt: Generate Phase I Atomic Tasks

This prompt follows the Constitution's mandate to break the Plan into verifiable "Work Units".

```markdown
/sp.task Break the Phase I technical plan into atomic implementation tasks.

Each task must include:
- Task ID (e.g., T1, T2)
- Clear description: What exactly needs to be coded.
- Preconditions: What must be finished first.
- Expected output: How to know it works.
- Artifacts: File paths to be created or modified.
- Spec Reference: Link to the specific section in `specs/001-todo-cli/specification.md`.

Tasks must cover:
1. Task data model and in-memory storage (Service Layer)
2. CLI menu and application loop (UI Layer)
3. Add task functionality
4. View task list functionality
5. Update task functionality (Title and Description)
6. Delete task functionality
7. Mark task complete/incomplete functionality
8. Input validation (IDs, Menu choices)
9. Application startup and exit flow

Rules:
- Tasks must be small, testable, and sequential.
- Do NOT introduce new features (No categories, No persistence).
- Do NOT include future phases.
- Tasks must be sufficient to fully implement Phase I as described in the Specs and Plan.

Deliver the result as `specs/001-todo-cli/tasks.md`.
```
