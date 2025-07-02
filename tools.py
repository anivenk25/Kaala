#tools.py 

from typing import List

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_internet",
            "description": "Search the internet for the latest information about a topic or query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find information online."
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of top search results to retrieve.",
                        "default": 5
                    }
                },
                "required": ["query"]
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
                    "description": {"type": "string", "description": "Optional description for the event"}
                },
                "required": ["summary", "start_time_str", "end_time_str"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_today_events",
            "description": "Lists today's Google Calendar events.",
            "parameters": {
                "type": "object",
                "properties": {}
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
                    },
                    "description": {
                        "type": "string",
                        "description": "Updated description for the event"
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
                    "description": {"type": "string", "description": "Optional description for the event"}
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
    },
    {
        "type": "function",
        "function": {
            "name": "list_emails",
            "description": "List recent emails from your mailbox via IMAP.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder": {"type": "string", "description": "Mailbox folder name", "default": "INBOX"},
                    "limit": {"type": "integer", "description": "Number of emails to list", "default": 5}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email via SMTP.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body content"}
                },
                "required": ["to", "subject", "body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_travel_time",
            "description": "Get travel time estimate between two locations using Google Maps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "Starting location"},
                    "destination": {"type": "string", "description": "Destination location"},
                    "mode": {"type": "string", "description": "Travel mode (driving, walking, bicycling, transit)", "default": "driving"}
                },
                "required": ["origin", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather for a location using OpenWeatherMap.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "Location name (city, region)"}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "Get weather forecast for a location and date using OpenWeatherMap.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "Location name (city, region)"},
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD or ISO format"}
                },
                "required": ["location", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_timezone",
            "description": "Convert a timestamp between time zones.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_str": {"type": "string", "description": "ISO 8601 timestamp"},
                    "from_tz": {"type": "string", "description": "Source timezone (e.g., Asia/Kolkata)"},
                    "to_tz": {"type": "string", "description": "Target timezone (e.g., UTC)"}
                },
                "required": ["time_str", "from_tz", "to_tz"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_events_on_date",
            "description": "List Google Calendar events for a specific date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_str": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                },
                "required": ["date_str"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_free_slots",
            "description": "Find free time slots on a date from your Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_str": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "duration": {"type": "integer", "description": "Minimum slot duration in minutes"}
                },
                "required": ["date_str", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_todo_list",
            "description": "Read the local to-do list.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "append_todo_item",
            "description": "Add an item to the to-do list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "Task description to add"}
                },
                "required": ["task"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_todo_item_done",
            "description": "Mark a to-do item as done.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_text": {"type": "string", "description": "Text of the task to mark done"}
                },
                "required": ["task_text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_todo_item",
            "description": "Delete a to-do item from the list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_text": {"type": "string", "description": "Text of the task to delete"}
                },
                "required": ["task_text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_task",
            "description": "Schedule a task into the next available free slot on your Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Event summary to schedule"},
                    "duration": {"type": "integer", "description": "Duration in minutes"},
                    "date_str": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "earliest_time": {"type": "string", "description": "Earliest HH:MM to start, default 00:00"},
                    "latest_time": {"type": "string", "description": "Latest HH:MM to end, default 23:59"}
                },
                "required": ["description", "duration", "date_str"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_todo_tasks",
            "description": "Auto-schedule all undone to-do list items into free slots on a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_str": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "default_duration": {"type": "integer", "description": "Default duration per task in minutes", "default": 60}
                },
                "required": ["date_str"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_contact",
            "description": "Add a new contact to your contacts list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Contact's name"},
                    "email": {"type": "string", "description": "Contact's email address"},
                    "phone": {"type": "string", "description": "Contact's phone number"},
                    "notes": {"type": "string", "description": "Optional notes about the contact"},
                    "frequency_days": {"type": "integer", "description": "Call frequency in days"}
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_contacts",
            "description": "List all saved contacts.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_contact",
            "description": "Search for contacts by name, email, phone, or notes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_contact",
            "description": "Update an existing contact's details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string", "description": "ID of the contact to update"},
                    "name": {"type": "string", "description": "New name"},
                    "email": {"type": "string", "description": "New email address"},
                    "phone": {"type": "string", "description": "New phone number"},
                    "notes": {"type": "string", "description": "Updated notes"},
                    "frequency_days": {"type": "integer", "description": "Updated call frequency in days"}
                },
                "required": ["contact_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_contact",
            "description": "Delete a contact from your list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string", "description": "ID of the contact to delete"}
                },
                "required": ["contact_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_call",
            "description": "Schedule a call with a contact on your Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string", "description": "ID of the contact to call"},
                    "date_str": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "time_str": {"type": "string", "description": "Time in HH:MM format"},
                    "duration": {"type": "integer", "description": "Duration of the call in minutes"},
                    "notes": {"type": "string", "description": "Optional notes or agenda for the call"}
                },
                "required": ["contact_id", "date_str", "time_str", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_scheduled_calls",
            "description": "List all scheduled calls with contacts.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_scheduled_call",
            "description": "Delete a scheduled call by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "call_id": {"type": "string", "description": "ID of the call to delete"}
                },
                "required": ["call_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "auto_schedule_calls",
            "description": "Auto-schedule calls for contacts with defined frequency between start and end dates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date_str": {"type": "string", "description": "Start date in YYYY-MM-DD format"},
                    "end_date_str": {"type": "string", "description": "End date in YYYY-MM-DD format"},
                    "time_str": {"type": "string", "description": "Time in HH:MM format for each call"},
                    "duration": {"type": "integer", "description": "Duration of each call in minutes"},
                    "notes": {"type": "string", "description": "Optional notes or agenda for calls"},
                    "timezone": {"type": "string", "description": "Timezone for scheduling", "default": "Asia/Kolkata"}
                },
                "required": ["start_date_str", "end_date_str", "time_str", "duration"]
            }
        }
    }
]

