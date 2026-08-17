import os
import sqlite3
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="To-Do API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "todo.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


class Task(BaseModel):
    id: int
    text: str
    done: bool


class TaskCreate(BaseModel):
    text: str


class TaskUpdate(BaseModel):
    text: Optional[str] = None
    done: Optional[bool] = None


def row_to_task(row: sqlite3.Row) -> Task:
    return Task(id=row["id"], text=row["text"], done=bool(row["done"]))


@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [row_to_task(row) for row in rows]


@app.post("/tasks", status_code=201)
def add_task(new_task: TaskCreate):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (text, done) VALUES (?, ?)", (new_task.text, 0)
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.close()
    return row_to_task(row)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    new_text = update.text if update.text is not None else row["text"]
    new_done = update.done if update.done is not None else bool(row["done"])

    conn.execute(
        "UPDATE tasks SET text = ?, done = ? WHERE id = ?",
        (new_text, int(new_done), task_id),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return row_to_task(row)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
