# google_calendar.py

import os
import datetime
import pytz
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
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
    now = datetime.datetime.now(pytz.timezone(timezone))
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

