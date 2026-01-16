"""Todo CRUD endpoints."""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.core.exceptions import NotFoundError, AuthorizationError
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/todos", tags=["Todos"])

@router.get("", response_model=List[TodoResponse])
def get_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all todos for the current user."""
    statement = select(Todo).where(Todo.user_id == current_user.id)
    todos = session.exec(statement).all()
    return todos

@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new todo for the current user."""
    todo = Todo(
        user_id=current_user.id,
        title=todo_data.title,
        description=todo_data.description
    )
    
    session.add(todo)
    session.commit()
    session.refresh(todo)
    
    return todo

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific todo by ID."""
    todo = session.get(Todo, todo_id)
    
    if not todo:
        raise NotFoundError("Todo not found")
    
    if todo.user_id != current_user.id:
        raise AuthorizationError("Access denied")
    
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a todo (full update)."""
    todo = session.get(Todo, todo_id)
    
    if not todo:
        raise NotFoundError("Todo not found")
    
    if todo.user_id != current_user.id:
        raise AuthorizationError("Access denied")
    
    # Update fields
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.description is not None:
        todo.description = todo_data.description
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
    
    todo.updated_at = datetime.utcnow()
    
    session.add(todo)
    session.commit()
    session.refresh(todo)
    
    return todo

@router.patch("/{todo_id}", response_model=TodoResponse)
def patch_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a todo (partial update)."""
    # Same implementation as PUT for this phase
    return update_todo(todo_id, todo_data, current_user, session)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a todo."""
    todo = session.get(Todo, todo_id)
    
    if not todo:
        raise NotFoundError("Todo not found")
    
    if todo.user_id != current_user.id:
        raise AuthorizationError("Access denied")
    
    session.delete(todo)
    session.commit()
    
    return None
