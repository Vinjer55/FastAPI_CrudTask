from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.security import authenticate_user, create_access_token
from src.db import models
from fastapi import APIRouter, Depends, HTTPException, status
from src.db.database import engine
from typing import Annotated
from src.db.database import db_dependency
from src.schemas.token import Token
from src.schemas.user import RegisterUserRequest
from src.auth.security import bcrypt_context, user_dependency
from dotenv import load_dotenv
import os

load_dotenv()

models.Base.metadata.create_all(bind=engine)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

@auth_router.get("/", summary="Get current user")
async def read_current_user(user: user_dependency, db : db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"User": user}

@auth_router.post("/register", summary="Create a new user")
async def create_user(user: RegisterUserRequest, db: db_dependency):
    db_user = models.User(
            username=user.username,
            hashed_password=bcrypt_context.hash(user.password)
        )
    
    if db.query(models.User).filter(models.User.username == user.username).first() is not None:
            raise HTTPException(status_code=400, detail="Username already registered")

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {"message": "User created successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An internal error occurred.")

@auth_router.post("/token", response_model=Token, summary="Get access token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db : db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token = create_access_token(user.username, user.id, timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    
    return {'access_token': token, 'token_type': 'bearer'}
