"""  
This module contains a function for handling database connections in FastAPI.  
"""  
  
from fastapi import Request  
from database import db  
  
  
async def db_connection(request: Request, call_next):  
    """  
    Handles database connections in FastAPI.  
  
    Args:  
        request (Request): The incoming request.  
        call_next (function): The next function to call in the request cycle.  
  
    Returns:  
        The response from the next function in the request cycle.  
    """  
    # Reconnect to the database  
    db._adapter.reconnect()  
    # Add the database connection to the request state  
    request.state.db = db  
    try:  
        # Call the next function in the request cycle  
        response = await call_next(request)  
    finally:  
        # Close the database connection  
        db._adapter.close()  
    # Return the response from the next function in the request cycle  
    return response  
