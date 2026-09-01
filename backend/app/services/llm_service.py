from openai import OpenAI
from app.schemas import ContextMemory


client = OpenAI()


def generate_context(messages):
    conversation_text = "\n\n".join(
        f"{message['role']}: {message['content']}"
        for message in messages
    )

    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Analyze this AI conversation and extract useful "
                    "context that would help another AI continue the work. "
                    "Focus on the user's goals, decisions, completed work, "
                    "current task, constraints, and open questions."
                ),
            },
            {
                "role": "user",
                "content": conversation_text,
            },
        ],
        text_format=ContextMemory,
    )

    return response.output_parsed