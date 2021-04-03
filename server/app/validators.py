import imghdr
from typing import Tuple

from starlette.datastructures import UploadFile


def is_valid_image(image_file: UploadFile, image_filename: str, valid_image_extensions: Tuple[str]):

    def is_valid_image_filename(filename, valid_extensions):
        return filename.lower().endswith(valid_extensions)

    def is_valid_image_file_format(file, valid_extensions):
        return '.' + imghdr.what(file) in valid_extensions

    def is_filename_extension_file_format_match(filename, file):
        filename_extension = filename.lower().split('.')[-1]
        filename_extension = 'jpeg' if filename_extension == 'jpg' else filename_extension  # potential conversion to match imghdr jpeg identification
        return imghdr.what(file) == filename_extension

    return is_valid_image_filename(image_filename, valid_image_extensions) \
           and is_valid_image_file_format(image_file, valid_image_extensions) \
           and is_filename_extension_file_format_match(image_filename, image_file)
