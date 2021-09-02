from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from starlette import status

import settings
from models import User
from servise import user_servises

SECRET = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def get_user(username: str) -> User:
    user = user_servises.get_user_by_name(username)
    return user


def verify_token(token: str) -> dict or False:
    try:
        jwt_decode = jwt.decode(token, SECRET, algorithms=ALGORITHM)
    except jwt.JWTError:
        return False
    else:
        now = datetime.now()
        delta = (now - datetime(1970, 1, 1)).total_seconds()
        print(f"{delta} || {jwt_decode['exp']}")
        if delta < jwt_decode["exp"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token is dead",
                headers={"WWW-Authenticate": "Bearer"}
            )
        else:
            return {"user_role": jwt_decode["user_role"]}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str) -> bool or User:
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def login_for_access_token(username: str, password: str) -> dict:
    current_user = authenticate_user(username, password)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"user_role": current_user.role_code}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


def check_role(cookies: Request.cookies, role: int) -> bool:
    if "access_token" in cookies:
        temp = verify_token(cookies["access_token"])
        if temp:
            if temp["user_role"] >= role:
                return True
        else:
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Access denied",
                headers={"WWW-Authenticate": "Bearer"}
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"}
        )
