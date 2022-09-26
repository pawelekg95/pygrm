""" Remove runner command module """
from app.error.error import Error


def perform(*_) -> Error:
    """
    :param _:
    :return:
    """
    return Error.OK
