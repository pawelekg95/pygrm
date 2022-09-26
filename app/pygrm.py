#!/bin/python3
""" PyGrm utility to easily manage github self-hosted runners """

import argparse
import sys
from typing import List

from github.client import Client as GithubClient
from terminal.interface import Interface


def parse_arguments(argv: List[str] = None):
    """
    Parses arguments
    :param argv: System arguments passed to PyGrm to be parsed
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='PyGrm. Python utility to manage github runners',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--token', dest='token', help='Private GitHub token', required=True)
    parser.add_argument('-u', '--user', dest='user', help='GitHub user', required=True)
    return parser.parse_args(args=argv)


if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    print('Fetching data...')
    github_client = GithubClient(user=args.user, auth_token=args.token)
    print('OK')
    interface = Interface(github_client)
