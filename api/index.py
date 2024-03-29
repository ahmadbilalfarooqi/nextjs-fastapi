# main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Todo
from pydantic import BaseModel
from .database import SessionLocal


class Todos(BaseModel):
    name: str
    description: str


class TodoUpdate(BaseModel):
    name: str
    description: str


app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.get("/api/todos")
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos

# post method 
@app.post("/api/todos")
def create_todo(todo: Todos, db: Session = Depends(get_db)):
    new_todo = Todo(name=todo.name,
                    description=todo.description)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# put method
@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.name = updated_todo.name # type: ignore
    db_todo.description = updated_todo.description # type: ignore
    db.commit()
    return db_todo

# delete method
@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}
