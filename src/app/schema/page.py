from pydantic import BaseModel
from typing import Any
from .pagination import Pagination

class Page(BaseModel):
    data: list[Any]
    meta: Pagination

