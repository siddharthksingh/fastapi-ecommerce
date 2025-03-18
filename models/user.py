from pydantic import BaseModel, EmailStr

class User(BaseModel):
    role: str
    name: str
    email: EmailStr
    password: str
    cartID: int | None

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: strs