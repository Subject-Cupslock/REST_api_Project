from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas, utils, oauth2
from app.database import get_db
from app.exceptions import UserAlreadyExistsException, InvalidCredentialsException

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post('/register', response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise UserAlreadyExistsException(email=user.email)

    hashed_pw = utils.hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.password):
        raise InvalidCredentialsException()

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/me', response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user
