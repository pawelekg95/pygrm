import paramiko
import scp
import os
from typing import Tuple
from error import Error


class RemoteClient:
    def __init__(self,
                 host: str = '',
                 user: str = '',
                 password: str = ''):
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
        stdin, stdout, stderr = self.ssh_client.exec_command('docker ps -q  --filter ancestor=' + image_name)
        if stdout.channel.recv_exit_status() != 0:
            return False
        return stdout.read().decode("utf-8").strip('\n') != ''

    def build_docker_image(self,
                           docker_file_path: str = '',
                           github_user: str = '',
                           github_token: str = '',
                           repository_name: str = '',
                           image_name: str = '',
                           additional_linux_packages: str = '',
                           additional_python_packages: str = '')\
            -> Tuple[Error, str, str]:
        self.scp_client.put(files=os.path.dirname(docker_file_path) + '/entrypoint.sh', remote_path='/tmp/entrypoint.sh')
        self.scp_client.put(files=docker_file_path, remote_path='/tmp/github-runner.dockerfile')
        stdin, stdout, stderr = self.ssh_client.exec_command(
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
        if self.__container_running(image_name):
            return Error.ALREADY, '', ''
        run_command = 'sudo docker run -d --restart unless-stopped --network host '
        stdin, stdout, stderr = self.ssh_client.exec_command(run_command + image_name)
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def stop_container(self,
                       image_name: str = '') -> Tuple[Error, str, str]:
        stdin, stdout, stderr = self.ssh_client.exec_command('sudo docker ps -a -q  --filter ancestor=' + image_name)
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), \
                   stderr.read().decode("utf-8")
        container_names = stdout.read().decode("utf-8").split('\n')
        stdin, stdout, stderr = self.ssh_client.exec_command('sudo docker update --restart no ' + ' '.join(container_names))
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"),\
                stderr.read().decode("utf-8")
        stdin, stdout, stderr = self.ssh_client.exec_command('sudo docker stop ' + ' '.join(container_names))
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def delete_image(self,
                     image_name: str = '') -> Tuple[Error, str, str]:
        stdin, stdout, stderr = self.ssh_client.exec_command('sudo docker image rm ' + image_name, get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def install_github_service(self,
                               github_user: str = '',
                               github_token: str = '',
                               repository_name: str = '',
                               runner_name: str = '',
                               dest_dir: str = '/home/github-runner') -> Tuple[Error, str, str]:
        architectures = {
            "amd64": "x64",
            "arm64": "arm64",
            "arm": "arm"
        }
        stdin, stdout, stderr = self.ssh_client.exec_command('dpkg --print-architecture')
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
        arch = architectures[stdout.read().decode("utf-8").strip('\n')]
        stdin, stdout, stderr = self.ssh_client.exec_command('sudo mkdir -p ' + dest_dir + '/' + runner_name)
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
        stdin, stdout, stderr = self.ssh_client.exec_command(
            'sudo curl -o ' + dest_dir + '/' + runner_name + '/actions-runner-linux-' + arch + '-2.296.1.tar.gz -L '
            '"https://github.com/actions/runner/releases/download/v2.296.1/actions-runner-linux-' + arch +
            '-2.296.1.tar.gz"', get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
        stdin, stdout, stderr = self.ssh_client.exec_command('sudo tar xzf ' + dest_dir + '/' + runner_name + '/actions-runner-linux-' +
                                                             arch + '-2.296.1.tar.gz -C ' + dest_dir, get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
        stdin, stdout, stderr = self.ssh_client.exec_command('sudo ' + dest_dir + '/' + runner_name + '/bin/installdependencies.sh', get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
        stdin, stdout, stderr = self.ssh_client.exec_command(
            'sudo RUNNER_ALLOW_RUNASROOT="1" ' + dest_dir + '/' + runner_name + './config.sh --unattended --url "https://github.com/' +
            github_user + '/' + repository_name + '" --token "' +
            github_token + '" --name "' + runner_name +
            '" --labels "shell_service"', get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        stdin, stdout, stderr = self.ssh_client.exec_command(
            'sudo RUNNER_ALLOW_RUNASROOT="1" ' + dest_dir + '/' + runner_name + './svc.sh install', get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def start_github_service(self,
                             runner_name: str = '',
                             service_dir: str = '/home/github-runner') -> Tuple[Error, str, str]:
        stdin, stdout, stderr = self.ssh_client.exec_command('sudo ' + service_dir + '/' + runner_name + '/svc.sh start')
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def stop_github_service(self,
                            runner_name: str = '',
                            service_dir: str = '/home/github-runner') -> Tuple[Error, str, str]:
        stdin, stdout, stderr = self.ssh_client.exec_command('sudo ' + service_dir + '/' + runner_name + '/svc.sh stop')
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
