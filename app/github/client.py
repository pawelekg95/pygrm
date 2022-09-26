"""
Github client module.
"""
import json
from typing import List, Tuple
import requests

from app.github.data.repository import Repository
from app.github.data.runner import Runner
from app.error.error import Error


ARCHS_LABELS = ['X64', 'ARM64', 'ARM']
SERVICE_LABELS = ['docker_service', 'shell_service']


def _parse_repositories(repository_json: str = '')\
        -> Tuple[Error, List[Repository]]:
    """
    Parses response from github api repositories request
    :param repository_json:
    :return:
    """
    try:
        parsed_json = json.loads(repository_json)
    except json.JSONDecodeError:
        return Error.PARSE_ERROR, []
    token = []
    for repository_object in parsed_json:
        try:
            token.append(Repository(repository_object['name']))
        except KeyError:
            return Error.PARSE_ERROR, token
    return Error.OK, token


def _parse_runners(runners_json: str = '', repository: str = '')\
        -> Tuple[Error, List[Runner]]:
    """
    Parses response from github api runners request
    :param runners_json:
    :param repository:
    :return:
    """
    try:
        parsed_json = json.loads(runners_json)
    except json.JSONDecodeError:
        return Error.PARSE_ERROR, []
    token = []
    for runner_object in parsed_json["runners"]:
        try:
            arch = ''
            service_type = ''
            for label in runner_object['labels']:
                if label['name'] in ARCHS_LABELS:
                    arch = label['name']
                elif label['name'] in SERVICE_LABELS:
                    service_type = label['name']
            token.append(Runner(name=runner_object['name'],
                                system=runner_object["os"],
                                arch=arch,
                                online=runner_object['status'] == 'online',
                                repository=repository,
                                as_docker=service_type == SERVICE_LABELS[0]))
        except KeyError:
            return Error.PARSE_ERROR, token
    return Error.OK, token


def _parse_token(token_json: str = '')\
        -> Tuple[Error, str]:
    """
    Parses github api token request
    :param token_json:
    :return:
    """
    try:
        parsed_json = json.loads(token_json)
    except json.JSONDecodeError:
        return Error.PARSE_ERROR, ''
    return Error.OK, parsed_json['token']


class Client:
    """
    Github api client.
    """
    def __init__(self, user: str = '', auth_token: str = ''):
        """
        Constructor
        :param user:
        :param auth_token:
        """
        self.base_url = 'https://api.github.com'
        self.user = user
        self.auth_token = auth_token
        self.auth_header = {'Authorization': 'Bearer ' + self.auth_token}
        self.json_header = {'Accept': 'application/vnd.github+json'}
        self.content_header = {'Content-type': 'application/json'}

    def get_repositories(self) -> Tuple[Error, List[Repository]]:
        """
        Get user repositories
        :return:
        """
        repository_request = requests.get(self.base_url + '/user/repos',
                                          headers={**self.json_header,
                                                   **self.auth_header,
                                                   **self.content_header})
        if repository_request.status_code != 200:
            return Error.HTTP_ERROR, []
        return _parse_repositories(repository_request.text)

    def get_runners(self, repository: str = '') -> Tuple[Error, List[Runner]]:
        """
        Get self-hosted runners for repository
        :param repository:
        :return:
        """
        if not repository:
            return Error.EMPTY, []
        runners_request = requests.get(self.base_url + '/repos/' +
                                       self.user + '/' + repository +
                                       '/actions/runners',
                                       headers={**self.json_header,
                                                **self.auth_header,
                                                **self.content_header})
        if runners_request.status_code != 200:
            return Error.HTTP_ERROR, []
        return _parse_runners(runners_request.text, repository)

    def registration_token(self, repository: str = '') -> Tuple[Error, str]:
        """
        Get self-hosted github runner registration token
        :param repository:
        :return:
        """
        token_request = requests.post(self.base_url + '/repos/' +
                                      self.user + '/' + repository +
                                      '/actions/runners/registration-token',
                                      headers={**self.json_header,
                                               **self.auth_header,
                                               **self.content_header})
        if token_request.status_code != 201:
            return Error.HTTP_ERROR, ''
        return _parse_token(token_request.text)
