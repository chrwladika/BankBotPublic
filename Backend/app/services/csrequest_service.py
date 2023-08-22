"""
CSRequest Database Operations

This module contains functions for retrieving and scheduling CSRequest objects from a database.

"""

from typing import List
from pydal import DAL
from models.csrequest import CSRequest
from models.page import Page


def get_page_csrequests(db: DAL, page: int, category: str) -> List[dict]:
    """
        Retrieves a page of CSRequest objects from a database.

        Args:
            db (DAL): The database connection object.
            page (int): The page number to retrieve.
            page_size (int): The number of CSRequest objects to retrieve per page.
            category (str, optional): Filter requests by category. Defaults to "".

        Returns:
            List[dict]: A list of dictionaries, each representing a CSRequest object.
    """
    offset = (page - 1) * 8
    rows = db((category == "") | (category == None) |
              (db.csrequests.category == category)).select(limitby=(offset, offset + 8), orderby=db.csrequests.id)
    maximum_pages = db((category == "") | (category == None) |
              (db.csrequests.category == category)).count()

    contents = []
    for row in rows:
        user = db(db.user.id == row.user_ref).select(db.user.ALL).first()
        content = CSRequest(id=row.id,
                            request=row.request,
                            customer_firstname=user.first_name,
                            customer_lastname=user.last_name,
                            category=row.category,
                            telephone=row.telephone)
        contents.append(content)


    page = Page(maximumPages=maximum_pages, page=page, pageContents=contents)

    print(page)
    return page


def get_csrequest_by_id(db: DAL, id: int) -> dict:
    """
    Retrieves a CSRequest object by its ID from a database.

    Args:
        db (DAL): The database connection object.
        id (int): The ID of the CSRequest object to retrieve.

    Returns:
        dict: A dictionary representing the CSRequest object.
    """
    row = db(db.csrequests.id == id).select(db.csrequests.ALL).first()
    csrequest = CSRequest.from_orm(row).dict()
    return csrequest
"""
This module contains functions for retrieving CSRequest objects from a database.
"""




def schedule_call(db: DAL, request: str, userID: int, telephone: str, category: str):
    """
    Schedule a Call Request

    Args:
        db (DAL): The database connection object.
        request (str): The call request details.
        userID (int): The ID of the user scheduling the call.
        telephone (str): The telephone number for the call.
        category (str): The category of the call request.

    Returns:
        str: A confirmation message indicating the call was scheduled.
    """
    db.csrequests.insert(user_ref=userID, request=request, telephone=telephone, category=category)
    db.commit()
    return "Call was scheduled"
