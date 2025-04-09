# scheduler.py

import os
from datetime import datetime

SCHEDULE_DIR = "schedules"
os.makedirs(SCHEDULE_DIR, exist_ok=True)

def get_schedule_path(date: str) -> str:
    return os.path.join(SCHEDULE_DIR, f"{date}.txt")

def create_schedule_if_missing(date: str):
    path = get_schedule_path(date)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"# Schedule for {date}\n\n")
            f.write("09:00 - 10:00 | [ ] Morning routine\n")
            f.write("10:00 - 12:00 | [ ] Deep work session\n")
            f.write("14:00 - 15:00 | [ ] Learn something new\n")
        return f"Created new schedule for {date}."
    return None

def read_schedule(date: str):
    create_schedule_if_missing(date)
    path = get_schedule_path(date)
    with open(path, "r") as f:
        return f.read()

def update_schedule(date: str, new_content: str):
    path = get_schedule_path(date)
    with open(path, "w") as f:
        f.write(new_content)
    return f"Updated schedule for {date}."

def append_task(date: str, time: str, task: str):
    path = get_schedule_path(date)
    line = f"{time} | [ ] {task}\n"
    with open(path, "a") as f:
        f.write(line)
    return f"Appended task to {date}: {task}"

def mark_task_done(date: str, task_text: str):
    path = get_schedule_path(date)
    if not os.path.exists(path):
        return "Schedule not found."
    with open(path, "r") as f:
        lines = f.readlines()
    updated = []
    found = False
    for line in lines:
        if task_text in line and "[ ]" in line:
            updated.append(line.replace("[ ]", "[x]"))
            found = True
        else:
            updated.append(line)
    with open(path, "w") as f:
        f.writelines(updated)
    return "Task marked as done." if found else "Task not found."

def summarize_schedule(date: str):
    schedule = read_schedule(date)
    lines = schedule.splitlines()
    total = sum(1 for l in lines if "| [ ]" in l or "| [x]" in l)
    done = sum(1 for l in lines if "| [x]" in l)
    return f"{done}/{total} tasks completed."

def list_time_blocks(date: str):
    schedule = read_schedule(date)
    blocks = [line.split(" | ")[0] for line in schedule.splitlines() if " | " in line]
    return "Scheduled time blocks:\n" + "\n".join(blocks)

def suggest_next_task(date: str):
    schedule = read_schedule(date)
    for line in schedule.splitlines():
        if "| [ ]" in line:
            return f"Next task: {line.strip()}"
    return "All tasks completed!"

def delete_schedule(date: str):
    path = get_schedule_path(date)
    if os.path.exists(path):
        os.remove(path)
        return f"Deleted schedule for {date}."
    return "Schedule not found."

