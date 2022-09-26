"""
Install shell github runner strategy
"""
from typing import Union
from app.error.error import Error
from app.github.client import Client as GithubClient
from app.device.local import LocalClient
from app.device.remote import RemoteClient


class ShellStrategy:  # pylint: disable=too-few-public-methods
    """
    Shell strategy
    """
    def __init__(self,
                 device_manager: Union[LocalClient, RemoteClient] = None,
                 github_client: GithubClient = None):
        """
        Constructor
        :param device_manager:
        :param github_client:
        """
        self.device_manager = device_manager
        self.github_client = github_client

    def install(self,
                repo_name: str = '',
                runner_name: str = '') -> Error:
        """
        Perform installation
        :param repo_name:
        :param runner_name:
        :return:
        """
        error_code, token = self.github_client.registration_token(repo_name)
        if error_code != Error.OK:
            return error_code
        error_code, stdout, stderr = self.device_manager.install_github_service(
            self.github_client.user,
            token,
            repo_name,
            repo_name + '_' + runner_name)
        print(stdout, '\n', stderr)
        return error_code
