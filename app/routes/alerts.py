from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..db.models.alerts import Alert
from ..db.session_handler import get_session

router = APIRouter()


@router.get("/alerts")
def get_alerts(
    db: Session = Depends(get_session),
    device_id: Optional[str] = None,
    event_type: Optional[str] = None
):
    query = db.query(Alert)
    if device_id:
        query = query.filter(Alert.device_id == device_id)
    if event_type:
        query = query.filter(Alert.event_type == event_type)
    return query.all()

