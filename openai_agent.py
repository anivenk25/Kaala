import os
import openai
import json
from datetime import datetime
from scheduler import (
    read_schedule, append_task, update_schedule, delete_schedule,
    mark_task_done, summarize_schedule, suggest_next_task
)
from google_calendar import (
    create_calendar_event,
    list_today_events,
    delete_calendar_event,
    update_calendar_event,
    list_upcoming_events,
    delete_all_events_on_date,
    create_all_day_event,
    delete_all_upcoming_events,
    find_events_by_keyword,
    export_calendar_to_json
)

from search_net import search_internet
from integrations import (
    list_emails, send_email,
    get_travel_time,
    get_current_weather, get_weather_forecast,
    convert_timezone,
    list_events_on_date, find_free_slots,
    read_todo_list, append_todo_item,
    mark_todo_item_done, delete_todo_item,
    schedule_task, schedule_todo_tasks
)
from contacts import add_contact, list_contacts, update_contact, delete_contact, find_contact, schedule_call, list_scheduled_calls, delete_scheduled_call, auto_schedule_calls
from tools import tools
from chat_history import load_recent_history, save_to_history
import pytz

# Set OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function dispatch map
function_map = {
    "create_calendar_event": create_calendar_event,
    "list_today_events": list_today_events,
    "delete_calendar_event": delete_calendar_event,
    "update_calendar_event": update_calendar_event,
    "list_upcoming_events": list_upcoming_events,
    "delete_all_events_on_date": delete_all_events_on_date,
    "create_all_day_event": create_all_day_event,
    "delete_all_upcoming_events": delete_all_upcoming_events,
    "find_events_by_keyword": find_events_by_keyword,
    "export_calendar_to_json": export_calendar_to_json,
    "search_internet": search_internet,
    # Email
    "list_emails": list_emails,
    "send_email": send_email,
    # Maps & Travel
    "get_travel_time": get_travel_time,
    # Weather
    "get_current_weather": get_current_weather,
    "get_weather_forecast": get_weather_forecast,
    # Timezone
    "convert_timezone": convert_timezone,
    # Calendar date-specific
    "list_events_on_date": list_events_on_date,
    "find_free_slots": find_free_slots,
    # To-do list
    "read_todo_list": read_todo_list,
    "append_todo_item": append_todo_item,
    "mark_todo_item_done": mark_todo_item_done,
    "delete_todo_item": delete_todo_item,
    # Advanced scheduling
    "schedule_task": schedule_task,
    "schedule_todo_tasks": schedule_todo_tasks,
    "add_contact": add_contact,
    "list_contacts": list_contacts,
    "find_contact": find_contact,
    "update_contact": update_contact,
    "delete_contact": delete_contact,
    "schedule_call": schedule_call,
    "list_scheduled_calls": list_scheduled_calls,
    "delete_scheduled_call": delete_scheduled_call,
    "auto_schedule_calls": auto_schedule_calls
}

# Set India timezone and format today's date
india_tz = pytz.timezone("Asia/Kolkata")
now = datetime.now(india_tz)
today_str = now.strftime("%Y-%m-%d")
today_readable = now.strftime("%A, %B %d, %Y")

# System prompt
SYSTEM_PROMPT = f"""
You are Kaala, a disciplined, helpful, and reliable personal assistant that manages Anirudh's daily schedule and calendar.

🧠 Always prefix the user's message with "🧠 User said:"
🤖 Always prefix your reply with "🤖 Kaala replies:"

📅 DO NOT invent or assume tasks, reminders, or events unless they are directly provided by the user.
📝 Never summarize or modify tasks unless the user asks you to.
🧭 Assume the user is located in India and operates in IST (Asia/Kolkata) timezone.
📂 The user stores schedules as `.txt` files in the `schedules/` folder, formatted as: `HH:MM - Task Description`.
🔁 If syncing is requested, only sync based on existing data — never generate your own events.
📎 When showing tasks or events, preserve their original wording and order.
   
Today is {today_readable}.
"""


def call_openai_with_tools(user_input: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.strip()},
        *load_recent_history(),
        {"role": "user", "content": user_input}
    ]

    # Save user's message
    save_to_history("user", user_input)

    # First OpenAI call
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_messages = []

    if response_message.tool_calls:
        # Execute each tool call
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"\n🛠 Calling tool: {function_name} with arguments {arguments}")

            if function_name in function_map:
                result = function_map[function_name](**arguments)

                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(result),
                })

        # Follow-up after tool call(s)
        messages.append(response_message.model_dump())
        messages.extend(tool_messages)

        followup = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages
        )

        assistant_reply = followup.choices[0].message.content

    else:
        # No tool calls needed, use direct response
        assistant_reply = response_message.content

    # Save assistant's reply
    save_to_history("assistant", assistant_reply.strip())

    return assistant_reply

