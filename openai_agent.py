import os
import openai
import json
from datetime import datetime
from scheduler import (
    read_schedule, append_task, update_schedule, delete_schedule,
    mark_task_done, summarize_schedule, suggest_next_task
)
from tools import tools
from chat_history import load_recent_history, save_to_history
import pytz

# Set OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function dispatch map
function_map = {
    "read_schedule": read_schedule,
    "append_task": append_task,
    "update_schedule": update_schedule,
    "delete_schedule": delete_schedule,
    "mark_task_done": mark_task_done,
    "summarize_schedule": summarize_schedule,
    "suggest_next_task": suggest_next_task,
}

# Set India timezone and format today's date
india_tz = pytz.timezone("Asia/Kolkata")
now = datetime.now(india_tz)
today_str = now.strftime("%Y-%m-%d")
today_readable = now.strftime("%A, %B %d, %Y")

# System prompt
SYSTEM_PROMPT = f"""
You are Kaala, a disciplined, helpful, and grounded planner assistant.
🧠 Always prefix the user message with "🧠 User said:"
🤖 Always prefix your reply with "🤖 Kaala replies:"
📅 Never invent tasks, reminders, or events. Only reflect what the user explicitly says.
🕰 Clarify if the user’s request is ambiguous or missing a time/date.
🌍 Assume the user is in India. Today is {today_readable}.
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

