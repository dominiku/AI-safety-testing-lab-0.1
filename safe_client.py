from typing import Self
import requests
from datetime import datetime, timezone
from pathlib import Path
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv

load_dotenv()

CF_ID = os.getenv('CF_ACCESS_CLIENT_ID')
CF_SECRET = os.getenv('CF_ACCESS_CLIENT_SECRET')

OLLAMA_URL = "https://ollama.domhome.priv.pl/api/generate"

# Model switcher
# MODEL = "tinyllama:latest"
# MODEL = "kimi-k2:1t-cloud"
# MODEL = "qwen:1.8b"
MODEL = "qwen:0.5b"
# MODEL = "olmo-3:7b-think"
# MODEL = "deepseek-r1:1.5b"

class Prompt(BaseModel):
    id: str
    text: str
    category: str
    intent: str

def run_prompt(prompt: Prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt.text, 
        "stream": False,
        "options": {
            "num_predict": 256,
            "temperature": 0,
    }}
 
    headers = {}

    if CF_ID and CF_SECRET:
        headers["CF-Access-Client-Id"] = CF_ID
        headers["CF-Access-Client-Secret"] = CF_SECRET

    r = requests.post(OLLAMA_URL, json=payload, headers=headers, timeout=(10, 300))
    r.raise_for_status()

    response = r.json()["response"]

    log = {
        "timestamp": datetime.now().strftime('%Y%m%d-%H%M%S'),
        "prompt": prompt.model_dump(),
        "response": response    
    }

    Path("logs").mkdir(exist_ok=True)
    with open(f"logs/{prompt.id}.json", "w") as f:
        json.dump(log, f, indent=2)

    return response

if __name__ == "__main__":
    with open("prompts/SAF-DUMMY-001.json") as f:
        data = json.load(f)

    prompt = Prompt(**data)
    response = run_prompt(prompt)
    print(response)