"""
Base class of other command classes
"""
from typing import List
from app.terminal.commands.additional_information import AdditionalInfo, Destination
from app.terminal.commands import common_parts
from app.error.error import Error
from app.device.local import LocalClient
from app.device.remote import RemoteClient
from app.github.data.repository import Repository


class ICommand:  # pylint: disable=too-few-public-methods
    """
    Base class for other commands.
    Takes base input from user, such as destination host and runner type.
    """
    def __init__(self, github_user: str = ''):
        """
        Constructor
        """
        self.additional_info = AdditionalInfo()
        self.additional_info.github_user = github_user
        self.device_manager = None

    def init_perform(self, repositories: List[Repository] = None) -> Error:
        """
        Initial command to perform. Gathers basic information from user and stores it
        as AdditionalInfo object, accessible for descendants. Also, does very basic verification.
        :param repositories: User's repositories
        :return: Error code
        """
        if not repositories:
            print('No repositories')
        error_code = common_parts.base_information(self.additional_info)
        if error_code != Error.OK:
            print('Failed to get base info')
            return error_code
        if self.additional_info.repository not in [x.name for x in repositories]:
            print('No such repository. '
                  'Run "repositories" command to list available projects')
            return Error.EMPTY
        error_code = common_parts.destination_information(self.additional_info)
        if error_code != Error.OK:
            print('Failed to get destination info')
            return error_code
        error_code = common_parts.runner_type_information(self.additional_info)
        if error_code != Error.OK:
            print('Failed to get runner type info')
            return error_code
        if self.additional_info.destination == Destination.LOCAL:
            self.device_manager = LocalClient()
        else:
            self.device_manager = RemoteClient(
                host=self.additional_info.hostname,
                user=self.additional_info.host_user,
                password=self.additional_info.host_password)
        return Error.OK
