import os
from io import BytesIO

import pytest
from PIL import Image, UnidentifiedImageError

from server.thumbnail_resizer import image_to_thumbnail


class TestImageToThumbnail:

    def test_image_to_thumbnail_valid_image(self, test_image_file):

        test_image_file.seek(0)
        file_location = f'server/tests/{test_image_file.name}'

        image_to_thumbnail(test_image_file, file_location)

        resized_image = Image.open(file_location)
        assert resized_image.size == (100, 100)

        os.remove(file_location)
        test_image_file.close()

    def test_image_to_thumbnail_invalid_image(self):

        bad_file = BytesIO()

        with pytest.raises(UnidentifiedImageError):
            image_to_thumbnail(bad_file, 'test')
