"""
Install runner command module
"""
from typing import List
import os
from app.github.client import Client as GithubClient
from app.github.data.repository import Repository
from app.error.error import Error
from app.terminal.commands.additional_information import Type
from app.terminal.commands.icommand import ICommand


class InstallCommand(ICommand):
    """
    Install command.
    """
    def perform(self, github_client: GithubClient = None,  # pylint: disable=too-many-return-statements
                repositories: List[Repository] = None) -> Error:
        """
        Installs new runner.
        The most safe and preferable way of launching any CI jobs is an isolated environment,
        such as docker container. Unfortunately, docker containers does not allow of systemd usage
        on which github runner service is based. To overcome this limitation PyGrm provides
        dockerfile to build images with special entrypoint, that manually launches github runner
        on container creation.
        It also allows to provide additional apt and python packages to make images more adjusted
        to particular projects.
        [ TO BE DONE ] Extend install command to get from user optional, additional packages.
        Native, straight forward github service installation on the host is available as well.

        :param github_client: Valid GithubClient initialized with private token and user name.
        :param repositories: User's repositories
        :return: Error code
        """
        self.init_perform(repositories)
        error_code, runners = github_client.get_runners(self.additional_info.repository)
        if error_code != Error.OK:
            print('Failed to get runners')
            return error_code
        if self.additional_info.repository + '_' + self.additional_info.runner \
                in [x.name for x in runners]:
            print('Runner with such name already exists.'
                  'Run "runners" command to list already registered runner')
            return Error.VALUE_ERROR
        error_code, token = github_client.registration_token(
            self.additional_info.repository
        )
        if error_code != Error.OK:
            return error_code
        if self.additional_info.runner_type == Type.SHELL:
            error_code, stdout, stderr = self.device_manager.install_github_service(
                github_client.user,
                token,
                self.additional_info.repository,
                self.additional_info.repository + '_' + self.additional_info.runner)
        else:
            error_code, cpu_arch, _ = self.device_manager.cpu_architecture()
            if error_code != Error.OK:
                return error_code
            default_image = input('Use default image? [yes / no] ')
            if default_image not in ['yes', 'no']:
                return Error.VALUE_ERROR
            image_path = \
                os.path.dirname(os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__))))) + \
                '/images/github-runner_' + cpu_arch.strip('\n') + '.dockerfile' \
                if default_image == 'yes' \
                else input('Image path: ')
            error_code, stdout, stderr = self.device_manager.build_docker_image(
                image_path,
                github_client.user,
                token,
                self.additional_info.repository,
                self.additional_info.repository + '_' + self.additional_info.runner)
        print(stdout, '\n', stderr)
        if error_code != Error.OK:
            return error_code
        launch = input('Runner installed correctly.'
                       'Do you want to launch it immediately? [yes / no] ')
        if launch not in ['yes', 'no']:
            return Error.VALUE_ERROR
        if launch == 'no':
            return Error.OK
        return self.device_manager.start_container(
            self.additional_info.repository + '_' + self.additional_info.runner)[0]\
            if self.additional_info.runner_type == Type.DOCKER\
            else self.device_manager.start_github_service(
                self.additional_info.repository + '_' + self.additional_info.runner)[0]
