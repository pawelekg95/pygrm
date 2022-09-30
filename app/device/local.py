"""
Module that provides abstraction layer for local device
"""
from typing import Tuple
from app.error.error import Error


class LocalClient:
    """
    Class representing local device. Provides methods to manage docker containers / images
    and github service on native system as systemd service
    """

    # @classmethod
    # def __container_running(cls, *_) -> bool:
    #     """
    #     Checks if docker container is already running
    #     :param image_name: Image name
    #     :return: True if docker container is running, False otherwise
    #     """
    #     return False

    @classmethod
    def build_docker_image(cls, *_) \
            -> Tuple[Error, str, str]:
        """
        To be implemented
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def start_container(cls, *_) -> Tuple[Error, str, str]:
        """
        To be implemented
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def stop_container(cls, *_) -> Tuple[Error, str, str]:
        """
        To be implemented
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def delete_image(cls, *_) -> Tuple[Error, str, str]:
        """
        To be implemented
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def install_github_service(cls, *_) -> Tuple[Error, str, str]:
        """
        To be implemented
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def start_github_service(cls, *_) -> Tuple[Error, str, str]:
        """
        To be implemented
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def stop_github_service(cls, *_) -> Tuple[Error, str, str]:
        """
        To be implemented
        :param _:
        :return:
        """
        return Error.OK, '', ''
