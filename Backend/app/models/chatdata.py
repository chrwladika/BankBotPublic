"""
ChatData Pydantic Model

This module defines the Pydantic model for chat data used in the application.

"""

from pydantic import BaseModel

class ChatData(BaseModel):
    """
    ChatData Model

    Represents a chat message.

    Attributes:
        message (str): The chat message content.

    """
    message: str

    class Config:
        """
        Pydantic Config

        Configuration for the Pydantic model.

        """
        orm_mode = True
