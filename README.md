# To-Do List

A tiny vanilla JS/HTML/CSS to-do list. No backend, no build step, no dependencies — just open `index.html`.

There's also a separate FastAPI backend exercise in [api/](api/) — a plain-Python-list to-do API, not yet wired up to this frontend.

## Features

- Add a task (Enter or the Add button)
- Mark a task done (checkbox, strikethrough text)
- Edit a task (click Edit, or double-click the text; Enter/blur saves, Escape cancels)
- Delete a task
- Filter: All / Active / Done

## Run it

Just open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

then visit `http://localhost:8000`.

## Code structure

All state lives in one array (`tasks`) in [script.js](script.js) — the single source of truth. Every user action calls a small function that updates `tasks` and then calls `render()`, which redraws the whole list from the array:

- `addTask(text)`
- `deleteTask(id)`
- `toggleTask(id)`
- `editTask(id, newText)`
- `setFilter(filter)`
- `render()` — the only function that touches the DOM list
