import os
from datetime import datetime

HISTORY_DIR = "chat_history"
os.makedirs(HISTORY_DIR, exist_ok=True)

def get_today_file():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(HISTORY_DIR, f"{today}.txt")

def save_to_history(role: str, message: str):
    assert role in ("user", "assistant")
    with open(get_today_file(), "a") as f:
        f.write(f"{role}: {message.strip()}\n")

def load_recent_history(limit=10):
    path = get_today_file()
    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        lines = f.readlines()[-limit * 2:]  # Each interaction is 2 lines: user + assistant

    messages = []
    for line in lines:
        if line.startswith("user:"):
            messages.append({"role": "user", "content": line[len("user:"):].strip()})
        elif line.startswith("assistant:"):
            messages.append({"role": "assistant", "content": line[len("assistant:"):].strip()})
    return messages

