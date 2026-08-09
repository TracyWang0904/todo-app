from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="To-Do API")


class Task(BaseModel):
    id: int
    text: str
    done: bool = False


class TaskCreate(BaseModel):
    text: str


class TaskUpdate(BaseModel):
    text: Optional[str] = None
    done: Optional[bool] = None


tasks: list[Task] = []
next_id = 1


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks", status_code=201)
def add_task(new_task: TaskCreate):
    global next_id
    task = Task(id=next_id, text=new_task.text, done=False)
    tasks.append(task)
    next_id += 1
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    for task in tasks:
        if task.id == task_id:
            if update.text is not None:
                task.text = update.text
            if update.done is not None:
                task.done = update.done
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return
    raise HTTPException(status_code=404, detail="Task not found")
