from pydantic import BaseModel


class User(BaseModel):
    role: str
    name: str
    email: str
    password: str
    cart: dict[str, int] = {}

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str