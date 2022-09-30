"""
List runner command module
"""
from typing import List
from app.github.client import Client as GithubClient
from app.terminal.commands.icommand import ICommand, Error, Repository


class ListCommand(ICommand):
    """
    List command
    """
    @classmethod
    def perform(cls, github_client: GithubClient = None,
                repositories: List[Repository] = None) -> Error:
        """
        Lists all runners assigned to a particular user's repository
        and prints its' settings.

        :param github_client: Valid GithubClient initialized with private token and user name.
        :param repositories: User's repositories
        :return: Error code
        """
        if not repositories:
            print('No repositories')
        repo_name = input('For what repository? ')
        if repo_name not in [x.name for x in repositories]:
            print('No such repository')
            return Error.EMPTY
        error_code, runners = github_client.get_runners(repo_name)
        if error_code != Error.OK:
            print('Failed to get runners')
            return error_code
        if not runners:
            print('No runners registered for project')
        for runner in runners:
            print('Name:', runner.name, ', system:', runner.system,
                  ', architecture:', runner.arch, ', online:',
                  runner.online, ', repository:', runner.repository,
                  ', runs as docker service:', runner.as_docker,
                  ', docker enabled:', runner.docker_enabled)
        return Error.OK
