"""
Remote device module
"""
import os
from typing import Tuple
import paramiko
import scp
from app.error.error import Error


class RemoteClient:
    """
    Class representing remote device. Provides methods to manage docker containers / images
    and github service on native system as systemd service
    """
    def __init__(self,
                 host: str = '',
                 user: str = '',
                 password: str = ''):
        """
        Constructor.
        Creates ssh and scp connection with host. Raises socket.error in case of failure.

        :param host: Host address/name
        :param user: User to log in - must be sudoer
        :param password: User password
        """
        self.host = host
        self.user = user
        self.password = password
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.host, username=self.user, password=self.password, timeout=15)
        self.scp_client = scp.SCPClient(self.ssh_client.get_transport())

    def __del__(self):
        self.scp_client.close()
        self.ssh_client.close()

    def __container_running(self, image_name: str = '') -> bool:
        """
        Checks if container based on provided image name is running

        :param image_name: Image name of the container
        :return: True if container is running, false otherwise
        """
        _, stdout, _ = self.ssh_client.exec_command(
            'docker ps -q  --filter ancestor=' + image_name)
        if stdout.channel.recv_exit_status() != 0:
            return False
        return stdout.read().decode("utf-8").strip('\n') != ''

    def cpu_architecture(self) -> Tuple[Error, str, str]:
        """
        Fetches information about device CPU architecture.
        :return: Error code, stdout and stderr strings
        """
        _, stdout, stderr = self.ssh_client.exec_command('dpkg --print-architecture')
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def build_docker_image(self,  # pylint: disable=too-many-arguments
                           docker_file_path: str = '',
                           github_user: str = '',
                           github_token: str = '',
                           repository_name: str = '',
                           image_name: str = '',
                           additional_linux_packages: str = '',
                           additional_python_packages: str = '')\
            -> Tuple[Error, str, str]:
        """
        Builds docker image.
        Copies dockerfile from path provided as an argument and an entrypoint
        from the same directory to the remote host's /tmp dir and builds docker image,
        naming it from concatenation of repository and image name.
        Github user name and token are required to build github runner inside the image.
        Passes additional linux and python packages to docker build context.

        :param docker_file_path: Local path to dockerfile.
        Entrypoint must be within the same directory.
        :param github_user: Github user name
        :param github_token: Private token of the user
        :param repository_name: Repository name to assign runner
        :param image_name: Image name
        :param additional_linux_packages: String with name of additional linux packages,
        comma seperated.
        :param additional_python_packages: String with name of additional python packages,
        comma seperated.
        :return: Error code, stdout and stderr strings
        """
        self.scp_client.put(files=os.path.dirname(docker_file_path) + '/entrypoint.sh',
                            remote_path='/tmp/entrypoint.sh')
        self.scp_client.put(files=docker_file_path,
                            remote_path='/tmp/github-runner.dockerfile')
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo docker build -t ' + image_name + ' -f /tmp/github-runner.dockerfile' +
            ' --build-arg REPOSITORY=' + repository_name + ' --build-arg GITHUB_TOKEN=' +
            github_token + ' --build-arg GITHUB_USER=' + github_user +
            ' --build-arg ADDITIONAL_PACKAGES=' + additional_linux_packages +
            ' --build-arg ADDITIONAL_PYTHON_PACKAGES=' + additional_python_packages +
            ' --build-arg RUNNER_NAME=' + image_name + ' /tmp', get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR,\
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def start_container(self,
                        image_name: str = '') -> Tuple[Error, str, str]:
        """
        Starts docker container.
        Container is set to be launched on boot and is started immediately.

        :param image_name: Image name on which container has to be created.
        :return: Error code, stdout and stderr strings
        """
        if self.__container_running(image_name):
            return Error.ALREADY, '', ''
        run_command = 'sudo docker run -d --restart unless-stopped --network host '
        _, stdout, stderr = self.ssh_client.exec_command(run_command + image_name)
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def stop_container(self,
                       image_name: str = '') -> Tuple[Error, str, str]:
        """
        Stops docker container.
        Updates container restart policy to 'no' and stops container immediately.

        :param image_name: Image name on which container was created.
        :return: Error code, stdout and stderr strings
        """
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo docker ps -a -q  --filter ancestor=' + image_name)
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), \
                   stderr.read().decode("utf-8")
        container_names = stdout.read().decode("utf-8").split('\n')
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo docker update --restart no ' + ' '.join(container_names))
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"),\
                stderr.read().decode("utf-8")
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo docker stop ' + ' '.join(container_names))
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def delete_image(self,
                     image_name: str = '') -> Tuple[Error, str, str]:
        """
        Deletes docker image.

        :param image_name: Image name to be deleted.
        :return: Error code, stdout and stderr strings
        """
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo docker image rm ' + image_name, get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def install_github_service(self,  # pylint: disable=too-many-arguments
                               github_user: str = '',
                               github_token: str = '',
                               repository_name: str = '',
                               runner_name: str = '',
                               dest_dir: str = '/home/github-runner') -> Tuple[Error, str, str]:
        """
        Installs github runner service.

        Downloads github runner package for host's architecture
        and installs it in the destination directory.
        After installing, registers new runner for the project.

        :param github_user: Github user name
        :param github_token: Private token of the user
        :param repository_name: Repository name to assign runner
        :param runner_name: Runner name
        :param dest_dir: Path where to download and install github runner
        :return: Error code, stdout and stderr strings
        """
        architectures = {
            "amd64": "x64",
            "arm64": "arm64",
            "arm": "arm"
        }
        error_code, stdout, stderr = self.cpu_architecture()
        if error_code != Error.OK:
            return error_code, stdout, stderr
        architecture = stdout.strip('\n')
        arch = architectures[architecture]
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo mkdir -p ' + dest_dir + '/' + runner_name)
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo curl -o ' + dest_dir + '/' + runner_name + '/actions-runner-linux-' +
            arch + '-2.296.1.tar.gz -L ' +
            '"https://github.com/actions/runner/releases/download/v2.296.1/actions-runner-linux-' +
            arch + '-2.296.1.tar.gz"', get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo tar xzf ' + dest_dir + '/' + runner_name + '/actions-runner-linux-' +
            arch + '-2.296.1.tar.gz -C ' + dest_dir, get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo ' + dest_dir + '/' + runner_name + '/bin/installdependencies.sh', get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo RUNNER_ALLOW_RUNASROOT="1" ' + dest_dir + '/' +
            runner_name + './config.sh --unattended --url "https://github.com/' +
            github_user + '/' + repository_name + '" --token "' +
            github_token + '" --name "' + runner_name +
            '" --labels "shell_service"', get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo RUNNER_ALLOW_RUNASROOT="1" ' + dest_dir + '/' +
            runner_name + './svc.sh install', get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def start_github_service(self,
                             runner_name: str = '',
                             service_dir: str = '/home/github-runner') -> Tuple[Error, str, str]:
        """
        Starts github runner service.

        Enables github runner service in systemd on the host.

        :param runner_name: Runner name.
        :param service_dir: Path where github runner is installed.
        :return: Error code, stdout and stderr strings
        """
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo ' + service_dir + '/' + runner_name + '/svc.sh start')
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def stop_github_service(self,
                            runner_name: str = '',
                            service_dir: str = '/home/github-runner') -> Tuple[Error, str, str]:
        """
        Stops github runner service.

        Stops github runner service in systemd.

        :param runner_name: Runner name.
        :param service_dir: Path where github runner is installed.
        :return: Error code, stdout and stderr strings
        """
        _, stdout, stderr = self.ssh_client.exec_command(
            'sudo ' + service_dir + '/' + runner_name + '/svc.sh stop')
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
