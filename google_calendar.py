# google_calendar.py

import os
import datetime
import pytz
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
from datetime import datetime, timedelta

CLIENT_SECRET_FILE = os.getenv("GOOGLE_CALENDAR_SECRET_PATH")
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None
    if os.path.exists("token.pkl"):
        with open("token.pkl", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pkl", "wb") as token:
            pickle.dump(creds, token)
    return build("calendar", "v3", credentials=creds)

def create_calendar_event(summary, start_time_str, end_time_str, timezone="Asia/Kolkata"):
    service = get_calendar_service()

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_time_str,
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_time_str,
            "timeZone": timezone,
        },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    return f"✅ Event created: {event.get('htmlLink')}"

def list_today_events(timezone="Asia/Kolkata"):
    service = get_calendar_service()
    now = datetime.now(pytz.timezone(timezone))
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])

    if not events:
        return "📭 No events found for today."

    out = "📅 Today's Google Calendar events:\n"
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        out += f"- {event['summary']} at {start}\n"
    return out


def sync_schedule_folder_to_calendar(folder_path="schedules"):
    service = get_calendar_service()
    timezone = "Asia/Kolkata"
    created_events = []

    for filename in os.listdir(folder_path):
        if not filename.endswith(".txt"):
            continue

        date_str = filename.replace(".txt", "")
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            if not line.strip():
                continue
            try:
                time_part, task = line.strip().split(" - ", 1)
                start_dt = datetime.strptime(f"{date_str} {time_part}", "%Y-%m-%d %H:%M")
                end_dt = start_dt + timedelta(minutes=60)

                event = {
                    "summary": task.strip(),
                    "start": {"dateTime": start_dt.isoformat(), "timeZone": timezone},
                    "end": {"dateTime": end_dt.isoformat(), "timeZone": timezone},
                }
                service.events().insert(calendarId="primary", body=event).execute()
                created_events.append(task.strip())
            except ValueError:
                continue

    return f"📤 Synced {len(created_events)} events from {folder_path} to Google Calendar."


def sync_calendar_to_schedule(folder_path="schedules"):
    service = get_calendar_service()
    timezone = "Asia/Kolkata"
    now = datetime.now(pytz.timezone(timezone))
    future = now + timedelta(days=7)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=future.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    written = 0

    for event in events:
        start = event["start"].get("dateTime")
        if not start:
            continue

        start_dt = datetime.fromisoformat(start)
        date_str = start_dt.strftime("%Y-%m-%d")
        time_str = start_dt.strftime("%H:%M")
        summary = event.get("summary", "Untitled")

        filepath = os.path.join(folder_path, f"{date_str}.txt")

        entry = f"{time_str} - {summary}\n"

        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                if entry in f.read():
                    continue

        with open(filepath, "a") as f:
            f.write(entry)
            written += 1

    return f"📥 Synced {written} events from Google Calendar into {folder_path} folder."


def delete_calendar_event(event_id):
    service = get_calendar_service()
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return f"🗑️ Deleted event with ID: {event_id}"
    except Exception as e:
        return f"❌ Failed to delete event: {str(e)}"

def update_calendar_event(event_id, summary=None, start_time_str=None, end_time_str=None, timezone="Asia/Kolkata"):
    service = get_calendar_service()
    try:
        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        if summary:
            event["summary"] = summary
        if start_time_str:
            event["start"]["dateTime"] = start_time_str
            event["start"]["timeZone"] = timezone
        if end_time_str:
            event["end"]["dateTime"] = end_time_str
            event["end"]["timeZone"] = timezone

        updated_event = service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
        return f"✏️ Event updated: {updated_event.get('htmlLink')}"
    except Exception as e:
        return f"❌ Failed to update event: {str(e)}"

def list_upcoming_events(n=5, timezone="Asia/Kolkata"):
    service = get_calendar_service()
    now = datetime.now(pytz.timezone(timezone)).isoformat()
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=n,
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])

    if not events:
        return "📭 No upcoming events found."

    out = f"📆 Your next {n} event(s):\n"
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        out += f"- {event['summary']} at {start} (ID: {event['id']})\n"
    return out

def delete_all_events_on_date(date_str, timezone="Asia/Kolkata"):
    service = get_calendar_service()
    start = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=pytz.timezone(timezone))
    end = start + timedelta(days=1)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    deleted = 0
    for event in events_result.get("items", []):
        service.events().delete(calendarId='primary', eventId=event['id']).execute()
        deleted += 1

    return f"🗑️ Deleted {deleted} event(s) on {date_str}"


def create_all_day_event(summary, date_str, timezone="Asia/Kolkata"):
    service = get_calendar_service()
    event = {
        "summary": summary,
        "start": {"date": date_str, "timeZone": timezone},
        "end": {"date": (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"), "timeZone": timezone},
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    return f"🗓️ All-day event created: {event.get('htmlLink')}"


def delete_all_upcoming_events(days=30, timezone="Asia/Kolkata"):
    service = get_calendar_service()
    now = datetime.now(pytz.timezone(timezone))
    future = now + timedelta(days=days)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=future.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    deleted = 0
    for event in events_result.get("items", []):
        service.events().delete(calendarId="primary", eventId=event["id"]).execute()
        deleted += 1

    return f"🚫 Cleared {deleted} upcoming event(s) from your calendar."


def find_events_by_keyword(keyword, timezone="Asia/Kolkata"):
    service = get_calendar_service()
    now = datetime.now(pytz.timezone(timezone))
    future = now + timedelta(days=30)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=future.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    matches = []
    for event in events_result.get("items", []):
        if keyword.lower() in event.get("summary", "").lower():
            matches.append(event)

    if not matches:
        return f"🔍 No events found with keyword '{keyword}'"

    out = f"🔍 Events containing '{keyword}':\n"
    for event in matches:
        start = event["start"].get("dateTime", event["start"].get("date"))
        out += f"- {event['summary']} at {start} (ID: {event['id']})\n"
    return out


def export_calendar_to_json(filepath="calendar_dump.json", timezone="Asia/Kolkata"):
    service = get_calendar_service()
    now = datetime.now(pytz.timezone(timezone))
    future = now + timedelta(days=90)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=future.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    with open(filepath, "w") as f:
        json.dump(events_result.get("items", []), f, indent=2)

    return f"📄 Exported {len(events_result.get('items', []))} events to {filepath}"

