"""
Command line interface module.

Provides classes to handle user input and perform particular commands.
"""
from typing import Callable, List
from app.error.error import Error, message
from app.github.client import Client as GithubClient
from app.github.data.repository import Repository
from .commands import install_runner, remove_runner, stop_runner, start_runner, list_runners


class Command:  # pylint: disable=too-few-public-methods
    """
    Command to perform.
    Contains callable function and its' description
    """
    def __init__(self,
                 description: str = '',
                 command: Callable[[GithubClient, List[Repository]], Error] = None):
        """
        Constructor.
        Takes description of the command and command itself as Callable
        that can take GithubClient object and list of repositories.

        :param description: Command description
        :param command:
        """
        self.description = description
        self.command = command


class Interface:
    """
    Interface class.
    Main loop of the application.
    Gets input from user and calls Commands stored as a map of command name and Command object.
    """
    def __init__(self, github_client: GithubClient = None):
        """
        Constructor.
        Initializes available commands and fetches repositories of the user logged in GithubClient.
        Starts main loop immediately.

        :param github_client: Valid GithubClient initialized with private token and user name.
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

    def list_repositories(self, *_) -> Error:
        """
        Lists all user's repositories

        :param _: Unused
        :return: Error code
        """
        for repository in self.repositories:
            print(repository.name)
        return Error.OK

    def print_description(self, *_) -> Error:
        """
        Prints description of available commands

        :param _: Unused
        :return: Error code
        """
        print('== PyGrm ==')
        for command_key, command in self.option_mapping.items():
            print(command_key, ' - ', command.description)
        return Error.OK

    def stop(self, *_) -> Error:
        """
        Stops whole pygrm

        :param _: Unused
        :return: Error code
        """
        print('Stopping PyGrm')
        self.running = False
        return Error.OK

    def loop(self) -> None:
        """
        Main loop.
        Takes input from user and calls corresponding Command object's callable method.
        In case of not existing command - continues,
        in case of command failure prints error message.

        :return: None
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
