# app.py
from contextlib import asynccontextmanager
from typing import List, AsyncIterator

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import AsyncSessionLocal, init_db
from models import Task

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield

app = FastAPI(
    title="Task Tracker API",
    lifespan=lifespan
)

origins = [
    "http://localhost"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


class TaskIn(BaseModel):
    title: str
    description: str = ""


class TaskOut(TaskIn):
    id: int


@app.get("/tasks", response_model=List[TaskOut])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    return [TaskOut(id=t.id, title=t.title, description=t.description) for t in tasks]


@app.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task:
        return TaskOut(id=task.id, title=task.title, description=task.description)
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", response_model=TaskOut, status_code=201)
async def create_task(task_in: TaskIn, session: AsyncSession = Depends(get_session)):
    task = Task(title=task_in.title, description=task_in.description)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return TaskOut(id=task.id, title=task.title, description=task.description)


@app.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task_in: TaskIn, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = task_in.title
    task.description = task_in.description
    await session.commit()
    await session.refresh(task)
    return TaskOut(id=task.id, title=task.title, description=task.description)


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(task)
    await session.commit()
    return None