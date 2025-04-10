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
    "export_calendar_to_json": export_calendar_to_json
}

# Set India timezone and format today's date
india_tz = pytz.timezone("Asia/Kolkata")
now = datetime.now(india_tz)
today_str = now.strftime("%Y-%m-%d")
today_readable = now.strftime("%A, %B %d, %Y")

# System prompt
SYSTEM_PROMPT = f"""
You are Kaala, a disciplined, helpful, and reliable personal assistant that manages the user's daily schedule and calendar.

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

    return assistant_reply

