import os
import imaplib
import smtplib
from email.message import EmailMessage
from email import message_from_bytes
import googlemaps
import requests
import json
from datetime import datetime, timedelta
import pytz
from google_calendar import get_calendar_service

# Email (IMAP) integration
def list_emails(folder: str = "INBOX", limit: int = 5) -> str:
    host = os.getenv("IMAP_HOST")
    port = int(os.getenv("IMAP_PORT", 993))
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    if not all([host, user, password]):
        return "IMAP credentials not set."
    try:
        mail = imaplib.IMAP4_SSL(host, port)
        mail.login(user, password)
        mail.select(folder)
        status, data = mail.search(None, "ALL")
        email_ids = data[0].split()
        email_ids = email_ids[-limit:] if len(email_ids) >= limit else email_ids
        emails = []
        for eid in reversed(email_ids):
            status, msg_data = mail.fetch(eid, "(RFC822.HEADER)")
            raw = msg_data[0][1]
            msg = message_from_bytes(raw)
            subj = msg.get("Subject")
            frm = msg.get("From")
            date = msg.get("Date")
            emails.append(f"From: {frm}, Subject: {subj}, Date: {date}")
        return "\n".join(emails) if emails else "No emails found."
    except Exception as e:
        return f"Failed to list emails: {e}"

# Email (SMTP) integration
def send_email(to: str, subject: str, body: str) -> str:
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", 587))
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    if not all([host, user, password]):
        return "SMTP credentials not set."
    try:
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            msg = EmailMessage()
            msg["From"] = user
            msg["To"] = to
            msg["Subject"] = subject
            msg.set_content(body)
            server.send_message(msg)
        return f"Email sent to {to}."
    except Exception as e:
        return f"Failed to send email: {e}"

# Google Maps travel-time estimates
def get_travel_time(origin: str, destination: str, mode: str = "driving") -> str:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return "Google Maps API key not set."
    try:
        gmaps = googlemaps.Client(key=api_key)
        matrix = gmaps.distance_matrix(origins=[origin], destinations=[destination], mode=mode)
        elem = matrix["rows"][0]["elements"][0]
        if elem.get("status") != "OK":
            return f"Could not compute travel time: {elem.get('status')}"
        duration = elem["duration"]["text"]
        return f"Travel time from {origin} to {destination} by {mode}: {duration}"
    except Exception as e:
        return f"Failed to get travel time: {e}"

# OpenWeatherMap integration
def get_current_weather(location: str) -> str:
    api_key = os.getenv("OWM_API_KEY")
    if not api_key:
        return "OpenWeatherMap API key not set."
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        resp = requests.get(url)
        data = resp.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Current weather in {location}: {temp}°C, {desc}."
    except Exception as e:
        return f"Failed to get weather: {e}"

def get_weather_forecast(location: str, date: str) -> str:
    api_key = os.getenv("OWM_API_KEY")
    if not api_key:
        return "OpenWeatherMap API key not set."
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
        resp = requests.get(url)
        data = resp.json()
        target = datetime.fromisoformat(date)
        forecasts = data.get("list", [])
        best = None
        for item in forecasts:
            dt = datetime.fromtimestamp(item["dt"])
            if dt.date() == target.date():
                best = item
                break
        if not best:
            return f"No forecast found for {date} in {location}."
        temp = best["main"]["temp"]
        desc = best["weather"][0]["description"]
        time_str = datetime.fromtimestamp(best["dt"]).strftime("%Y-%m-%d %H:%M")
        return f"Forecast for {location} on {date} at {time_str}: {temp}°C, {desc}."
    except Exception as e:
        return f"Failed to get weather forecast: {e}"

# Timezone conversion
def convert_timezone(time_str: str, from_tz: str, to_tz: str) -> str:
    try:
        naive = datetime.fromisoformat(time_str)
        src = pytz.timezone(from_tz)
        dst = pytz.timezone(to_tz)
        localized = src.localize(naive)
        converted = localized.astimezone(dst)
        return converted.isoformat()
    except Exception as e:
        return f"Failed to convert timezone: {e}"

# Google Calendar date-specific events
def list_events_on_date(date_str: str, timezone: str = "Asia/Kolkata") -> str:
    service = get_calendar_service()
    tz = pytz.timezone(timezone)
    start = tz.localize(datetime.strptime(date_str, "%Y-%m-%d"))
    end = start + timedelta(days=1)
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])
    if not events:
        return f"No events on {date_str}."
    out = f"Events on {date_str}:"
    for event in events:
        start_time = event["start"].get("dateTime", event["start"].get("date"))
        out += f"\n- {event.get('summary','')} at {start_time} (ID: {event.get('id')})"
    return out

