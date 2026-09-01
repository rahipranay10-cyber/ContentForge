from app.services.context_processor import process_conversation


messages = [
    {
        "role": "user",
        "content": (
            "I'm building an ecommerce backend using FastAPI "
            "and PostgreSQL. I need JWT authentication."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "Use FastAPI for the API layer, PostgreSQL for "
            "persistence, and JWT for authentication."
        ),
    },
    {
        "role": "user",
        "content": "Let's implement the authentication service next.",
    },
]


result = process_conversation(messages)

print("\n=== STRUCTURED CONTEXT ===")
print(result.model_dump())