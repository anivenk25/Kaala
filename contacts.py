"""
contacts.py

Module for managing contacts and scheduling calls.
"""
import os
import json
import uuid
from datetime import datetime, timedelta
import pytz
from google_calendar import get_calendar_service

# File paths for storage
CONTACTS_FILE = "contacts.json"
CALLS_FILE = "calls.json"
DEFAULT_TIMEZONE = "Asia/Kolkata"

def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "w") as f:
            json.dump([], f)
        return []
    try:
        with open(CONTACTS_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=2)

def add_contact(name, email=None, phone=None, notes=None, frequency_days=None):
    """Add a new contact. Optionally specify a call frequency in days."""
    contacts = load_contacts()
    contact_id = str(uuid.uuid4())
    contact = {
        "id": contact_id,
        "name": name,
        "email": email,
        "phone": phone,
        "notes": notes,
        "frequency_days": frequency_days,
    }
    contacts.append(contact)
    save_contacts(contacts)
    return f"✅ Added contact '{name}' with id {contact_id}."

def list_contacts():
    """List all saved contacts, including call frequency if set."""
    contacts = load_contacts()
    if not contacts:
        return "No contacts found."
    out = "Contacts:"
    for c in contacts:
        parts = [f"Name: {c.get('name')}" ]
        if c.get('email'):
            parts.append(f"Email: {c.get('email')}")
        if c.get('phone'):
            parts.append(f"Phone: {c.get('phone')}")
        if c.get('notes'):
            parts.append(f"Notes: {c.get('notes')}")
        if c.get('frequency_days'):
            parts.append(f"Call every {c.get('frequency_days')} days")
        out += f"\n- id: {c.get('id')}, " + ", ".join(parts)
    return out

def find_contact(query):
    """Search contacts by name, email, phone, or notes."""
    contacts = load_contacts()
    matches = []
    q = query.lower()
    for c in contacts:
        if (
            q in (c.get('name') or '').lower()
            or q in (c.get('email') or '').lower()
            or q in (c.get('phone') or '').lower()
            or q in (c.get('notes') or '').lower()
        ):
            matches.append(c)
    if not matches:
        return f"No contacts matching '{query}'."
    out = f"Contacts matching '{query}':"
    for c in matches:
        out += f"\n- id: {c.get('id')}, Name: {c.get('name')}"
    return out

def update_contact(contact_id, name=None, email=None, phone=None, notes=None, frequency_days=None):
    """Update an existing contact's details, including call frequency."""
    contacts = load_contacts()
    for c in contacts:
        if c.get('id') == contact_id:
            if name:
                c['name'] = name
            if email is not None:
                c['email'] = email
            if phone is not None:
                c['phone'] = phone
            if notes is not None:
                c['notes'] = notes
            if frequency_days is not None:
                c['frequency_days'] = frequency_days
            save_contacts(contacts)
            return f"✅ Updated contact '{contact_id}'."
    return f"Contact with id {contact_id} not found."

def delete_contact(contact_id):
    """Delete a contact."""
    contacts = load_contacts()
    new_contacts = [c for c in contacts if c.get('id') != contact_id]
    if len(new_contacts) == len(contacts):
        return f"Contact with id {contact_id} not found."
    save_contacts(new_contacts)
    return f"🗑️ Deleted contact with id {contact_id}."

def load_calls():
    if not os.path.exists(CALLS_FILE):
        with open(CALLS_FILE, "w") as f:
            json.dump([], f)
        return []
    try:
        with open(CALLS_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_calls(calls):
    with open(CALLS_FILE, "w") as f:
        json.dump(calls, f, indent=2)

def schedule_call(contact_id, date_str, time_str, duration, notes=None, timezone=DEFAULT_TIMEZONE):
    """Schedule a call with a contact on Google Calendar."""
    contacts = load_contacts()
    contact = next((c for c in contacts if c.get('id') == contact_id), None)
    if not contact:
        return f"Contact with id {contact_id} not found."
    name = contact.get('name')
    try:
        start_naive = datetime.fromisoformat(f"{date_str}T{time_str}")
    except ValueError:
        return f"Invalid date or time format."
    tz = pytz.timezone(timezone)
    start = tz.localize(start_naive)
    end = start + timedelta(minutes=duration)
    summary = f"Call with {name}"
    description = notes or ""
    event_body = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start.isoformat(), "timeZone": timezone},
        "end": {"dateTime": end.isoformat(), "timeZone": timezone},
    }
    service = get_calendar_service()
    try:
        created = service.events().insert(calendarId="primary", body=event_body).execute()
        event_id = created.get("id")
        link = created.get("htmlLink")
        call_id = str(uuid.uuid4())
        calls = load_calls()
        calls.append({
            "call_id": call_id,
            "contact_id": contact_id,
            "start": start.isoformat(),
            "duration": duration,
            "event_id": event_id,
            "notes": notes,
        })
        save_calls(calls)
        return f"✅ Scheduled call with '{name}' on {date_str} at {time_str}. Event link: {link}. Call id: {call_id}"
    except Exception as e:
        return f"❌ Failed to schedule call: {e}"

