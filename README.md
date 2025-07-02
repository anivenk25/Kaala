<p align="center">
  <img src="assets/Kaala_mascot.png" width="200" alt="Kaala Mascot"/>
</p>

<h1 align="center"> Kaala — Your Disciplined Planner Assistant</h1>

<p align="center">
  <em>Focused. Grounded. Always on time.</em>
</p>

Kaala is a minimalist, no-nonsense personal planner assistant powered by OpenAI. It integrates local text-based schedules and Google Calendar to help you stay focused, organized, and grounded — no fluff, no hallucinations.

## 🤖 What Kaala Does

- 📂 Maintains daily `.txt`-based schedule files in the `schedules/` folder.
- 📅 Syncs your schedules **to and from Google Calendar**.
- 🔁 Handles real-time calendar updates, edits, and deletions.
- ✏️ Reads, writes, and updates tasks on your local schedule files.
- 🧹 Filters out hallucinated reminders — only reflects what *you* explicitly say.
- 🔧 Exposes tools for integration with function-calling LLMs.

---

## 🛠 Available Tools

### 📁 Local Schedule Management
- `read_schedule(date)`
- `append_task(date, time, task)`
- `update_schedule(date, time, new_task)`
- `delete_schedule(date, time)`
- `mark_task_done(date, time)`
- `summarize_schedule(date)`
- `suggest_next_task(date)`

### 📆 Google Calendar Integration
- `create_calendar_event(summary, start_time_str, end_time_str)`
- `delete_calendar_event(event_id)`
- `update_calendar_event(event_id, summary, start_time_str, end_time_str)`
- `list_today_events()`
- `list_upcoming_events(n)`
- `sync_schedule_to_calendar(schedule_path)`
- `sync_schedule_folder_to_calendar(folder_path)`
- `sync_calendar_to_schedule(folder_path)`
- `delete_events_by_index(indices, n=5)`

---
### 📧 Email Integration
- `list_emails(folder, limit)`: List recent emails via IMAP.
- `send_email(to, subject, body)`: Send an email via SMTP.

### 🗺️ Maps & Travel
- `get_travel_time(origin, destination, mode)`: Estimate travel time using Google Maps.

### 🌤️ Weather
- `get_current_weather(location)`: Current weather via OpenWeatherMap.
- `get_weather_forecast(location, date)`: Weather forecast for a specific date.

### ⏰ Timezone Conversion
- `convert_timezone(time_str, from_tz, to_tz)`: Convert timestamps between time zones.

### 📅 Date-Specific Calendar & Availability
- `list_events_on_date(date_str)`: List events on a given date.
- `find_free_slots(date_str, duration)`: Find free slots of at least duration minutes.
- `schedule_task(description, duration, date_str, earliest_time, latest_time)`: Schedule a task into the next available free slot.
- `schedule_todo_tasks(date_str, default_duration)`: Auto-schedule all undone to-do items on that date.

### ✅ To-Do List Syncing
- `read_todo_list()`: Read the local to-do list.
- `append_todo_item(task)`: Add an item to your to-do.
- `mark_todo_item_done(task_text)`: Mark a to-do item done.
 - `delete_todo_item(task_text)`: Delete an item from your to-do list.
  
### 📇 Contacts & Connections
- `add_contact(name, email, phone, notes)`: Add a new contact to your contacts list.
- `list_contacts()`: List all saved contacts.
- `find_contact(query)`: Search for contacts by name, email, phone, or notes.
- `update_contact(contact_id, name, email, phone, notes)`: Update details of an existing contact.
- `delete_contact(contact_id)`: Delete a contact from your list.
- `schedule_call(contact_id, date_str, time_str, duration, notes)`: Schedule a call with a contact on Google Calendar.
- `list_scheduled_calls()`: List all your scheduled calls.
- `delete_scheduled_call(call_id)`: Delete a scheduled call by its ID.
- `auto_schedule_calls(start_date_str, end_date_str, time_str, duration, notes, timezone)`: Auto-schedule calls for contacts with defined frequency between start and end dates.
---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/kaala.git
cd kaala
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```
Note: we now include `googlemaps` for Maps integration.

### 3. Set up Google Calendar API

1. Visit [https://console.developers.google.com/](https://console.developers.google.com/)
2. Create a new project (or select an existing one).
3. Go to **APIs & Services > Library**.
4. Search for and enable the **Google Calendar API**.
5. Go to **APIs & Services > Credentials**.
6. Click **Create Credentials > OAuth client ID**.
    - Application type: **Desktop App**
    - Name: anything (e.g., "Kaala Calendar Integration")
7. Download the `client_secret.json` file.
8. Move it to a convenient location and optionally rename it (e.g., `~/client_secret.json`).
9. Set an environment variable pointing to it (see below).
10. Run Kaala once to trigger the authentication flow — a browser will open and ask you to log in.
    - The token will be saved as `token.pkl` for future use.

---

### 4. Environment Variables

Set the required environment variables in your shell config (`~/.zshrc`, `~/.bashrc`, etc.):

```bash
export OPENAI_API_KEY="your-openai-key"
export GOOGLE_CALENDAR_SECRET_PATH="$HOME/client_secret.json"
export IMAP_HOST="imap.example.com"
export IMAP_PORT=993
export SMTP_HOST="smtp.example.com"
export SMTP_PORT=587
export EMAIL_USER="you@example.com"
export EMAIL_PASS="app-specific-password"
export GOOGLE_MAPS_API_KEY="your-google-maps-key"
export OWM_API_KEY="your-openweathermap-key"
```

Then reload your shell:

```bash
source ~/.zshrc  # or ~/.bashrc
```

---

## 🧪 Usage

Run Kaala's main interface (or integrate into your agent framework):

```bash
python run.py
```

Or interact via your own OpenAI agent by calling tools listed in `openai_agent.py`.

---

## 📂 Folder Structure

```
Kaala/
├── schedules/            # Daily txt-based schedules (e.g., 2025-04-10.txt)
├── openai_agent.py       # Tool-function map + LLM logic
├── google_calendar.py    # Calendar interaction layer
├── tools.py              # JSON tool specs (for OpenAI function calling)
├── chat_history.py       # Tracks user messages and assistant replies
├── scheduler.py          # Local schedule operations
├── run.py                # Sample main interface
```

---

## 🔒 Philosophy

Kaala never invents reminders or tasks. It always reflects exactly what you've said or scheduled. It acts more like a disciplined planner than a chatty assistant.

---

## 🙌 Contributing

Pull requests are welcome. If you want to add new calendar integrations, memory systems, or schedule views, open an issue first to discuss what you have in mind.

---

## 🧘‍♂️ Built for Grounded Productivity

Created with ❤️ by [Anirudh Venkateswaran](https://github.com/anivenk25)  
Made for those who value clarity, structure, and calm control.



