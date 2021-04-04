from celery import Celery
from celery.utils.log import get_task_logger


celery_app = Celery(
    'tasks',
    backend='redis://redis:6379/0',
    broker='pyamqp://guest@rabbit//',
    track_started=True
)

logger = get_task_logger(__name__)
