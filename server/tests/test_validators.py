from io import BytesIO

from server.validators import is_valid_image


VALID_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')


class TestIsValidImage:

    def test_is_valid_image(self, test_image_file):

        test_image_file.seek(0)

        assert is_valid_image(test_image_file, test_image_file.name, VALID_IMAGE_EXTENSIONS)

        test_image_file.close()

    def test_invalid_filename_extension(self, test_image_file):

        test_image_file.name = 'test.bad_extension'

        assert not is_valid_image(test_image_file, test_image_file.name, VALID_IMAGE_EXTENSIONS)

        test_image_file.close()

    def test_invalid_file_format(self):

        invalid_file = BytesIO()
        invalid_file.seek(0)

        assert not is_valid_image(invalid_file, 'test', VALID_IMAGE_EXTENSIONS)

        invalid_file.close()

    def test_invalid_filename_extension_file_format_match(self, test_image_file):

        test_image_file.name = 'test.jpg'
        test_image_file.seek(0)

        assert not is_valid_image(test_image_file, test_image_file.name, VALID_IMAGE_EXTENSIONS)

        test_image_file.close()
