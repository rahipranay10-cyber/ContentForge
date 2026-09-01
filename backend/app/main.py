from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Conversation
from app.schemas import ConversationRequest
from app.services.context_processor import process_conversation
from dotenv import load_dotenv
from app.models import Conversation, ContextMemoryModel

load_dotenv()
from app.chunk_models import MemoryChunk

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ContextFlow AI",
    description="AI-powered context management backend",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ContextFlow AI",
    }

@app.post("/api/conversations")
def create_conversation(
    conversation: ConversationRequest,
    db: Session = Depends(get_db),
):
    messages = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in conversation.messages
    ]

    # 1. Store the raw conversation
    new_conversation = Conversation(
        platform=conversation.platform,
        source_url=conversation.source_url,
        source_title=conversation.source_title,
        messages=messages,
    )

    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    # 2. Ask our local AI to extract useful context
    context = process_conversation(messages)

    # 3. Store the extracted memory
    memory = ContextMemoryModel(
        conversation_id=new_conversation.id,
        summary=context.summary,
        goals=context.goals,
        decisions=context.decisions,
        completed=context.completed,
        current_task=context.current_task,
        constraints=context.constraints,
        open_questions=context.open_questions,
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    # 4. Return both
    return {
        "conversation_id": new_conversation.id,
        "memory_id": memory.id,
        "context": context.model_dump(),
    }