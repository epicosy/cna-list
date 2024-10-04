from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional


class Scope(BaseModel):
    external: bool
    third_party: bool
    organizations: List[str]


class CNA(BaseModel):
    id: str
    name: str
    root: EmailStr
    email: EmailStr
    scope: Scope
    advisories: Optional[HttpUrl] = None
