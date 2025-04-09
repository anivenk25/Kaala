# tools.py

from typing import List

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_schedule",
            "description": "Read the schedule for a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"}
                },
                "required": ["date"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "append_task",
            "description": "Append a new task to the schedule.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "time": {"type": "string"},
                    "task": {"type": "string"},
                },
                "required": ["date", "time", "task"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mark_task_done",
            "description": "Mark a task as done.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "task_text": {"type": "string"},
                },
                "required": ["date", "task_text"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_schedule",
            "description": "Summarize how many tasks are done vs total.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"}
                },
                "required": ["date"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_next_task",
            "description": "Suggest the next undone task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"}
                },
                "required": ["date"]
            },
        },
    },
]

