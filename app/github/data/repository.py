"""
Copyright (c) 2022 Pawel Gmurczyk

Repository module
"""


class Repository:  # pylint: disable=too-few-public-methods
    """
    Repository class
    """
    def __init__(self, name: str = ''):
        """
        Constructor
        :param name:
        """
        self.name = name
