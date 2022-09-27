"""
Copyright (c) 2022 Pawel Gmurczyk

Module that provides abstraction layer for local device
"""
from typing import Tuple
from app.error.error import Error


class LocalClient:
    """
    Abstraction to represent local device
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
        Build docker image
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def start_container(cls, *_) -> Tuple[Error, str, str]:
        """
        Start docker container from image name
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def stop_container(cls, *_) -> Tuple[Error, str, str]:
        """
        Stop container started upon image name
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def delete_image(cls, *_) -> Tuple[Error, str, str]:
        """
        Delete image
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def install_github_service(cls, *_) -> Tuple[Error, str, str]:
        """
        Install github runner as a service
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def start_github_service(cls, *_) -> Tuple[Error, str, str]:
        """
        Start github runner service
        :param _:
        :return:
        """
        return Error.OK, '', ''

    @classmethod
    def stop_github_service(cls, *_) -> Tuple[Error, str, str]:
        """
        Stop github runner service
        :param _:
        :return:
        """
        return Error.OK, '', ''
