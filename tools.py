from typing import List

tools = [
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
            "name": "delete_all_events_on_date",
            "description": "Delete all events on a given date from Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_str": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format"
                    }
                },
                "required": ["date_str"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_all_day_event",
            "description": "Create an all-day event on a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "date_str": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                },
                "required": ["summary", "date_str"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_all_upcoming_events",
            "description": "Delete all upcoming events within the next N days.",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "default": 30,
                        "description": "Number of days ahead to delete events"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_events_by_keyword",
            "description": "Search upcoming events by keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string"}
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "export_calendar_to_json",
            "description": "Export all upcoming events to a JSON file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "default": "calendar_dump.json",
                        "description": "Path to save the exported JSON file"
                    }
                },
                "required": []
            }
        }
    }
]

