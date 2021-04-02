import os
from io import BytesIO

import pytest
from PIL import Image, UnidentifiedImageError

from server.thumbnail_resizer import image_to_thumbnail


class TestImageToThumbnail:

    def test_image_to_thumbnail_valid_image(self):

        file = BytesIO()
        image = Image.new('RGBA', size=(150, 150), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        file_location = f'server/tests/{file.name}'

        image_to_thumbnail(file, file_location)

        resized_image = Image.open(file_location)
        assert resized_image.size == (100, 100)

        os.remove(file_location)

    def test_image_to_thumbnail_invalid_image(self):

        bad_file = BytesIO()

        with pytest.raises(UnidentifiedImageError):
            image_to_thumbnail(bad_file, 'test')
