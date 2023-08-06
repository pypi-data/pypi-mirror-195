"""
This file is for customizing errors and anything related to errors
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from file_validator.constants import DEFAULT_ERROR_MESSAGE, DEFAULT_FILE_NAME

try:
    # Get Error Message From Django Setting
    CUSTOM_ERROR_MESSAGE = settings.FILE_VALIDATOR_ERROR_MESSAGE
except (AttributeError, ImproperlyConfigured):
    CUSTOM_ERROR_MESSAGE = DEFAULT_ERROR_MESSAGE


class FileValidationException(Exception):
    """Raised when file is not valid"""


class SizeValidationException(Exception):
    """Raised when file size is not valid"""


class DjangoFileValidationException(Exception):
    """Raised when file validation operation for django fails"""


class LibraryNotSupportedException(Exception):
    """Raised when a library is not supported"""


class MimesEmptyException(Exception):
    """Raised when the mime list is empty"""


class TypeNotSupportedException(Exception):
    """
    Raised when the type not supported,
    supported types: image, audio, video, archive, font
    """


def error_message(
    mimes=None,
    file_size=None,
    max_file_size=None,
    message=CUSTOM_ERROR_MESSAGE,
    file_name=DEFAULT_FILE_NAME,
    **kwargs
) -> str:
    """
    :type file_name: str
    :param file_name: Returns the name of the file to be validated
    :type mimes: list
    :param mimes: It returns the mimes on which the file is to be validated
    :type file_size: str
    :param file_size: It returns the file size on which the file is to be validated
    :type max_file_size: str
    :param max_file_size: Returns the maximum file size to be validated and the user can upload,
        If you have not confirmed the file size, it will return 0 by default
    :param message: The error message to be shown to the user when the file is not valid
    :return: return your error message or default error message
    """
    file_mimes = ""
    current_file_mime = kwargs.get("current_file_mime")
    if mimes is not None:
        for mime in mimes:
            if mime == mimes[-1]:
                file_mimes += str(mime)
            else:
                file_mimes += str(mime)
                file_mimes += ", "

    return message.format(
        mimes=file_mimes,
        file_size=file_size,
        max_file_size=max_file_size,
        file_name=file_name,
        current_file_mime=current_file_mime,
    )
