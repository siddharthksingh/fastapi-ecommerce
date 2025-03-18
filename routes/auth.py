from fastapi import APIRouter, HTTPException
from models.user import UserCreate, UserLogin
from database import db
from utils.gen_token import create_jwt_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    new_user = user.model_dump()
    new_user.update({"role": "user"})
    await db.users.insert_one(new_user)

@router.post("/login")
async def login_user(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token({"sub": {"email": db_user["email"], "role": db_user["role"]}}, timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}