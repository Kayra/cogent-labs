from io import BytesIO
from typing import Union, List
from tempfile import SpooledTemporaryFile

from PIL import Image


def image_to_thumbnail(image: Union[str, SpooledTemporaryFile, BytesIO],
                       thumbnail_name: str, size: Union[List, None] = None) -> None:

    if not size:
        size = 100, 100

    image_file = Image.open(image)
    resized_image = image_file.resize(size)
    resized_image.save(thumbnail_name)
