"""
Enums for User Roles and Categories

This module defines enumerations for user roles and request categories.

"""

from enum import Enum

class Roles(str, Enum):
    """
    User Roles Enumeration

    Represents the roles that users can have in the application.

    Attributes:
        ADMIN (str): The admin role.
        USER (str): The user role.

    """
    ADMIN = "admin"
    USER = "user"

class Categories(str, Enum):
    """
    Request Categories Enumeration

    Represents categories for customer service requests.

    Attributes:
        GENERAL (str): General category.
        CARD (str): Card-related category.
        CREDIT (str): Credit-related category.

    """
    GENERAL = "General"
    CARD = "Card"
    CREDIT = "Credit"
