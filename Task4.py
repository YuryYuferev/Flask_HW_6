# Напишите API для управления списком задач. Для этого создайте модель Task со следующими полями:
# id: int (первичный ключ)
# title: str (название задачи)
# description: str (описание задачи)
# done: bool (статус выполнения задачи)
# API должно поддерживать следующие операции:
# Получение списка всех задач: GET /tasks/
# Получение информации о конкретной задаче: GET /tasks/{task_id}/
# Создание новой задачи: POST /tasks/
# Обновление информации о задаче: PUT /tasks/{task_id}/
# Удаление задачи: DELETE /tasks/{task_id}/
# Для валидации данных используйте параметры Field модели Task.
# Для работы с базой данных используйте SQLAlchemy и модуль databases.


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание подключения к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель для задачи
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    done = Column(Boolean, default=False)

# Создание таблицы в базе данных при первом запуске
Base.metadata.create_all(bind=engine)

# Модель для создания/обновления задачи
class TaskCreateUpdate(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=255)
    done: bool = Field(default=False)

app = FastAPI()

# Получение списка всех задач
@app.get("/tasks/")
async def get_tasks(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks

# Получение информации о конкретной задаче
@app.get("/tasks/{task_id}/")
async def get_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Создание новой задачи
@app.post("/tasks/")
async def create_task(task: TaskCreateUpdate):
    db = SessionLocal()
    db_task = Task(title=task.title, description=task.description, done=task.done)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Обновление информации о задаче
@app.put("/tasks/{task_id}/")
async def update_task(task_id: int, updated_task: TaskCreateUpdate):
    db = SessionLocal()
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = updated_task.title
    db_task.description = updated_task.description
    db_task.done = updated_task.done
    db.commit()
    db.refresh(db_task)
    return db_task

# Удаление задачи
@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    db = SessionLocal()
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}

# uvicorn Task4:app --reload
