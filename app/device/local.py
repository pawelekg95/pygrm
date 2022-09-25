import subprocess
from typing import Tuple
from error import Error


class LocalClient:

    def build_docker_image(self, docker_file_path='', github_user='', github_token='', repository_name='',
                           image_name='', additional_linux_packages='', additional_python_packages='') \
            -> Tuple[Error, str, str, str]:
        stdin, stdout, stderr = self.ssh_client.exec_command(
            'docker build -t ' + image_name + ' -f ' + docker_file_path +
            ' --build-arg REPOSITORY=' + repository_name + ' --build-arg GITHUB_TOKEN=' +
            github_token + ' --build-arg GITHUB_USER=' + github_user +
            ' --build-arg ADDITIONAL_PACKAGES=' + additional_linux_packages +
            ' --build-arg ADDITIONAL_PYTHON_PACKAGES=' + additional_python_packages +
            ' --build-arg RUNNER_NAME=' + image_name + ' /tmp/')
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, stdin.read().decode("utf-8"), \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def start_container(self, image_name='', permanently=False) -> Tuple[Error, str, str, str]:
        run_command = 'docker run ' if not permanently else 'docker run -d --restart unless-stopped '
        stdin, stdout, stderr = self.ssh_client.exec_command(run_command + image_name)
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, stdin.read().decode("utf-8"), \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def stop_container(self, image_name='') -> Tuple[Error, str, str, str]:
        stdin, stdout, stderr = self.ssh_client.exec_command('docker update --restart unless-stopped ' + image_name)
        if stdout.channel.recv_exit_status() != 0:
            return Error.SSH_ERROR, stdin.read().decode("utf-8"), stdout.read().decode("utf-8"), \
                   stderr.read().decode("utf-8")
        stdin, stdout, stderr = self.ssh_client.exec_command('docker stop ' + image_name)
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, stdin.read().decode("utf-8"), \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def delete_image(self, image_name='') -> Tuple[Error, str, str, str]:
        stdin, stdout, stderr = self.ssh_client.exec_command('docker image rm ' + image_name)
        return Error.OK if stdout.channel.recv_exit_status() == 0 else Error.SSH_ERROR, stdin.read().decode("utf-8"), \
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
