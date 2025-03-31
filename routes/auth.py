from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from models.user import UserCreate, UserLogin, User
from database import db
from utils import create_jwt_token, verify_token
from datetime import timedelta
from utils import require_roles

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    new_user = user.model_dump()
    new_user.update({"role": "user"})
    await db.users.insert_one(new_user)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token({"email": db_user["email"], "role": db_user["role"]}, timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/get", response_model=dict[str, list[User]])
@require_roles(["admin"])
async def display_users(user: dict = Depends(verify_token)):
    """Display details of all users"""
    users = await db.users.find().to_list(None)
    return {"users": users}

@router.put("/update")
@require_roles(["admin"])
async def make_admin(email: str, user: dict = Depends(verify_token)):
    """Assign admin role to a user"""

    # Check if user exists in the database
    user_data = await db.users.find_one({"email": email})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    await db.users.update_one(
        {"email": email},
        {"$set": {"role": "admin"}}
    )
    return {"message": f"User {email} is now an admin"}