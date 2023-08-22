"""
CSRequest Pydantic Model

This module defines the Pydantic model for customer service requests used in the application.

"""

from pydantic import BaseModel
from typing import Optional, List



class CSRequest(BaseModel):
    """
    CSRequest Model

    Represents a customer service request.

    Attributes:
        id (int): The ID of the request.
        request (str): The details of the request.
        user_ref (int): The reference ID of the user making the request.
        category (str): The category of the request.
        telephone (str): The telephone number associated with the request.

    """
    id: int
    request: str
    customer_firstname: str
    customer_lastname: str
    category: str
    telephone: str

    class Config:
        orm_mode = True