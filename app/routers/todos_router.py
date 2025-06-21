from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import User
from app.utils.dependencies import get_current_user
from app.database import get_db
from app.schemas import TodoCreate, TodoOut, TodoUpdate
import app.crud.crud_todos as crud_todos

todos_router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

@todos_router.get("/", response_model=List[TodoOut])
def get_all_todos(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_todos.get_all_todos(db = db, user=current_user)

@todos_router.get("/{id}", response_model=TodoOut)
def get_todo( id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo =  crud_todos.get_todo_by_id(id=id, db=db)

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} was not found")
    # todo_dict = todo.dict()
    if todo.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this todo")
    return todo

@todos_router.post("/create", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud_todos.create(db = db, todo=todo, user_id=current_user.id)

@todos_router.put("/{id}", status_code=status.HTTP_200_OK, response_model=TodoOut)
def update_todo(id: int,todo_update: TodoUpdate, db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = crud_todos.get_todo_by_id(id=id, db=db)

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    # todo_dict = todo.dict()
    if todo.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    updated_todo = crud_todos.update_todo_by_id(id=id, user_id=current_user.id, db=db, update_data=todo_update) # type: ignore
    return updated_todo

@todos_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = crud_todos.get_todo_by_id(id=id, db=db)

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    if todo.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    crud_todos.delete_todo_by_id(id=id, db=db)
    return
