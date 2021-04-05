import os
import time
from io import BytesIO

import requests
from PIL import Image


TEST_HOST = "http://127.0.0.1:8000"


class TestResizeImageToThumbnailView:

    thumbnail_view_endpoint = os.path.join(TEST_HOST, 'thumbnails')

    def test_post_valid_image(self, test_image_file):

        test_image_file.seek(0)

        response = requests.post(self.thumbnail_view_endpoint, files={'image': test_image_file})

        assert response.status_code == 202
        assert 'Resized image URL' in response.json()

    def test_post_invalid_image(self):

        bad_file = BytesIO()

        response = requests.post(self.thumbnail_view_endpoint, files={'image': bad_file})

        assert response.status_code == 400
        assert 'Error' in response.json()

    @classmethod
    def teardown_class(cls):
        images = [image for image in os.listdir() if '.png' in image]
        for image in images:
            os.remove(image)


class TestReturnThumbnailView:

    thumbnail_view_endpoint = os.path.join(TEST_HOST, 'thumbnails')

    def test_request_valid_image(self, test_image_file):

        test_image_file.seek(0)
        resize_response = requests.post(self.thumbnail_view_endpoint, files={'image': test_image_file})
        image_name = resize_response.json()['Resized image URL'].split('/')[-1]

        resized_image_url = os.path.join(self.thumbnail_view_endpoint, image_name)
        image_response = requests.get(resized_image_url)

        while image_response.status_code == 409:
            image_response = requests.get(resized_image_url)
            time.sleep(1)

        image_stream = BytesIO(image_response.content)
        resized_image = Image.open(image_stream)

        assert resized_image.size == (100, 100)
        assert image_response.status_code == 200

    def test_request_invalid_image(self):

        resized_image_url = os.path.join(self.thumbnail_view_endpoint, 'bad_image.jpg')
        image_response = requests.get(resized_image_url)

        assert image_response.status_code == 404
        assert 'Error' in image_response.json()

    def test_request_pending_image(self):

        test_image_file = BytesIO()
        image = Image.new('RGBA', size=(5000, 5000), color=(155, 0, 0))
        image.save(test_image_file, 'png')
        test_image_file.name = 'test.png'
        test_image_file.seek(0)

        resize_response = requests.post(self.thumbnail_view_endpoint, files={'image': test_image_file})
        image_name = resize_response.json()['Resized image URL'].split('/')[-1]

        resized_image_url = os.path.join(self.thumbnail_view_endpoint, image_name)
        image_response = requests.get(resized_image_url)

        assert image_response.status_code == 409
        assert 'Processing' in image_response.json()
        assert any([status in image_response.json()['Processing'] for status in ['PENDING', 'RETRY']])

    @classmethod
    def teardown_class(cls):
        images = [image for image in os.listdir() if '.png' in image]
        for image in images:
            os.remove(image)
