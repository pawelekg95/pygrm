from getpass import getpass
from typing import List
from github.client import Client as GithubClient
from device.local import LocalClient
from device.remote import RemoteClient
from error import Error


def perform(github_client: GithubClient = None, repositories: List[str] = None) -> Error:
    if not repositories:
        print('No repositories')
    repo_name = input('For what repository? ')
    if repo_name not in [x.name for x in repositories]:
        print('No such repository. Run "repositories" command to list available projects')
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
    return device_manager.start_container(repo_name + '_' + runner_name)[0] if runner_type == 'docker' else \
        device_manager.start_github_service(repo_name + '_' + runner_name)[0]
