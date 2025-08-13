from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post('/register', response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= 'Email alredy registered')
    

    hashed_pw = utils.hash_password(user.password)
    new_user = models.User(username= user.username, email = user.email, paswword=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user