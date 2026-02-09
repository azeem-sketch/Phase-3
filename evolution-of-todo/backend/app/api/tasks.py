from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_session
# Deferred imports inside endpoints
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.api.deps import get_current_user
from typing import Any, List

router = APIRouter(prefix="/todos", tags=["Tasks"])

@router.get("", response_model=List[TodoResponse])
def get_tasks(
    current_user: Any = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all tasks for a specific user."""
    from app.models.todo import Todo
    statement = select(Todo).where(Todo.user_id == current_user.id)
    return session.execute(statement).scalars().all()

@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TodoCreate,
    current_user: Any = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for a specific user."""
    from app.models.todo import Todo
    task = Todo(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{id}", response_model=TodoResponse)
def get_task_details(
    id: int,
    current_user: Any = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get details of a specific task."""
    from app.models.todo import Todo
    task = session.get(Todo, id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{id}", response_model=TodoResponse)
def update_task(
    id: int,
    task_data: TodoUpdate,
    current_user: Any = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task."""
    from app.models.todo import Todo
    task = session.get(Todo, id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
    
    from datetime import datetime
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    id: int,
    current_user: Any = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task."""
    from app.models.todo import Todo
    task = session.get(Todo, id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return None

@router.patch("/{id}/complete", response_model=TodoResponse)
def toggle_task_completion(
    id: int,
    current_user: Any = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task."""
    from app.models.todo import Todo
    task = session.get(Todo, id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = not task.completed
    from datetime import datetime
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


