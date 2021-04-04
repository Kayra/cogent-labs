import os

from celery import Celery
from celery.utils.log import get_task_logger


celery_app = Celery(
    'tasks',
    backend=os.getenv('CELERY_BACKEND', 'redis://redis:6379/0'),
    broker=os.getenv('CELERY_BROKER', 'pyamqp://guest@rabbit//'),
    track_started=True
)

logger = get_task_logger(__name__)
