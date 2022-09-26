""" Start runner command module """
from getpass import getpass
from typing import List
from app.device.local import LocalClient
from app.device.remote import RemoteClient
from app.error.error import Error


def perform(_, repositories: List[str] = None) -> Error:
    """
    Start runner command
    :param _:
    :param repositories:
    :return:
    """
    if not repositories:
        print('No repositories')
    repo_name = input('For what repository? ')
    if repo_name not in [x.name for x in repositories]:
        print('No such repository. '
              'Run "repositories" command to list available projects')
        return Error.EMPTY
    runner_name = input('Runner name: ')
    destination = input('Install runner locally on remote host? [local / remote] ')
    if destination not in ['local', 'remote']:
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
    if runner_type not in ['shell', 'docker']:
        return Error.VALUE_ERROR
    return device_manager.start_container(repo_name + '_' + runner_name)[0]\
        if runner_type == 'docker'\
        else device_manager.start_github_service(repo_name + '_' + runner_name)[0]
