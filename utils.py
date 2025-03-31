from datetime import timedelta, datetime
from copy import deepcopy
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from config import JWT_SECRET
from functools import wraps
from fastapi import HTTPException, Depends, status

def require_roles(allowed_roles: list):
    """Decorator to restrict endpoint access based on user roles."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user: dict = Depends(verify_token), **kwargs):
            if user["role"] not in allowed_roles:
                raise HTTPException(status_code=403, detail="Access forbidden: Insufficient role")
            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator

def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = deepcopy(data)
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")


bearer_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload  # Returns decoded token data (e.g., {"sub": "user@example.com"})
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
