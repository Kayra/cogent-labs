from typing import Union, List

from PIL import Image
from workers.celery_main import celery_app


@celery_app.task(autoretry_for=(OSError, FileNotFoundError, SyntaxError), default_retry_delay=1)
def image_to_thumbnail(image_location: str, thumbnail_name: str, size: Union[List, None] = None) -> None:

    if not size:
        size = 100, 100

    image_file = Image.open(image_location)
    resized_image = image_file.resize(size)
    resized_image.save(thumbnail_name)
