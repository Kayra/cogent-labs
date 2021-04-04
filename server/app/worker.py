from typing import Union, List

from PIL import Image
from celery import Celery
from celery.utils.log import get_task_logger


celery_app = Celery('tasks', backend='redis://redis:6379/0', broker='pyamqp://guest@rabbit//', track_started=True)
logger = get_task_logger(__name__)


@celery_app.task
def image_to_thumbnail(image_location: str, thumbnail_name: str, size: Union[List, None] = None) -> None:

    if not size:
        size = 100, 100

    image_file = Image.open(image_location)
    resized_image = image_file.resize(size)
    resized_image.save(thumbnail_name)
