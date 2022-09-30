"""
Remove runner command module
"""
from app.error.error import Error
from app.terminal.commands.icommand import ICommand


class RemoveCommand(ICommand):
    """
    Remove runner command
    """
    @classmethod
    def perform(cls, *_) -> Error:
        """
        To be implemented

        :param _:
        :return:
        """
        return Error.OK
