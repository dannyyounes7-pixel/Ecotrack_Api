from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    postal_code = Column(String, nullable=True, index=True)
    geom = Column(String, nullable=True)  # optionnel

    indicators = relationship(
        "Indicator",
        back_populates="zone",
        cascade="all, delete"
    )
