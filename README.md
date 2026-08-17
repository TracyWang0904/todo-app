# To-Do List

A vanilla JS/HTML/CSS to-do list frontend, backed by the FastAPI + SQLite API in [api/](api/). The browser holds no data of its own — every add/edit/complete/delete goes through the API, which is the single source of truth.

## Features

- Add a task (Enter or the Add button)
- Mark a task done (checkbox, strikethrough text)
- Edit a task (click Edit, or double-click the text; Enter/blur saves, Escape cancels)
- Delete a task
- Filter: All / Active / Done

## Run it

1. Start the API first (see [api/README.md](api/README.md)) — it listens on `http://127.0.0.1:8000`.
2. Serve this folder on a **different** port, e.g.:

```bash
python3 -m http.server 4176
```

then visit `http://localhost:4176`. (Opening `index.html` directly as a `file://` URL also works.)

## Code structure

`script.js` keeps no local copy of the tasks as its source of truth — `tasks` is just a cache of whatever the API last returned. Every action calls the API first, then re-fetches and redraws:

- `loadTasks()` — `GET /tasks`, stores the result in `tasks`, calls `render()`
- `addTask(text)` — `POST /tasks`, then `loadTasks()`
- `deleteTask(id)` — `DELETE /tasks/{id}`, then `loadTasks()`
- `toggleTask(id)` — `PUT /tasks/{id}` with the flipped `done`, then `loadTasks()`
- `editTask(id, newText)` — `PUT /tasks/{id}` with the new `text`, then `loadTasks()`
- `setFilter(filter)` — local-only UI state, no API call
- `render()` — the only function that touches the DOM list, draws from the current `tasks` cache
