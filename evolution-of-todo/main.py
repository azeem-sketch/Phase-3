from src.todo_app.services.todo_service import TodoService
from src.todo_app.cli.menu import CLIHandler

def main():
    service = TodoService()
    app = CLIHandler(service)
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
