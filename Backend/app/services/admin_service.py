"""
User Management Utilities

This module contains utility functions for managing user-related operations.

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

def create_user(username: str, email: str, first_name: str, last_name: str, role: str, db: DAL) -> int:
    """
    Create a new user and insert it into the database.

    Args:
        username (str): The user's username.
        email (str): The user's email address.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        role (str): The user's role.
        db (DAL): The PyDAL database connection.

    Returns:
        int: The ID of the newly created user.

    """
    user_id = db.user.insert(username=username, email=email, first_name=first_name,
                             last_name=last_name, role=role)
    db.commit()
    return user_id
