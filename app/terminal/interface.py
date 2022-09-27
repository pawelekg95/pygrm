"""
Copyright (c) 2022 Pawel Gmurczyk

Command line interface module
"""
from typing import Callable, List
from app.error.error import Error, message
from app.github.client import Client as GithubClient
from .commands import install_runner, remove_runner, stop_runner, start_runner, list_runners


class Command:  # pylint: disable=too-few-public-methods
    """
    Command abstraction class. Contains callable function and its' description
    """
    def __init__(self,
                 description: str = '', command: Callable[[GithubClient, List[str]], Error] = None):
        self.description = description
        self.command = command


class Interface:
    """
    Interface class
    """
    def __init__(self, github_client: GithubClient = None):
        """
        Constructor
        :param github_client: Initialized Github client to be used
        """
        self.running = True
        self.github_client = github_client
        error_code, self.repositories = github_client.get_repositories()
        if error_code != Error.OK:
            raise ConnectionError
        self.option_mapping = {
            'install': Command('Install new GitHub runner',
                               install_runner.InstallCommand().perform),
            'remove':  Command('Remove GitHub runner', remove_runner.RemoveCommand().perform),
            'stop': Command('Stop GitHub runner', stop_runner.StopCommand().perform),
            'start': Command('Start GitHub runner', start_runner.StartCommand().perform),
            'exit': Command('Quit PyGrm', self.stop),
            'help': Command('Print help', self.print_description),
            'runners': Command('List all runners', list_runners.ListCommand().perform),
            'repositories': Command('List repositories', self.list_repositories)
        }

        self.loop()

    def list_repositories(self, *_):
        """
        Lists all repositories of user
        :param _:
        :return:
        """
        for repository in self.repositories:
            print(repository.name)
        return Error.OK

    def print_description(self, *_):
        """
        Prints description
        :param _:
        :return:
        """
        print('== PyGrm ==')
        for command_key, command in self.option_mapping.items():
            print(command_key, ' - ', command.description)
        return Error.OK

    def stop(self, *_):
        """
        Stop pygrm
        :param _:
        :return:
        """
        print('Stopping PyGrm')
        self.running = False
        return Error.OK

    def loop(self):
        """
        Main loop
        :return:
        """
        self.print_description()
        while self.running:
            option = input('>>> ')
            if option not in self.option_mapping.keys():  # pylint: disable=consider-iterating-dictionary
                continue
            error_code = self.option_mapping[option].command(
                self.github_client, self.repositories)
            if error_code != Error.OK:
                print('Command failed, error=' + message(error_code))
