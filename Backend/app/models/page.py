from pydantic import BaseModel
from typing import Optional, List

from models.enum import Roles
from models.csrequest import CSRequest
from typing import List


class Page(BaseModel):
    pageContents: List[CSRequest]
    maximumPages: int
    page: int

    class Config:
        orm_mode = False