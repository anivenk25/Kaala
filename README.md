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

### 3. Set up Google Calendar API

- Visit https://console.developers.google.com/
- Enable the **Google Calendar API**
- Download your `client_secret.json` and place it where needed
- Run Kaala once to trigger authentication (token will be saved as `token.pkl`)

### 4. Environment Variables

Set your OpenAI key:

```bash
export OPENAI_API_KEY=your-openai-key
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



