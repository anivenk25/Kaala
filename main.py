# main.py

from fastapi import FastAPI
from scheduler import (
    read_schedule, update_schedule, append_task,
    mark_task_done, delete_schedule,
    summarize_schedule, suggest_next_task, list_time_blocks
)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Kaala JARVIS scheduler is online."}

@app.get("/read")
def api_read(date: str):
    return {"schedule": read_schedule(date)}

@app.post("/update")
def api_update(date: str, content: str):
    return {"message": update_schedule(date, content)}

@app.post("/append")
def api_append(date: str, time: str, task: str):
    return {"message": append_task(date, time, task)}

@app.post("/done")
def api_done(date: str, task_text: str):
    return {"message": mark_task_done(date, task_text)}

@app.get("/summary")
def api_summary(date: str):
    return {"summary": summarize_schedule(date)}

@app.get("/suggest")
def api_suggest(date: str):
    return {"suggestion": suggest_next_task(date)}

@app.get("/blocks")
def api_blocks(date: str):
    return {"blocks": list_time_blocks(date)}

@app.delete("/delete")
def api_delete(date: str):
    return {"message": delete_schedule(date)}

