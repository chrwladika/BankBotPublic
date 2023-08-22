"""
Authentication and Authorization Utilities

This module contains utility functions and classes related to authentication and authorization.

"""

import secrets
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import exceptions
from pydal import DAL
import jwt
from datetime import datetime, timedelta
from passlib.hash import bcrypt

from common.dependencies import db_connection
from models.enum import Roles
from models.user import User

# OAuth2PasswordBearer instance for token retrieval
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_access_token(data: dict, expires_delta: timedelta) -> str:
    """
    Generate an access token.

    Args:
        data (dict): Data to be encoded into the token.
        expires_delta (timedelta): Token expiration time.

    Returns:
        str: The generated access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secrets.JWT_SECRET_KEY, algorithm=secrets.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current user from the token.

    Args:
        token (str): Access token.

    Returns:
        User: The current user.
    """
    try:
        payload = jwt.decode(token, secrets.JWT_SECRET_KEY, algorithms=[secrets.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return db_connection().get(User, user_id)

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user.

    Args:
        current_user (User): The current user.

    Returns:
        User: The current active user.
    """
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
