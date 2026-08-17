# To-Do API

A tiny FastAPI backend for the to-do list, backed by SQLite (see `todo.db`, created automatically on first run — not committed).

## Run it

```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open `http://127.0.0.1:8000/docs` — FastAPI's auto-generated docs page. You can add, list, update, and delete tasks straight from there.

## Routes

| Method | Path | Does |
|---|---|---|
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Add a task — body: `{"text": "..."}` |
| PUT | `/tasks/{task_id}` | Update a task — body: `{"text": "...", "done": true}` (both optional) |
| DELETE | `/tasks/{task_id}` | Delete a task |

Data lives in a SQLite file ([todo.db](todo.db), created next to `main.py` on first run) — it survives server restarts. The frontend in the parent folder ([../script.js](../script.js)) talks to this API directly via `fetch`, so run this server (port 8000) before opening the frontend. CORS is wide open (`allow_origins=["*"]`) since this is a local dev setup, not something to ship as-is.
