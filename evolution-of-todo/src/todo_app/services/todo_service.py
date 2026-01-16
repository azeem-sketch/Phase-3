from typing import List, Optional
from ..models.task import Task

class TodoService:
    def __init__(self):
        self._tasks: List[Task] = []
        self._last_id: int = 0

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")

        self._last_id += 1
        new_task = Task(
            id=self._last_id,
            title=title.strip(),
            description=description.strip() if description else None
        )
        self._tasks.append(new_task)
        return new_task

    def get_all_tasks(self) -> List[Task]:
        return self._tasks

    def get_task_by_id(self, task_id: int) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"Task with ID {task_id} not found.")

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        task = self.get_task_by_id(task_id)
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty.")
            task.title = title.strip()
        if description is not None:
            task.description = description.strip()
        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        self._tasks.remove(task)
        return True

    def toggle_task_completion(self, task_id: int) -> Task:
        task = self.get_task_by_id(task_id)
        task.is_completed = not task.is_completed
        return task
