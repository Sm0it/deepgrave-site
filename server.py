from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Update with your Ollama instance/model as needed
OLLAMA_URL = "http://192.168.0.237:11434/api/generate"
OLLAMA_MODEL = "mistral:latest"

app = Flask(__name__)
CORS(app)

def format_prompt(user_input):
    base = (
        "You are a Linux terminal on the Deepgrave Penitentiary security server in the Red Rising universe. Sevro au Barca is logged in as admin.\n"
        "\nRules:\n"
        "- Output ONLY the direct result of the SINGLE user command just received.\n"
        "- Do NOT invent or output any extra commands, session logs, prompts, or follow-ups—just the immediate output for the command.\n"
        "- Output must fit the Red Rising universe only. Do NOT use real-world people, places, tech, or history.\n"
        "- If a command is unrecognized: output 'bash: <command>: command not found'\n"
        "- If a file does not exist: output 'bash: cat: <filename>: No such file or directory'\n"
        "- If the command would return nothing (like 'clear' or just pressing enter): output nothing.\n"
        "- Never explain, never suggest, never narrate—just literal terminal output.\n"
        "- Never output markdown, commentary, or code blocks—just terminal output.\n"
        "- Only use Red Rising lore and names if outputting files or content, but ONLY when the command requests it.\n"
        "- Ignore any previous context or conversation—just respond to the current command, as a real Linux terminal would.\n"
        "- Do NOT invent any extra files, commands, or session history not specifically requested by the user command.\n"
        "- If command is 'exit', output '[Session ended]' and nothing else.\n"
        "\nRespond ONLY with the terminal output for the user command. NOTHING else."
    )
    prompt = f"{base}\n$ {user_input}\n"
    return prompt



@app.route('/api/terminal', methods=['POST'])
def terminal():
    print(">>> Received a POST to /api/terminal")
    data = request.get_json(force=True, silent=True)
    print(f">>> Request data: {data}")
    if not data or 'input' not in data:
        print(">>> ERROR: No input provided in request")
        return jsonify({"output": "[No input provided]"})
    user_input = data.get('input', '')
    prompt = format_prompt(user_input)
    print(f">>> Built prompt:\n{prompt}")
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        print(f">>> Ollama status code: {resp.status_code}")
        resp.raise_for_status()
        json_resp = resp.json()
        print(f">>> Ollama raw response: {json_resp}")
        ai_reply = json_resp.get('response', '').strip()
        print(f">>> AI reply: {ai_reply}")
        return jsonify({"output": ai_reply})
    except Exception as e:
        print(f">>> ERROR communicating with Ollama: {e}")
        return jsonify({"output": "[Error from AI]"})

if __name__ == "__main__":
    print(">>> Starting Flask backend...")
    app.run(host='0.0.0.0', port=5000, debug=True)
