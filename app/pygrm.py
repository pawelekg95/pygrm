#!/bin/python3
"""
PyGrm - Python Github Runners Manager.

Utility to manage github self-hosted runners.
Provides possibility to install, remove, start and stop github runners as:
    - bare github service installed on the host [local / remote]
    - inside docker container
"""

import argparse
from typing import List
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.github.client import Client as GithubClient  # pylint: disable=wrong-import-position
from app.terminal.interface import Interface  # pylint: disable=wrong-import-position


def parse_arguments(argv: List[str] = None):
    """
    Parses arguments provided from command line

    :param argv: System arguments passed to PyGrm to be parsed
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='PyGrm. Python utility to manage github runners',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--token', dest='token',
                        help='Private GitHub token. Writing access required',
                        required=True)
    parser.add_argument('-u', '--user', dest='user', help='GitHub user', required=True)
    return parser.parse_args(args=argv)


if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    print('Fetching data...')
    github_client = GithubClient(user=args.user, auth_token=args.token)
    print('OK')
    interface = Interface(github_client)
