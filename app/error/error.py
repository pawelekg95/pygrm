""" Error module. Provides all error codes and message casting """
from enum import Enum


class Error(Enum):
    """
    Error codes used in PyGrm
    """
    OK = 0
    PARSE_ERROR = 1
    HTTP_ERROR = 2
    EMPTY = 3
    VALUE_ERROR = 4
    SSH_ERROR = 5
    ALREADY = 6


_MESSAGES = {
    Error.OK: 'Ok',
    Error.PARSE_ERROR: 'Parse error',
    Error.HTTP_ERROR: 'HTTP error',
    Error.EMPTY: 'Empty value',
    Error.VALUE_ERROR: 'Wrong value',
    Error.SSH_ERROR: 'SSH error',
    Error.ALREADY: 'Already existing / running'
}


def message(error: Error = None) -> str:
    """
    Casts error codes to description message
    :param error: Error code
    :return: Description message
    """
    for error_code, description in _MESSAGES.items():
        if error_code == error:
            return description
    return 'Unknown error'
