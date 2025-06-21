from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_tags
from app.database import get_db
from app.models import User
from app.schemas import TagCreate, TagOut
from app.utils.dependencies import get_current_user

tags_router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)

@tags_router.get("/")
def get_all_tags(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_tags.get_all_tags(db = db, user=current_user)

@tags_router.get("/{id}", response_model=TagOut)
def get_tag(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = crud_tags.get_tag_by_id(id=id, db=db)

    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag with id {id} was not found")
    if tag.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this todo")
    return tag

@tags_router.post("/create", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    return crud_tags.create(db = db, tag=tag, user_id=current_user.id)

@tags_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tag = crud_tags.get_tag_by_id(id=id, db=db)

    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    if tag.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    crud_tags.delete_tag_by_id(id=id, db=db)
    return

@tags_router.put("/{id}", status_code=status.HTTP_200_OK, response_model=TagOut)
def update_todo(id: int,tag_update: TagCreate, db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    tag = crud_tags.get_tag_by_id(id=id, db=db)

    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    if tag.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    updated_tag = crud_tags.update_tag_by_id(id=id, db=db, update_data=tag_update)
    return updated_tag

