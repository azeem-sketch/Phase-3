import sys
from ..services.todo_service import TodoService

class CLIHandler:
    def __init__(self, service: TodoService):
        self.service = service

    def display_menu(self):
        print("\n=== EVOLUTION OF TODO: PHASE I (CLI) ===")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Completion")
        print("6. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nSelect an option (1-6): ").strip()

            try:
                if choice == "1":
                    self.view_tasks()
                elif choice == "2":
                    self.add_task()
                elif choice == "3":
                    self.update_task()
                elif choice == "4":
                    self.delete_task()
                elif choice == "5":
                    self.toggle_task()
                elif choice == "6":
                    print("Exiting application. Goodbye!")
                    sys.exit(0)
                else:
                    print("Error: Invalid selection. Please enter a number between 1 and 6.")
            except Exception as e:
                print(f"Error: {str(e)}")

    def view_tasks(self):
        tasks = self.service.get_all_tasks()
        if not tasks:
            print("\nNo tasks found.")
            return

        print("\nID  | Status | Title")
        print("-" * 30)
        for t in tasks:
            status = "[x]" if t.is_completed else "[ ]"
            print(f"{t.id:<3} | {status}    | {t.title}")

    def add_task(self):
        title = input("Enter Task Title: ").strip()
        description = input("Enter Description (optional): ").strip()
        task = self.service.add_task(title, description)
        print(f"Success: Task {task.id} added.")

    def update_task(self):
        tasks = self.service.get_all_tasks()
        if not tasks:
            print("\nNo tasks to update.")
            return

        task_id = self._get_id_input()
        if task_id is None: return

        try:
            task = self.service.get_task_by_id(task_id)
            print(f"Updating Task: {task.title}")
            print("Leave blank to keep current value.")
            new_title = input(f"New Title ({task.title}): ") or None
            new_desc = input(f"New Description ({task.description or 'None'}): ") or None

            self.service.update_task(task_id, new_title, new_desc)
            print("Success: Task updated.")
        except KeyError as e:
            print(f"Error: {e}")

    def delete_task(self):
        tasks = self.service.get_all_tasks()
        if not tasks:
            print("\nNo tasks to delete.")
            return

        task_id = self._get_id_input()
        if task_id is None: return

        try:
            self.service.delete_task(task_id)
            print("Success: Task deleted.")
        except KeyError as e:
            print(f"Error: {e}")

    def toggle_task(self):
        tasks = self.service.get_all_tasks()
        if not tasks:
            print("\nNo tasks to toggle.")
            return

        task_id = self._get_id_input()
        if task_id is None: return

        try:
            task = self.service.toggle_task_completion(task_id)
            status = "Completed" if task.is_completed else "Incomplete"
            print(f"Success: Task {task_id} is now {status}.")
        except KeyError as e:
            print(f"Error: {e}")

    def _get_id_input(self) -> int | None:
        val = input("Enter Task ID: ").strip()
        if not val.isdigit():
            print("Error: ID must be a number.")
            return None
        return int(val)
