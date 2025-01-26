# from celery import Celery
# from ..core.config import RABBITMQ_URL
# from app.db.session_handler import get_session
# from app.services.alert_service import process_alert
# import json
#
# celery_app = Celery('alert_worker', broker=RABBITMQ_URL)
#
#
# @celery_app.task(queue='alerts_queue')
# def handle_event(event_data):
#     db_gen = get_session()
#     db = next(db_gen)
#     try:
#         event = json.loads(event_data)
#         process_alert(db, event)
#     finally:
#         db.close()
#
#
#
#
#

from celery import Celery
import json
from sqlalchemy.orm import Session
from ..core.config import RABBITMQ_URL
from ..db.session_handler import get_session
from ..db.models.alerts import Alert
from ..services.alert_service import handle_speed_violation, handle_intrusion_detection, handle_unauthorized_access
import base64
import os

celery_app = Celery(
    "alert_service",
    broker=os.getenv("RABBITMQ_URL", RABBITMQ_URL),
)

celery_app.conf.task_routes = {
    "tasks.process_event": {"queue": "events"}
}


@celery_app.task(name="tasks.process_event")
def process_event(event_data):
    """Process incoming events and generate alerts if necessary."""
    db = next(get_session())
    print("Hellooo")
    print(f"event_data:{event_data}")
    event_data["timestamp"] = event_data["timestamp"].isoformat()
    if event_data["device_type"] == "access_controller":
        handle_unauthorized_access(event_data, db)
    elif event_data["device_type"] in "radar":
        handle_speed_violation(event_data, db)
    elif event_data["device_type"] in "security_camera":
        handle_intrusion_detection(event_data, db)
    db.close()



