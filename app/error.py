from enum import Enum


class Error(Enum):
    OK = 0
    PARSE_ERROR = 1
    HTTP_ERROR = 2
    EMPTY = 3
    VALUE_ERROR = 4
    SSH_ERROR = 5
    ALREADY = 6


def message(error: Error = None) -> str:
    if error == Error.OK:
        return 'Ok'
    elif error == Error.PARSE_ERROR:
        return 'Parse error'
    elif error == Error.HTTP_ERROR:
        return 'HTTP error'
    elif error == Error.EMPTY:
        return 'Empty value'
    elif error == Error.VALUE_ERROR:
        return 'Wrong value'
    elif error == Error.SSH_ERROR:
        return 'SSH error'
    elif error == Error.ALREADY:
        return 'Already existing / running'
    else:
        return 'Unknown error'
