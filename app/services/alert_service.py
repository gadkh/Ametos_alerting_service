from sqlalchemy.orm import Session
from ..db.models.alerts import Alert
from app.schemas.alert import AlertCreate

from dotenv import load_dotenv
from ..db.redis_client import redis_client
import os
import json
import redis

load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6380)
REDIS_DB = os.getenv("REDIS_DB", 0)
VALID_USERS_SET = "valid_users"


def process_alert(db: Session, event_data: dict):
    if event_data.get('event_type') == 'security_breach':
        new_alert = Alert(
            device_id=event_data["device_id"],
            alert_type="security",
            message="Security breach detected"
        )
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        return new_alert
    return None


def create_alert(db: Session, alert_data: AlertCreate):
    db_alert = Alert(**alert_data.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_alerts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Alert).offset(skip).limit(limit).all()


def handle_unauthorized_access(event_data, db: Session):
    if not redis_client.sismember(VALID_USERS_SET, event_data["user_id"]):
        alert = Alert(
            device_id=event_data["device_id"],
            alert_type="Unauthorized Access",
            details=f"User is not authorized.",
            timestamp=event_data["timestamp"],
            event=json.dumps(event_data)
        )
        db.add(alert)
        db.commit()
        print("Unauthorized access alert stored.")


def handle_speed_violation(event_data, db: Session):
    if event_data["speed_kmh"] > 90:
        alert = Alert(
            device_id=event_data["device_id"],
            alert_type="Speed Violation",
            details=f"Speed violation detected: {event_data['speed_kmh']} km/h",
            timestamp=event_data["timestamp"],
            event=event_data
        )
        db.add(alert)
        db.commit()
        print("Speed violation alert stored.")


def handle_intrusion_detection(event_data, db: Session):
    if event_data["zone"] == "Restricted Area":
        alert = Alert(
            device_id=event_data["device_id"],
            alert_type="Intrusion Detection",
            details=f"Intrusion detected in restricted area for device {event_data['device_id']}",
            timestamp=event_data["timestamp"],
            event=event_data
        )
        db.add(alert)
        db.commit()
        print("Intrusion detection alert stored.")


