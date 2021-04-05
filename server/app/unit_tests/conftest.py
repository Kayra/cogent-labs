from io import BytesIO

import pytest
from PIL import Image


@pytest.fixture()
def test_image_file():

    image_file = BytesIO()
    image = Image.new('RGBA', size=(150, 150), color=(155, 0, 0))
    image.save(image_file, 'png')
    image_file.name = 'test.png'

    yield image_file
