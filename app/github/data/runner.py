"""
Runner module
"""


class Runner:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    Runner.
    Contains information about system, architecture and runner type.
    """
    def __init__(self,  # pylint: disable=too-many-arguments
                 name: str = '',
                 repository: str = '',
                 system: str = '',
                 arch: str = '',
                 online: bool = False,
                 as_docker: bool = False,
                 docker_enabled: bool = False):
        """
        Constructor.

        :param name: Runner name
        :param repository: Project to which runner is bound
        :param system: OS of the runner
        :param arch: Runner's CPU architecture
        :param online: Indicates whether runner is online
        :param as_docker: Indicates whether runner is docker type
        :param docker_enabled: Indicates whether runner allows docker operations on it.
        """
        self.name = name
        self.repository = repository
        self.system = system
        self.arch = arch
        self.online = online
        self.as_docker = as_docker
        self.docker_enabled = docker_enabled
