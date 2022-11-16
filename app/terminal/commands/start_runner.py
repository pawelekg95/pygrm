"""
Start runner command module
"""
from typing import List
from app.terminal.commands.icommand import ICommand, Error, Repository
from app.terminal.commands.additional_information import Type


class StartCommand(ICommand):
    """
    Start runner command
    """
    def perform(self, _, repositories: List[Repository] = None) -> Error:
        """
        Starts github runner.
        Shell runners are systemd services and that's how they are started.
        Docker doesn't support systemd. That is why images are having special entrypoint
        to launch github runner explicitly as a normal process.
        Containers are being launched and set to auto launch on boot.

        :param _: Unused
        :param repositories: User's repositories
        :return: Error code
        """
        self.init_perform(repositories)
        docker_inside_docker = 'no'
        if self.additional_info.runner_type == Type.DOCKER:
            docker_inside_docker = input('Allow docker inside container? [yes / no] ').lower()
        return self.device_manager.start_container(
            self.additional_info.repository + '_' + self.additional_info.runner,
            docker_inside_docker == 'yes')[0] \
            if self.additional_info.runner_type == Type.DOCKER \
            else self.device_manager.start_github_service(self.additional_info.github_user,
                    self.additional_info.repository, self.additional_info.runner)[0]
