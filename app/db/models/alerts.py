from sqlalchemy import Column, Integer, String, DateTime, func, TIMESTAMP
from ..session_handler import Base
from sqlalchemy.dialects.postgresql import JSONB


# class Alert(Base):
#     __tablename__ = "alerts"
#
#     id = Column(Integer, primary_key=True, index=True)
#     device_id = Column(String, index=True)
#     event_type = Column(String, index=True)
#     timestamp = Column(TIMESTAMP, nullable=False)
#     created_at = Column(DateTime, default=func.now())
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    alert_type = Column(String, index=True)
    timestamp = Column(TIMESTAMP)
    details = Column(String)
    created_at = Column(DateTime, default=func.now())
    event = Column(JSONB)
