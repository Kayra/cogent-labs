import imghdr
from typing import List

from starlette.datastructures import UploadFile


def is_valid_image(image: UploadFile, valid_image_extensions: List[str]):

    def is_valid_image_filename(image_filename, valid_extensions):
        return image_filename.lower().endswith(valid_extensions)

    def is_valid_image_file_format(file, valid_extensions):
        return '.' + imghdr.what(file) in valid_extensions

    def is_filename_extension_file_format_match(filename, file):
        filename_extension = filename.lower().split('.')[-1]
        filename_extension = 'jpeg' if filename_extension == 'jpg' else filename_extension  # potential conversion to match imghdr jpeg identification
        return imghdr.what(file) == filename_extension

    return is_valid_image_filename(image.filename, valid_image_extensions) \
           and is_valid_image_file_format(image.file, valid_image_extensions) \
           and is_filename_extension_file_format_match(image.filename, image.file)
