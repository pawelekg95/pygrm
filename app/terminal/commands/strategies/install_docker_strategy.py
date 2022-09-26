"""
Install docker runner strategy
"""
import os
from typing import Union
from app.error.error import Error
from app.github.client import Client as GithubClient
from app.device.local import LocalClient
from app.device.remote import RemoteClient


class DockerStrategy:  # pylint: disable=too-few-public-methods
    """
    Strategy for installing github runner inside docker container
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
        Performs installation
        :param repo_name:
        :param runner_name:
        :return:
        """
        image_path = \
            os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))))) + \
            '/images/github-runner.dockerfile'
        error_code, token = self.github_client.registration_token(repo_name)
        if error_code != Error.OK:
            return error_code
        error_code, stdout, stderr = self.device_manager.build_docker_image(
            image_path,
            self.github_client.user,
            token,
            repo_name,
            repo_name + '_' + runner_name)
        print(stdout, '\n', stderr)
        return error_code
