from sqlalchemy.orm import Session

from app.chunk_models import MemoryChunk
from app.services.chunk_service import chunk_text
from app.services.embedding_service import generate_embedding


def index_conversation(
    db: Session,
    conversation_id: int,
    messages: list[dict],
):
    text = "\n\n".join(
        f"{message['role']}: {message['content']}"
        for message in messages
    )

    chunks = chunk_text(text)

    indexed_chunks = []

    for chunk in chunks:
        embedding = generate_embedding(chunk)

        memory_chunk = MemoryChunk(
            conversation_id=conversation_id,
            content=chunk,
            embedding=embedding,
        )

        db.add(memory_chunk)
        indexed_chunks.append(memory_chunk)

    db.commit()

    return indexed_chunks