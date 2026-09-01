from pydantic import BaseModel
from typing import Optional,List


class Message(BaseModel):
    role: str
    content: str


class ConversationRequest(BaseModel):
    platform: str
    source_url: str
    source_title: Optional[str] = None
    messages: list[Message]

class ContextMemory(BaseModel):
    summary: str
    goals: List[str]
    decisions: List[str]
    completed: List[str]
    current_task: Optional[str] = None
    constraints: List[str]
    open_questions: List[str]