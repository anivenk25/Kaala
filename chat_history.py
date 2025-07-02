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
    """
    Load up to the last `limit` user-assistant exchanges from all history files.
    Returns a list of message dicts formatted for OpenAI: {'role': ..., 'content': ...}.
    """
    # Collect lines from all history files in chronological order
    files = sorted(os.listdir(HISTORY_DIR))
    all_lines = []
    for filename in files:
        if not filename.endswith('.txt'):
            continue
        path = os.path.join(HISTORY_DIR, filename)
        try:
            with open(path, 'r') as f:
                all_lines.extend(f.readlines())
        except OSError:
            continue
    # Take the last limit * 2 lines (each exchange has user + assistant)
    lines = all_lines[-(limit * 2):] if all_lines else []

    messages = []
    for line in lines:
        # Expect lines of form 'user: ...' or 'assistant: ...'
        if line.startswith('user:'):
            messages.append({'role': 'user', 'content': line[len('user:'):].strip()})
        elif line.startswith('assistant:'):
            messages.append({'role': 'assistant', 'content': line[len('assistant:'):].strip()})
    return messages


