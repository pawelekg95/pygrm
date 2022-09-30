"""
Provides functions to get some all-commands-wide information.
"""
from getpass import getpass
from app.terminal.commands.additional_information import AdditionalInfo, Destination, Type
from app.error.error import Error


def base_information(token: AdditionalInfo = None) -> Error:
    """
    Gets repository and runner name from user
    :param token: AdditionalInfo object to be filled
    :return: Error code
    """
    if not AdditionalInfo:
        return Error.EMPTY
    repo_name = input('For what repository? ')
    token.repository = repo_name
    runner_name = input('Runner name: ')
    token.runner = runner_name
    return Error.OK


def destination_information(token: AdditionalInfo = None) -> Error:
    """
    Gets destination host information from user
    :param token: AdditionalInfo object to be filled
    :return: Error code
    """
    if not AdditionalInfo:
        return Error.EMPTY
    destination = input('Destination of the runner [local / remote]: ')
    if destination not in ['local', 'remote']:
        return Error.VALUE_ERROR
    if destination == 'local':
        token.destination = Destination.LOCAL
        return Error.OK
    token.destination = Destination.REMOTE
    host = input('Host: ')
    user = input('User: ')
    password = getpass()
    token.hostname = host
    token.host_user = user
    token.host_password = password
    return Error.OK


def runner_type_information(token: AdditionalInfo = None) -> Error:
    """
    Gets runner type information from user
    :param token: AdditionalInfo object to be filled
    :return: Error code
    """
    if not AdditionalInfo:
        return Error.EMPTY
    runner_type = input('What type of runner? [shell / docker] ')
    if runner_type not in ['shell', 'docker']:
        return Error.VALUE_ERROR
    token.runner_type = Type.SHELL if runner_type == 'shell'\
        else Type.DOCKER
    return Error.OK
