from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    url = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    indicators = relationship(
        "Indicator",
        back_populates="source",
        cascade="all, delete"
    )
