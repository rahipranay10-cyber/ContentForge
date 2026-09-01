from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    platform: Mapped[str] = mapped_column(String(50))
    source_url: Mapped[str] = mapped_column(Text)
    source_title: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    messages: Mapped[list] = mapped_column(JSONB)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


class ContextMemoryModel(Base):
    __tablename__ = "context_memories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    goals: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    decisions: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    completed: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    current_task: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    constraints: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    open_questions: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    conversation = relationship(
        "Conversation",
        backref="memory",
    )