"""
Stop runner command module
"""
from typing import List
from app.terminal.commands.icommand import ICommand, Error, Repository
from app.terminal.commands.additional_information import Type


class StopCommand(ICommand):
    """
    Stop runner command.
    """
    def perform(self, _, repositories: List[Repository] = None) -> Error:
        """
        Stops github runner.
        For native (shell) runners stops service in systemd
        using script provided from Github runner package.
        Docker runners are being forbidden from auto launching on boot and stopped immediately.

        :param _: Unused
        :param repositories: User's repositories
        :return: Error code
        """
        self.init_perform(repositories)
        return self.device_manager.stop_container(
            self.additional_info.repository + '_' + self.additional_info.runner)[0] \
            if self.additional_info.runner_type == Type.DOCKER \
            else self.device_manager.stop_github_service(
            self.additional_info.repository + '_' + self.additional_info.runner)[0]
