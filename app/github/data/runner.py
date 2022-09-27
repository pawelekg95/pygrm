"""
Copyright (c) 2022 Pawel Gmurczyk

Runner module
"""


class Runner:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    Runner class
    """
    def __init__(self,  # pylint: disable=too-many-arguments
                 name: str = '',
                 repository: str = '',
                 system: str = '',
                 arch: str = '',
                 online: bool = False,
                 as_docker: bool = False,
                 docker_enabled: bool = False,
                 docker_container_id: str = ''):
        """
        Constructor
        :param name:
        :param repository:
        :param system:
        :param arch:
        :param online:
        :param as_docker:
        :param docker_enabled:
        :param docker_container_id:
        """
        self.name = name
        self.repository = repository
        self.system = system
        self.arch = arch
        self.online = online
        self.as_docker = as_docker
        self.docker_enabled = docker_enabled
        self.docker_container_id = docker_container_id
