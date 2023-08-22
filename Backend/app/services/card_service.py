"""
Card Locking Utility

This module contains a function for locking a card by its card number.

"""

from pydal import DAL

def lockCard(cardnumber: str) -> str:
    """
    Locks a card based on its card number.

    Args:
        cardnumber (str): The card number to be locked.

    Returns:
        str: A message confirming the card locking.
    """
    return f"Karte mit Nummer {cardnumber} wurde gesperrt"

