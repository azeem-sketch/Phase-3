import json
from sqlmodel import Session, select
from mcp.server.fastmcp import FastMCP
from app.database import engine
from app.models import Todo

mcp = FastMCP("TodoMCP")

@mcp.tool()
def add_task(user_id: str, title: str, description: str = None) -> str:
    """Create a new task for the user."""
    with Session(engine) as session:
        task = Todo(user_id=int(user_id) if user_id.isdigit() else user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({
            "task_id": task.id,
            "status": "created",
            "title": task.title
        })

@mcp.tool()
def list_tasks(user_id: str, status: str = None) -> str:
    """List tasks for the user."""
    with Session(engine) as session:
        uid = int(user_id) if user_id.isdigit() else user_id
        statement = select(Todo).where(Todo.user_id == uid)
        if status:
            if status.lower() == "completed":
                statement = statement.where(Todo.completed == True)
            elif status.lower() == "pending":
                statement = statement.where(Todo.completed == False)
        
        tasks = session.exec(statement).all()
        return json.dumps([t.model_dump() for t in tasks], default=str)

@mcp.tool()
def complete_task(user_id: str, task_id: int) -> str:
    """Mark a task as completed."""
    with Session(engine) as session:
        uid = int(user_id) if user_id.isdigit() else user_id
        task = session.exec(select(Todo).where(Todo.id == task_id, Todo.user_id == uid)).first()
        if not task:
            return json.dumps({"error": "Task not found"})
        
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return json.dumps({
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        })

@mcp.tool()
def delete_task(user_id: str, task_id: int) -> str:
    """Delete a task."""
    with Session(engine) as session:
        uid = int(user_id) if user_id.isdigit() else user_id
        task = session.exec(select(Todo).where(Todo.id == task_id, Todo.user_id == uid)).first()
        if not task:
            return json.dumps({"error": "Task not found"})
        
        session.delete(task)
        session.commit()
        
        return json.dumps({
            "task_id": task_id,
            "status": "deleted",
            "title": task.title
        })

@mcp.tool()
def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> str:
    """Update a task's title or description."""
    with Session(engine) as session:
        uid = int(user_id) if user_id.isdigit() else user_id
        task = session.exec(select(Todo).where(Todo.id == task_id, Todo.user_id == uid)).first()
        if not task:
            return json.dumps({"error": "Task not found"})
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
            
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return json.dumps({
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        })
