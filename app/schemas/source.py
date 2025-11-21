from pydantic import BaseModel
from typing import Optional


class SourceBase(BaseModel):
    name: str
    url: Optional[str] = None
    description: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None


class SourceOut(SourceBase):
    id: int

    class Config:
        from_attributes = True