def list_scheduled_calls():
    """List all scheduled calls."""
    calls = load_calls()
    contacts = {c.get('id'): c for c in load_contacts()}
    if not calls:
        return "No scheduled calls."
    out = "Scheduled calls:"
    # Sort by start time
    try:
        sorted_calls = sorted(calls, key=lambda x: x.get('start'))
    except Exception:
        sorted_calls = calls
    for c in sorted_calls:
        contact = contacts.get(c.get('contact_id'), {})
        name = contact.get('name', 'Unknown')
        out += f"\n- Call id: {c.get('call_id')}, with: {name}, start: {c.get('start')}, duration: {c.get('duration')} mins"
    return out

def delete_scheduled_call(call_id):
    """Delete a scheduled call by its ID."""
    calls = load_calls()
    call = next((c for c in calls if c.get('call_id') == call_id), None)
    if not call:
        return f"Call with id {call_id} not found."
    event_id = call.get('event_id')
    service = get_calendar_service()
    try:
        if event_id:
            service.events().delete(calendarId='primary', eventId=event_id).execute()
    except Exception:
        pass
    new_calls = [c for c in calls if c.get('call_id') != call_id]
    save_calls(new_calls)
    return f"🗑️ Deleted scheduled call with id {call_id}."

def auto_schedule_calls(start_date_str, end_date_str, time_str, duration, notes=None, timezone=DEFAULT_TIMEZONE):
    """
    Auto-schedule calls for contacts with defined frequency_days between start and end dates (inclusive).
    start_date_str, end_date_str: YYYY-MM-DD; time_str: HH:MM; duration in minutes; optional notes and timezone.
    """
    try:
        start_naive = datetime.fromisoformat(f"{start_date_str}T{time_str}")
        end_naive = datetime.fromisoformat(f"{end_date_str}T{time_str}")
    except ValueError:
        return "❌ Invalid date or time format."
    tz = pytz.timezone(timezone)
    start_dt = tz.localize(start_naive)
    end_dt = tz.localize(end_naive)
    contacts_list = load_contacts()
    calls_list = load_calls()
    results = []
    for contact in contacts_list:
        freq = contact.get('frequency_days')
        if not isinstance(freq, int) or freq <= 0:
            continue
        contact_id = contact.get('id')
        # Determine last scheduled call for this contact
        contact_calls = [c for c in calls_list if c.get('contact_id') == contact_id]
        if contact_calls:
            last_call = max(contact_calls, key=lambda c: c.get('start'))
            try:
                last_dt = datetime.fromisoformat(last_call.get('start'))
            except Exception:
                continue
            if last_dt.tzinfo is None:
                last_dt = tz.localize(last_dt)
        else:
            # No previous calls: schedule first call at start_dt
            last_dt = start_dt - timedelta(days=freq)
        # Schedule calls at intervals
        next_dt = last_dt + timedelta(days=freq)
        while next_dt <= end_dt:
            date_str = next_dt.strftime("%Y-%m-%d")
            time_str_fmt = next_dt.strftime("%H:%M")
            res = schedule_call(contact_id, date_str, time_str_fmt, duration, notes, timezone)
            results.append(res)
            # Refresh calls list after scheduling
            calls_list = load_calls()
            # Next
            next_dt = next_dt + timedelta(days=freq)
    if not results:
        return "No calls scheduled. Ensure contacts have 'frequency_days' set to a positive integer and dates are valid."
    return "\n".join(results)