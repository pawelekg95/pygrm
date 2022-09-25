class Runner:
    def __init__(self,
                 name: str = '',
                 repository: str = '',
                 system: str = '',
                 arch: str = '',
                 online: bool = False,
                 as_docker: bool = False,
                 docker_enabled: bool = False,
                 docker_container_id: str = ''):
        self.name = name
        self.repository = repository
        self.system = system
        self.arch = arch
        self.online = online
        self.as_docker = as_docker
        self.docker_enabled = docker_enabled
        self.docker_container_id = docker_container_id
