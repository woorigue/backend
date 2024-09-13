from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.model.user import User

SECRET_KEY = "JWTSECRETKEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7

RLS_SECRET_KEY = "NvbeIjVAT/MW8ihG5pWzb03pzI3PlSCRFJE8B0IzyUAlIzxXiJinD8ywbjQEfOilhkD+fARoW/SlWiU5LrFncw=="
RLS_ALGORITHM = "HS256"
RLS_ACCESS_TOKEN_EXPIRE_DAYS = 365
RLS_REFRESH_TOKEN_EXPIRE_DAYS = 365

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_header = APIKeyHeader(name="Authorization")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode = data.copy()
    expire = datetime.now() + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict):
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = data.copy()
    expire = datetime.now() + refresh_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(bearer_header)], db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # TODO: Use HTTPBearer
    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"system_code": "EXPIRED_ACCESS_TOKEN"},
        )
    except JWTError:
        raise credentials_exception
    user = db.scalar(select(User).where(User.email == username))
    if user is None:
        raise credentials_exception
    return user


def validate_refresh_token(
    token: Annotated[str, Depends(bearer_header)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"system_code": "EXPIRED_REFRESH_TOKEN"},
        )
    except JWTError:
        raise credentials_exception


def create_rls_access_token(data: dict):
    access_token_expires = timedelta(days=RLS_ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode = data.copy()
    expire = datetime.now() + access_token_expires
    to_encode.update(
        {
            "exp": expire,
            "aud": "authenticated",
            "role": "authenticated",
        }
    )
    encoded_jwt = jwt.encode(to_encode, RLS_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_rls_refresh_token(data: dict):
    refresh_token_expires = timedelta(days=RLS_REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = data.copy()
    expire = datetime.now() + refresh_token_expires
    to_encode.update(
        {
            "exp": expire,
            "aud": "authenticated",
            "role": "authenticated",
        }
    )
    encoded_jwt = jwt.encode(to_encode, RLS_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
