import pytest
from app.schemas.alert import AlertCreate
from app.services.alert_service import process_alert
from app.db.models.alerts import Alert
from app.db.session_handler import SessionLocal
from datetime import datetime
import json


@pytest.fixture
def sample_alert():
    return AlertCreate(
        device_id="AA:BB:CC:DD:EE:FF",
        event_type="motion_detected",
        alert_message="Unauthorized access detected",
        timestamp=datetime.utcnow(),
        event={
            "zone": "Restricted Area",
            "confidence": 0.98
        }
    )


@pytest.fixture
def db_session():
    db = SessionLocal()
    yield db
    db.close()


def test_alert_creation(db_session, sample_alert):
    """Test if an alert is correctly processed and stored."""
    process_alert(db_session, sample_alert.dict())

    alert = db_session.query(Alert).filter_by(device_id="AA:BB:CC:DD:EE:FF").first()
    event = json.loads(alert.event)
    print(f"event:::: {event}")
    assert alert is not None


def test_alert_event_serialization(sample_alert):
    """Test serialization of event data for alert processing."""
    alert_dict = sample_alert.dict()
    json_event = json.dumps(alert_dict['event'])

    assert isinstance(json_event, str)
    assert "Restricted Area" in json_event


def test_alert_invalid_data():
    """Test handling of invalid alert data."""
    with pytest.raises(ValueError):
        AlertCreate(
            device_id="INVALID_ID",
            event_type="",
            alert_message="",
            timestamp="invalid_timestamp",
            event=None
        )
