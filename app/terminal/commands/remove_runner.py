"""
Remove runner command module
"""
from typing import List
from app.error.error import Error
from app.terminal.commands.icommand import ICommand
from app.github.client import Client as GithubClient
from app.github.data.repository import Repository


class RemoveCommand(ICommand):
    """
    Remove runner command
    """
    def perform(self, github_client: GithubClient = None,
                repositories: List[Repository] = None) -> Error:
        """

        :param github_client:
        :param repositories:
        :return:
        """
        self.init_perform(repositories)
        error_code, runners = github_client.get_runners(self.additional_info.repository)
        if error_code != Error.OK:
            print('Failed to get runners')
            return error_code
        if self.additional_info.repository + '_' + self.additional_info.runner \
                not in [x.name for x in runners]:
            print('Runner with such name already exists.'
                  'Run "runners" command to list already registered runner')
            return Error.VALUE_ERROR
        return Error.OK
