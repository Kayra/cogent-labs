import os
from io import BytesIO

import requests


TEST_HOST = "http://127.0.0.1:8000"


class TestResizeImageToThumbnailView:

    resize_image_to_thumbnail_view_endpoint = os.path.join(TEST_HOST, 'thumbnails')

    def test_post_valid_image(self, test_image_file):

        test_image_file.seek(0)

        response = requests.post(self.resize_image_to_thumbnail_view_endpoint, files={'image': test_image_file})

        assert response.status_code == 202
        assert 'Resized image URL' in response.json()

        image_name = response.json()['Resized image URL'].split('/')[-1]
        os.remove(image_name)

    def test_post_invalid_image(self):

        bad_file = BytesIO()

        response = requests.post(self.resize_image_to_thumbnail_view_endpoint, files={'image': bad_file})

        assert response.status_code == 400
        assert 'Error' in response.json()


class TestReturnThumbnailView:

    def test_request_valid_image(self):
        pass

    def test_request_invalid_image(self):
        pass
