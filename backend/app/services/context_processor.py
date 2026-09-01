import json
import urllib.request

from app.schemas import ContextMemory


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:1.7b"

def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["response"]


def process_conversation(messages) -> ContextMemory:
    conversation_text = "\n\n".join(
        f"{message['role']}: {message['content']}"
        for message in messages
    )

    prompt = f"""
You are a context extraction engine.

Analyze the conversation below.

Extract information that would help another AI continue
the user's work later.

Return ONLY valid JSON.
Do not use markdown.
Do not include explanations.

Use exactly this structure:

{{
  "summary": "string",
  "goals": ["string"],
  "decisions": ["string"],
  "completed": ["string"],
  "current_task": "string or null",
  "constraints": ["string"],
  "open_questions": ["string"]
}}

Conversation:

{conversation_text}
"""

    raw_output = call_ollama(prompt)

    print("=== OLLAMA OUTPUT ===")
    print(raw_output)

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Ollama returned invalid JSON: {raw_output}"
        ) from error

    return ContextMemory.model_validate(parsed)