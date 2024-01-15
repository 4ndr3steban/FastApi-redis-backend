from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped
import time

class Base(DeclarativeBase):
    pass

class Tmetric(Base):
    __tablename__ = "metrics"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    device_id: Mapped[str] = Column(String(30), index=True)
    metric_type: Mapped[str] = Column(String(5))
    metric_value: Mapped[float] = Column(Float)
    timestamp: Mapped[str] = Column(String(50), default=str(time.time()))
