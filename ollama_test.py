import requests

OLLAMA_URL = "http://192.168.0.237:11434/api/generate"

response = requests.post(
    OLLAMA_URL,
    json={
        "model": "mistral:latest",
        "prompt": "Say hello from the Society shell.",
        "stream": False
    },
    timeout=60
)

print(response.status_code)
print(response.json())
