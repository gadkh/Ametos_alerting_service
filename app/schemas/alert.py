from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any


class AlertCreate(BaseModel):
    device_id: str
    event_type: str
    alert_message: str
    timestamp: datetime
    event: Dict[str, Any]


class AlertResponse(AlertCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
