"""  
This module contains API routes for creating, retrieving, and editing User objects.  
"""  
  
from fastapi import APIRouter, Request, Depends, HTTPException  
from pydal import DAL  
from models.enum import Roles  
from models.user import User  
from fastapi.responses import JSONResponse  
from sqlite3 import IntegrityError  
  
router = APIRouter()  
  
  
@router.patch("/user/edit/")  
async def edit_user(request: Request, userID: int, username: str = None, email: str = None):  
    """  
    Edits a User object in the database.  
  
    Args:  
        request (Request): The incoming request.  
        userID (int): The ID of the User object to edit.  
        username (str, optional): The new username for the User object. Defaults to None.  
        email (str, optional): The new email for the User object. Defaults to None.  
  
    Raises:  
        HTTPException: If an IntegrityError occurs while updating the User object.  
  
    Returns:  
        JSONResponse: A JSON response with a status code and details about the update.  
    """  
    db: DAL = request.state.db  
  
    # Retrieve the User object from the database  
    db_entry = db((db.user.id == userID)).select().first()  
  
    if not db_entry:  
        return JSONResponse(content={"detail": "User not found, contact admin"},  
                            status_code=500)  
  
    if not username and not email:  
        return JSONResponse(content={"detail": "Nothing changed"},  
                            status_code=200)  
  
    try:  
        # Update the User object in the database  
        if username is not None:  
            db_entry.update(username=username)  
        if email is not None:  
            db_entry.update(email=email)  
  
        db.commit()  
    except IntegrityError:  
        # Raise an exception if an IntegrityError occurs  
        raise HTTPException(  
            status_code=409,  
            detail=f"Integrity Error"  
        )  
  
    return JSONResponse(content={"detail": "Changed successfully"},  
                        status_code=200)  
  
  
@router.post("/user/create/")  
async def create_user(username: str, email: str, first_name: str, last_name: str, role: str, request: Request):  
    """  
    Creates a new User object in the database.  
  
    Args:  
        username (str): The username for the new User object.  
        email (str): The email for the new User object.  
        first_name (str): The first name of the user.  
        last_name (str): The last name of the user.  
        role (str): The role of the user.  
        request (Request): The incoming request.  
  
    Returns:  
        JSONResponse: A JSON response with a status code and details about the new User object.  
    """  
    db: DAL = request.state.db  
  
    # Create the new User object in the database  
    user_id = create_user(username, email, first_name, last_name, db)  
  
    return JSONResponse(content={"detail": "User created successfully under id {}".format(str(user_id))},  
                        status_code=201)  
  
  
@router.get("/user/get/")  
async def get_user(request: Request, id: int):  
    """  
    Retrieves a User object from the database.  
  
    Args:  
        request (Request): The incoming request.  
        id (int): The ID of the User object to retrieve.  
  
    Returns:  
        JSONResponse: A JSON response with a status code and details about the retrieved User object.  
    """  
    db: DAL = request.state.db  
  
    if id is None:  
        return JSONResponse(content={"detail": "user not found", "userID": id},  
                            status_code=404)  
  
    # Retrieve the User object from the database  
    user_data = db(db.user.id == id).select().first()  
  
    if user_data:  
        return JSONResponse(content={"detail": "User found", "user": User.from_orm(user_data)}, status_code=200)  
  
    return JSONResponse
