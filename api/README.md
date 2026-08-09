# To-Do API

A tiny FastAPI backend for the to-do list, storing tasks in a plain Python list (no database yet).

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

Data lives in memory (a plain Python list in [main.py](main.py)) — it resets whenever the server restarts. The frontend in the parent folder does **not** talk to this API yet; the two are separate exercises for now.
