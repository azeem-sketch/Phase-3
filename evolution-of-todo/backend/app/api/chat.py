from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_session
# Models will be imported inside functions to avoid global hang
from app.agent.core import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Any]

from app.api.deps import get_current_user
from app.models.user import User

@router.post("/{user_id}/chat", response_model=ChatResponse)
def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: Any = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from app.models import Conversation, Message, Role
    from app.models.user import User
    
    # Check if current_user is a User object
    curr_user_id = getattr(current_user, 'id', None)
    if user_id != str(curr_user_id):
        raise HTTPException(status_code=403, detail="Not authorized to chat on behalf of this user")

    # 1. Get or create conversation
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # 2. Persist User Message
    user_msg = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role=Role.USER,
        content=request.message
    )
    session.add(user_msg)
    session.commit()

    # 3. Load History
    history_stmt = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at)
    history_msgs = session.execute(history_stmt).scalars().all()
    
    agent_history = [{"role": msg.role.value, "content": msg.content} for msg in history_msgs]
    
    agent_result = run_agent(user_id, agent_history)
    
    # 5. Persist Assistant Response
    assistant_msg = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role=Role.ASSISTANT,
        content=agent_result["content"] or "" 
    )
    session.add(assistant_msg)
    session.commit()
    
    return {
        "conversation_id": conversation.id,
        "response": agent_result["content"],
        "tool_calls": agent_result["tool_calls"]
    }

