from datetime import timedelta, datetime
from jose import jwt
from config import JWT_SECRET
from copy import deepcopy

def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = deepcopy(data)
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")