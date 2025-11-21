from pydantic import BaseModel
from typing import Optional


class ZoneBase(BaseModel):
    name: str
    postal_code: Optional[str] = None
    geom: Optional[str] = None


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    name: Optional[str] = None
    postal_code: Optional[str] = None
    geom: Optional[str] = None


class ZoneOut(ZoneBase):
    id: int

    class Config:
        from_attributes = True
