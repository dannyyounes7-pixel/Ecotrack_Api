from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class IndicatorBase(BaseModel):
    source_id: int
    zone_id: int
    type: str
    value: float
    unit: str
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class IndicatorCreate(IndicatorBase):
    pass


class IndicatorUpdate(BaseModel):
    source_id: Optional[int] = None
    zone_id: Optional[int] = None
    type: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class IndicatorOut(IndicatorBase):
    id: int

    class Config:
        from_attributes = True
