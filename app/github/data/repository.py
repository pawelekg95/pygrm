"""
Repository module
"""


class Repository:  # pylint: disable=too-few-public-methods
    """
    Repository
    """
    def __init__(self, name: str = ''):
        """
        Constructor
        :param name: Repository name
        """
        self.name = name
