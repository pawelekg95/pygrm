from typing import Union
from error import Error
from github.client import Client as GithubClient
from device.local import LocalClient
from device.remote import RemoteClient


class ShellStrategy:
    def __init__(self,
                 device_manager: Union[LocalClient, RemoteClient] = None,
                 github_client: GithubClient = None):
        self.device_manager = device_manager
        self.github_client = github_client

    def install(self,
                repo_name: str = '',
                runner_name: str = '') -> Error:
        error_code, token = self.github_client.registration_token(repo_name)
        if error_code != Error.OK:
            return error_code
        error_code, stdout, stderr = self.device_manager.install_github_service(self.github_client.user,
                                                                                token,
                                                                                repo_name,
                                                                                repo_name + '_' + runner_name)
        print(stdout, '\n', stderr)
        return error_code


