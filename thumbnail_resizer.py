from typing import Union, List

from PIL import Image


def image_to_thumbnail(image_location: str, size: Union[List, None] = None) -> None:

    if not size:
        size = 100, 100

    image = Image.open(image_location)
    resized_image = image.resize(size)
    resized_image.save('thumbnail.jpg')
