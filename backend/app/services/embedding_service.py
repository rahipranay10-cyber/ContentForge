import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "qwen3-embedding:0.6b"


def generate_embedding(text: str) -> list[float]:
    payload = {
        "model": EMBEDDING_MODEL,
        "input": text,
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

    return result["embeddings"][0]