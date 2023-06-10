from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from typing import Annotated

from core.database import db
from schemas.auth import UserRegister, UserInfo
from utils import get_password_hash, verify_password, create_access_token


router = APIRouter(prefix="/api/auth", tags=["auth"])

users = db["users"]


@router.post("/signup", description="register user")
async def signup_user(user: UserRegister):
    # Check if the user already exists
    existing_user = users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Account already exists")

    # Hash the password and insert the new user data into the database
    password_hash = get_password_hash(user.password)

    user_dict = user.dict()
    user_dict['password'] = password_hash
    user_dict['settings'] = {"lang": "ch",
                             "region": "us", "category": "technology"}
    user_dict['created_at'] = datetime.utcnow()
    user_dict['updated_at'] = user_dict['created_at']
    users.insert_one(user_dict)

    return {"status": "success"}


@router.post("/signin", description="login user")
async def signin_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username", headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "user": UserInfo(**user)}
