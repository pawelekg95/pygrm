"""
Copyright (c) 2022 Pawel Gmurczyk

Stop runner command module
"""
from typing import List
from app.error.error import Error
from app.terminal.commands.additional_information import Type
from app.terminal.commands.icommand import ICommand


class StopCommand(ICommand):
    """
    Stop runner command
    """
    def perform(self, _, repositories: List[str] = None) -> Error:
        """
        Stop runner
        :param _: Unused
        :param repositories:
        :return:
        """
        self.init_perform(repositories)
        return self.device_manager.stop_container(
            self.additional_info.repository + '_' + self.additional_info.runner)[0] \
            if self.additional_info.runner_type == Type.DOCKER \
            else self.device_manager.stop_github_service(
            self.additional_info.repository + '_' + self.additional_info.runner)[0]
