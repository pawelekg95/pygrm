from typing import List
from github.client import Client as GithubClient
from error import Error


def perform(github_client: GithubClient = None, repositories: List[str] = None) -> Error:
    return Error.OK
