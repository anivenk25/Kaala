import os
import json
from datetime import datetime

HISTORY_DIR = "chat_history"
os.makedirs(HISTORY_DIR, exist_ok=True)

def get_today_file(extension=".jsonl"):
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(HISTORY_DIR, f"{today}{extension}")

def save_message(message: dict):
    """
    Save a single message dictionary (OpenAI format) to today's JSONL history file.
    """
    with open(get_today_file(".jsonl"), "a") as f:
        f.write(json.dumps(message) + "\n")

def save_to_history(role: str, message: str):
    """Legacy support: saves a simple text message."""
    save_message({"role": role, "content": message.strip()})

def load_recent_history(limit=15):
    """
    Load up to the last `limit` messages from history files.
    Supports both legacy .txt (plain text) and new .jsonl (JSON objects).
    """
    if not os.path.exists(HISTORY_DIR):
        return []
        
    files = sorted(os.listdir(HISTORY_DIR))
    all_messages = []
    
    for filename in files:
        path = os.path.join(HISTORY_DIR, filename)
        try:
            with open(path, 'r') as f:
                if filename.endswith('.jsonl'):
                    for line in f:
                        if line.strip():
                            all_messages.append(json.loads(line))
                elif filename.endswith('.txt'):
                    # Legacy support
                    for line in f:
                        if line.startswith('user:'):
                            all_messages.append({'role': 'user', 'content': line[len('user:'):].strip()})
                        elif line.startswith('assistant:'):
                            all_messages.append({'role': 'assistant', 'content': line[len('assistant:'):].strip()})
        except (OSError, json.JSONDecodeError):
            continue
            
    return all_messages[-limit:] if all_messages else []



