from sqlalchemy.orm import Session
from app.schemas import TagCreate
import app.models

def get_all_tags(db:Session, user):
    tags = db.query(app.models.Tag).filter(app.models.Tag.owner_id == user.id).all()
    return tags

def get_tag_by_id(db:Session, id:int):
    tag = db.query(app.models.Tag).filter(app.models.Tag.id == id).first()
    return tag

def create(db: Session, tag: TagCreate, user_id: int):
    db_tag = app.models.Tag(name=tag.name,
        owner_id=user_id )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag_by_id(id: int, db: Session):
    tag = db.query(app.models.Tag).filter(app.models.Tag.id == id).first()
    if not tag:
        return None
    db.delete(tag)
    db.commit()
    return tag 

def update_tag_by_id(id: int, db: Session, update_data: TagCreate):
    tag = db.query(app.models.Tag).filter(app.models.Tag.id == id).first()
    if not tag:
        return None

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(tag, key, value)

    db.commit()
    db.refresh(tag)
    return tag 

