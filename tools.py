# tools.py

from typing import List

tools = [
    {
        "type": "function",
        "function": {
            "name": "sync_schedule_folder_to_calendar",
            "description": "Sync all schedule text files in a folder to Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {"type": "string", "default": "schedules"}
                }
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "sync_calendar_to_schedule",
            "description": "Export upcoming Google Calendar events into local schedule text files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {"type": "string", "default": "schedules"}
                }
            }
        }
    },


    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Create a new event on Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "start_time_str": {"type": "string", "description": "ISO 8601 format"},
                    "end_time_str": {"type": "string", "description": "ISO 8601 format"},
                },
                "required": ["summary", "start_time_str", "end_time_str"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_today_events",
            "description": "Lists today's Google Calendar events.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
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

    {
    "type": "function",
    "function": {
        "name": "delete_calendar_event",
        "description": "Delete a Google Calendar event by its ID",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The ID of the event to delete"
                }
            },
            "required": ["event_id"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "update_calendar_event",
        "description": "Update details of a Google Calendar event by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The ID of the event to update"
                },
                "summary": {
                    "type": "string",
                    "description": "Updated event title"
                },
                "start_time_str": {
                    "type": "string",
                    "description": "Updated start time (RFC3339 format)"
                },
                "end_time_str": {
                    "type": "string",
                    "description": "Updated end time (RFC3339 format)"
                }
            },
            "required": ["event_id"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "list_upcoming_events",
        "description": "List upcoming Google Calendar events",
        "parameters": {
            "type": "object",
            "properties": {
                "n": {
                    "type": "integer",
                    "description": "Number of events to retrieve"
                }
            },
            "required": []
        }
    }
}

]

