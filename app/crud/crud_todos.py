from sqlalchemy.orm import Session

from app import schemas
from app.schemas import TodoCreate, TodoUpdate
import app.models

def get_all_todos(db:Session, user):
    todos = db.query(app.models.Todo).filter(app.models.Todo.owner_id == user.id).all()
    return todos

def get_todo_by_id(db:Session, id:int):
    todo = db.query(app.models.Todo).filter(app.models.Todo.id == id).first()
    return todo

def update_todo_by_id(id: int, user_id: int, db: Session, update_data: TodoUpdate):
    todo = db.query(app.models.Todo).filter(app.models.Todo.id == id, app.models.Todo.owner_id == user_id).first()
    if not todo:
        return None
    if update_data.title is not None:
        todo.title = update_data.title # type: ignore
    if update_data.content is not None:
        todo.content = update_data.content # type: ignore
    if update_data.completed is not None:
        todo.completed = update_data.completed # type: ignore

    if update_data.tag_ids is not None:
        tags = db.query(app.models.Tag).filter(
            app.models.Tag.id.in_(update_data.tag_ids),
            app.models.Tag.owner_id == user_id
        ).all()
        todo.tags = tags


    db.commit()
    db.refresh(todo)
    return todo 

def create(db: Session, todo: TodoCreate, user_id: int):
    tag_objects = db.query(app.models.Tag).filter(app.models.Tag.id.in_(todo.tag_ids)).all()
    db_todo = app.models.Todo(title=todo.title,
        content=todo.content,
        completed=False,
        owner_id=user_id,
        tags = tag_objects )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    
    return db_todo

def delete_todo_by_id(id: int, db: Session):
    todo = db.query(app.models.Todo).filter(app.models.Todo.id == id).first()
    if not todo:
        return None
    db.delete(todo)
    db.commit()
    return todo 