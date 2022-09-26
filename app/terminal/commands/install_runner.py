""" Install runner command module """
from getpass import getpass
from typing import List
from app.github.client import Client as GithubClient
from app.error.error import Error
from app.device.local import LocalClient
from app.device.remote import RemoteClient
from app.terminal.commands.strategies.install_shell_strategy import ShellStrategy
from app.terminal.commands.strategies.install_docker_strategy import DockerStrategy


DESTINATION = ['local', 'remote']
TYPE = ['shell', 'docker']


def perform(github_client: GithubClient = None,  # pylint: disable=too-many-return-statements
            repositories: List[str] = None) -> Error:
    """
    Installs new runner
    :param github_client:
    :param repositories:
    :return:
    """
    if not repositories:
        print('No repositories')
    repo_name = input('For what repository? ')
    if repo_name not in [x.name for x in repositories]:
        print('No such repository. Run "repositories" command to list available projects')
        return Error.EMPTY
    runner_name = input('Runner name: ')
    error_code, runners = github_client.get_runners(repo_name)
    if error_code != Error.OK:
        print('Failed to get runners')
        return error_code
    if repo_name + '_' + runner_name in [x.name for x in runners]:
        print('Runner with such name already exists.'
              'Run "runners" command to list already registered runner')
        return Error.VALUE_ERROR
    destination =\
        input('Install runner locally on remote host? [local / remote] ')
    if destination not in DESTINATION:
        print('Wrong option')
        return Error.VALUE_ERROR
    if destination == 'local':
        device_manager = LocalClient()
    else:
        host = input('Host: ')
        user = input('User: ')
        password = getpass()
        device_manager = RemoteClient(host=host, user=user, password=password)
    runner_type = input('What type of runner? [shell / docker] ')
    if runner_type not in TYPE:
        return Error.VALUE_ERROR
    install_strategy = ShellStrategy(device_manager, github_client) if runner_type == TYPE[0] \
        else DockerStrategy(device_manager, github_client)
    error_code = install_strategy.install(repo_name, runner_name)
    if error_code != Error.OK:
        return error_code
    launch = input('Runner installed correctly.'
                   'Do you want to launch it immediately? [yes / no] ')
    if launch not in ['yes', 'no']:
        return Error.VALUE_ERROR
    if launch == 'no':
        return Error.OK
    return device_manager.start_container(repo_name + '_' + runner_name)[0]\
        if runner_type == 'docker'\
        else device_manager.start_github_service(repo_name + '_' + runner_name)[0]
