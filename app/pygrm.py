#!/bin/python3

import argparse
import sys

from github.client import Client as GithubClient
from terminal.interface import Interface


def parse_arguments(argv):
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

