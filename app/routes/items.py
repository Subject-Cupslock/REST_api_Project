from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix = '/items',
    tags = ['Items']
)

@router.post("/", response_model = schemas.ItemResponse)
def create_item(item:schemas.ItemCreate, db:Session = Depends(get_db), current_user:models.User = Depends(get_current_user)):
    new_item = models.Item(**item.dict(), owner_id = current_user.id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model = List[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Item).filter(models.Item.owner_id == current_user.id).all()

@router.get("/{id}", response_model = schemas.ItemResponse)
def get_item(id:int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Item).filter(models.Item.id == id, models.Item.owner_id==current_user.id).first()
    if not item:
        raise HTTPException(status_code = 404, detail = 'Item not found')
    return item

@router.put("/{id}", response_model = schemas.ItemResponse)
def update_item(id:int,update_item: schemas.ItemUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Item).filter(models.Item.id == id, models.Item.owner_id==current_user.id).first()
    if not item:
        raise HTTPException(status_code = 404, detail = 'Item not found')
    for key, value in update_item.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_item(id:int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Item).filter(models.Item.id == id, models.Item.owner_id==current_user.id).first()
    if not item:
        raise HTTPException(status_code = 404, detail = 'Item not found')
    db.delete(item)
    db.commit()
    return None