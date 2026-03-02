import os
import json
from datetime import datetime
from dotenv import load_dotenv
from sap_ai_sdk_gen.proxy.native.openai import OpenAI
import pytz

# Load environment variables
load_dotenv()

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
    schedule_task
)
from contacts import (
    add_contact, list_contacts, update_contact, delete_contact, 
    find_contact, schedule_call, list_scheduled_calls, 
    delete_scheduled_call, auto_schedule_calls
)
from tools import tools
from chat_history import load_recent_history, save_message

# SAP AI Core / GenAI Hub Configuration
# These should be set in .env based on the SAP BTP service key
AICORE_CLIENT_ID = os.getenv("AICORE_CLIENT_ID")
AICORE_CLIENT_SECRET = os.getenv("AICORE_CLIENT_SECRET")
AICORE_AUTH_URL = os.getenv("AICORE_AUTH_URL")
AICORE_BASE_URL = os.getenv("AICORE_BASE_URL")
AICORE_RESOURCE_GROUP = os.getenv("AICORE_RESOURCE_GROUP", "default")
# deployment_id from GenAI Hub
LLM_DEPLOYMENT_ID = os.getenv("LLM_DEPLOYMENT_ID")

# Initialize SAP AI Core Client
client = OpenAI(
    deployment_id=LLM_DEPLOYMENT_ID
)

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
    "list_emails": list_emails,
    "send_email": send_email,
    "get_travel_time": get_travel_time,
    "get_current_weather": get_current_weather,
    "get_weather_forecast": get_weather_forecast,
    "convert_timezone": convert_timezone,
    "list_events_on_date": list_events_on_date,
    "find_free_slots": find_free_slots,
    "schedule_task": schedule_task,
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
today_readable = now.strftime("%A, %B %d, %Y")

# System prompt
SYSTEM_PROMPT = f"""
You are Joule, SAP's AI copilot, a disciplined and reliable personal assistant managed via the SAP Business Agent Foundation.
Your core mission is to help Anirudh manage his calendar and schedule with high precision.

🧠 **Persona**: Joule is grounded, minimalist, and strictly data-driven. 
🧠 Always prefix the user's message with "🧠 User said:"
🤖 Always prefix your reply with "🤖 Joule replies:"

🤖 **Groundedness**: You have NO MEMORY of Anirudh's calendar events. You MUST use the provided tools to fetch any schedule or calendar information. 
🚫 **Strict Rule**: NEVER invent, assume, or hallucinate tasks, reminders, or events. If you haven't called a tool to fetch data, you DO NOT know the schedule. 
🦾 **Tool-First**: Always call a tool first when asked about the agenda, calendar, or free time.
🦾 **Reliability**: When asked to "do that" or "add this," use `create_calendar_event` or `schedule_task`.

🧭 Assume the user is located in India and operates in IST (Asia/Kolkata) timezone.
🔁 When scheduling, use `schedule_task` to find available slots automatically (09:00-18:00 default).
   
Today is {today_readable}.
"""

def call_agent(user_input: str, stream_callback=None):
    history = load_recent_history()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.strip()},
        *history
    ]
    
    user_message = {"role": "user", "content": user_input}
    messages.append(user_message)
    save_message(user_message)

    assistant_reply = ""
    
    while True:
        # Turn to check for tools
        response = client.chat.completions.create(
            model="gpt-4", # Model name is often ignored by GenAI Hub in favor of deployment_id
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0
        )

        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            # We must convert the response message to a dict for persistence and turn-handling
            messages.append(response_message.model_dump())
            save_message(response_message.model_dump())
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                
                try:
                    arguments = json.loads(tool_call.function.arguments)
                except Exception:
                    arguments = {}

                if stream_callback:
                    stream_callback(f"\n🛠 calling tool: [bold cyan]{function_name}[/bold cyan]...")
                
                if function_name in function_map:
                    try:
                        result = function_map[function_name](**arguments)
                    except Exception as e:
                        result = f"Error executing tool: {str(e)}"

                    tool_response_message = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(result),
                    }
                    messages.append(tool_response_message)
                    save_message(tool_response_message)
            
            # Continue loop to let model process tool results
            continue

        else:
            # Final text response
            assistant_reply = response_message.content
            if stream_callback and assistant_reply:
                stream_callback(assistant_reply)
            
            save_message({"role": "assistant", "content": assistant_reply.strip()})
            break

    return assistant_reply
