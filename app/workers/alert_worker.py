from celery import Celery
from ..db.session_handler import get_session
from ..services.alert_service import handle_speed_violation, handle_intrusion_detection, handle_unauthorized_access
import os
from dotenv import load_dotenv

running_in_docker = os.getenv("RUNNING_IN_DOCKER")
if not running_in_docker:
    load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")


celery_app = Celery(
    "alert_service",
    # broker=os.getenv("RABBITMQ_URL", RABBITMQ_URL),
    broker=RABBITMQ_URL
)

celery_app.conf.task_routes = {
    "tasks.process_event": {"queue": "events"}
}


@celery_app.task(name="tasks.process_event")
def process_event(event_data):
    """Process incoming events and generate alerts if necessary."""
    db = next(get_session())
    event_data["timestamp"] = event_data["timestamp"].isoformat()
    if event_data["device_type"] == "access_controller":
        handle_unauthorized_access(event_data, db)
    elif event_data["device_type"] in "radar":
        handle_speed_violation(event_data, db)
    elif event_data["device_type"] in "security_camera":
        handle_intrusion_detection(event_data, db)
    db.close()



