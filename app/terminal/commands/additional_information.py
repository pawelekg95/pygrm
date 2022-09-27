"""
Copyright (c) 2022 Pawel Gmurczyk

Module for querying additional information from user
"""
from enum import Enum


class Destination(Enum):
    """
    Destination of the runner
    """
    REMOTE = 0
    LOCAL = 1


class Type(Enum):
    """
    Runner type
    """
    SHELL = 0
    DOCKER = 1


class AdditionalInfo:  # pylint: disable=too-few-public-methods
    """
    Additional information from user
    """
    def __init__(self):
        self.destination = Destination.LOCAL
        self.hostname = ''
        self.host_user = ''
        self.host_password = ''
        self.repository = ''
        self.runner = ''
        self.runner_type = Type.DOCKER
