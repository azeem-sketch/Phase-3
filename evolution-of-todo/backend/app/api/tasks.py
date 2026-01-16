"""Task CRUD endpoints (Phase II Refactor)."""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.core.exceptions import NotFoundError, AuthorizationError
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["Tasks"])

def verify_user_match(user_id: int, current_user: User):
    """Ensure the user_id in the URL matches the authenticated user."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own tasks"
        )

@router.get("", response_model=List[TodoResponse])
def get_tasks(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all tasks for a specific user."""
    verify_user_match(user_id, current_user)
    statement = select(Todo).where(Todo.user_id == user_id)
    return session.exec(statement).all()

@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: int,
    task_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for a specific user."""
    verify_user_match(user_id, current_user)
    task = Todo(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{id}", response_model=TodoResponse)
def get_task_details(
    user_id: int,
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get details of a specific task."""
    verify_user_match(user_id, current_user)
    task = session.get(Todo, id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{id}", response_model=TodoResponse)
def update_task(
    user_id: int,
    id: int,
    task_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task."""
    verify_user_match(user_id, current_user)
    task = session.get(Todo, id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
    
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: int,
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task."""
    verify_user_match(user_id, current_user)
    task = session.get(Todo, id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return None

@router.patch("/{id}/complete", response_model=TodoResponse)
def toggle_task_completion(
    user_id: int,
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task."""
    verify_user_match(user_id, current_user)
    task = session.get(Todo, id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
