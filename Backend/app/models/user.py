"""
User Pydantic Model

This module defines the Pydantic model for user data used in the application.

"""

from pydantic import BaseModel
from models.enum import Roles

class User(BaseModel):
    """
    User Model

    Represents user data.

    Attributes:
        id (int): The ID of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        role (Roles): The role of the user.

    """
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        """
        Pydantic Config

        Configuration for the Pydantic model.

        """
        orm_mode = True
