from typing import Callable, List
from error import Error, message
from .commands import install_runner, remove_runner, stop_runner, start_runner, list_runners
from github.client import Client as GithubClient


class Command:
    def __init__(self,
                 description: str = '', command: Callable[[GithubClient, List[str]], Error] = None):
        self.description = description
        self.command = command


class Interface:
    def __init__(self, github_client: GithubClient = None):
        self.running = True
        self.github_client = github_client
        error_code, self.repositories = github_client.get_repositories()
        if error_code != Error.OK:
            raise ConnectionError
        self.option_mapping = {
            'install': Command('Install new GitHub runner', install_runner.perform),
            'remove':  Command('Remove GitHub runner', remove_runner.perform),
            'stop': Command('Stop GitHub runner', stop_runner.perform),
            'start': Command('Start GitHub runner', start_runner.perform),
            'exit': Command('Quit PyGrm', self.stop),
            'help': Command('Print help', self.print_description),
            'runners': Command('List all runners', list_runners.perform),
            'repositories': Command('List repositories', self.list_repositories)
        }

        self.loop()

    def list_repositories(self, *_):
        for repository in self.repositories:
            print(repository.name)
        return Error.OK

    def print_description(self, *_):
        print('== PyGrm ==')
        for command_key, command in self.option_mapping.items():
            print(command_key, ' - ', command.description)
        return Error.OK

    def stop(self, *_):
        print('Stopping PyGrm')
        self.running = False
        return Error.OK

    def loop(self):
        self.print_description()
        while self.running:
            option = input('>>> ')
            if option not in self.option_mapping.keys():
                continue
            error_code = self.option_mapping[option].command(self.github_client, self.repositories)
            if error_code != Error.OK:
                print('Command failed, error=' + message(error_code))