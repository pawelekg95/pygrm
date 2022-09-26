""" List runner command module """
from typing import List
from app.github.client import Client as GithubClient
from app.error.error import Error


def perform(github_client: GithubClient = None,
            repositories: List[str] = None) -> Error:
    """
    Lists runners
    :param github_client:
    :param repositories:
    :return:
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
              ', docker enabled:', runner.docker_enabled, ', container id:',
              runner.docker_container_id if runner.as_docker else 'None')
    return Error.OK