# Find free slots based on calendar events
def find_free_slots(date_str: str, duration: int, timezone: str = "Asia/Kolkata") -> str:
    service = get_calendar_service()
    tz = pytz.timezone(timezone)
    start = tz.localize(datetime.strptime(date_str, "%Y-%m-%d"))
    end = start + timedelta(days=1)
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])
    slots = []
    current = start
    for event in events:
        ev_start = datetime.fromisoformat(event["start"].get("dateTime", event["start"].get("date")))
        ev_end = datetime.fromisoformat(event["end"].get("dateTime", event["end"].get("date")))
        if ev_start - current >= timedelta(minutes=duration):
            slots.append((current, ev_start))
        current = max(current, ev_end)
    if end - current >= timedelta(minutes=duration):
        slots.append((current, end))
    if not slots:
        return f"No free slots of at least {duration} minutes on {date_str}."
    out = f"Free slots on {date_str} for {duration} minutes:"
    for s, e in slots:
        out += f"\n- {s.strftime('%H:%M')} to {e.strftime('%H:%M')}"
    return out

# Local to-do list syncing
todo_file = "todo_list.txt"

def read_todo_list() -> str:
    if not os.path.exists(todo_file):
        open(todo_file, "w").close()
    with open(todo_file) as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines:
        return "No tasks in to-do list."
    out = "To-do list:"
    for idx, line in enumerate(lines, 1):
        out += f"\n{idx}. {line}"
    return out

def append_todo_item(task: str) -> str:
    if not os.path.exists(todo_file):
        open(todo_file, "w").close()
    with open(todo_file, "a") as f:
        f.write(f"[ ] {task}\n")
    return f"Added to to-do list: {task}"

def mark_todo_item_done(task_text: str) -> str:
    if not os.path.exists(todo_file):
        return "To-do list not found."
    with open(todo_file) as f:
        lines = f.readlines()
    new_lines = []
    found = False
    for l in lines:
        if task_text in l and "[ ]" in l:
            new_lines.append(l.replace("[ ]", "[x]"))
            found = True
        else:
            new_lines.append(l)
    with open(todo_file, "w") as f:
        f.writelines(new_lines)
    return "Marked task as done." if found else "Task not found."

def delete_todo_item(task_text: str) -> str:
    if not os.path.exists(todo_file):
        return "To-do list not found."
    with open(todo_file) as f:
        lines = f.readlines()
    new_lines = [l for l in lines if task_text not in l]
    deleted = len(lines) - len(new_lines)
    with open(todo_file, "w") as f:
        f.writelines(new_lines)
    return f"Deleted {deleted} matching task(s)." if deleted else "Task not found."

def schedule_task(description: str, duration: int, date_str: str,
                  earliest_time: str = None, latest_time: str = None,
                  timezone: str = "Asia/Kolkata") -> str:
    """
    Schedule a task into the next available free slot on a given date.
    - description: event summary
    - duration: minutes needed
    - date_str: YYYY-MM-DD
    - earliest_time: HH:MM (default: 00:00)
    - latest_time: HH:MM (default: 23:59)
    """
    service = get_calendar_service()
    tz = pytz.timezone(timezone)
    # Build day start/end boundaries
    if earliest_time:
        start_dt = datetime.fromisoformat(f"{date_str}T{earliest_time}")
    else:
        start_dt = datetime.fromisoformat(f"{date_str}T00:00")
    if latest_time:
        end_dt = datetime.fromisoformat(f"{date_str}T{latest_time}")
    else:
        end_dt = datetime.fromisoformat(f"{date_str}T23:59")
    start = tz.localize(start_dt)
    end = tz.localize(end_dt)
    # Fetch existing events
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])
    # Find free slot
    cursor = start
    for ev in events:
        ev_start_str = ev["start"].get("dateTime")
        ev_end_str = ev["end"].get("dateTime")
        if not ev_start_str or not ev_end_str:
            continue
        ev_start = datetime.fromisoformat(ev_start_str)
        ev_end = datetime.fromisoformat(ev_end_str)
        # Check for gap before this event
        if (ev_start - cursor).total_seconds() >= duration * 60:
            slot_start = cursor
            break
        # Move cursor forward
        cursor = max(cursor, ev_end)
    else:
        # After all events, check final gap
        if (end - cursor).total_seconds() >= duration * 60:
            slot_start = cursor
        else:
            return f"No available slot of {duration} minutes on {date_str}."
    slot_end = slot_start + timedelta(minutes=duration)
    # Create event
    event_body = {
        "summary": description,
        "start": {"dateTime": slot_start.isoformat(), "timeZone": timezone},
        "end": {"dateTime": slot_end.isoformat(), "timeZone": timezone},
    }
    try:
        created = service.events().insert(calendarId="primary", body=event_body).execute()
        link = created.get("htmlLink")
        return f"✅ Scheduled '{description}' on {date_str} at {slot_start.strftime('%H:%M')}. Link: {link}"
    except Exception as e:
        return f"Failed to schedule task: {e}"

def schedule_todo_tasks(date_str: str, default_duration: int = 60,
                        timezone: str = "Asia/Kolkata") -> str:
    """
    Auto-schedule all undone to-do list items into free slots on a given date.
    """
    # Load undone tasks
    if not os.path.exists(todo_file):
        return "To-do list not found."
    with open(todo_file) as f:
        lines = [l.strip() for l in f if l.startswith("[ ]")]
    if not lines:
        return "No undone tasks to schedule."
    results = []
    for line in lines:
        # Strip checkbox prefix
        task = line[3:].strip()
        res = schedule_task(task, default_duration, date_str,
                            timezone=timezone)
        results.append(res)
    return "\n".join(results)