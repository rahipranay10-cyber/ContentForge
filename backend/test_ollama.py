import json
import urllib.request


url = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen3:4b",
    "prompt": "Say hello in one sentence.",
    "stream": False,
}

data = json.dumps(payload).encode("utf-8")

request = urllib.request.Request(
    url,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(request, timeout=120) as response:
    result = json.loads(response.read().decode("utf-8"))

print("Status:", response.status)
print("Response:", result["response"])