# PyGRM
## Python GitHub Runners Manager
### Utility to manage GitHub runners on local / remote hosts.
Copyright (c) 2022 Pawel Gmurczyk

Documentation:
* [Reference](https://pawelekg95.github.io/pygrm/)

# CI status
|                | Quality          | Deployment      |
| :------------: | :--------------: | :-------------: |
| ![linux_badge] | ![quality_badge] | ![deploy_badge] |

[linux_badge]: https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black
[quality_badge]: https://github.com/pawelekg95/pygrm/actions/workflows/quality.yml/badge.svg
[deploy_badge]: https://github.com/pawelekg95/pygrm/actions/workflows/deploy.yml/badge.svg

# Introduction

PyGRM is a simple command line application to manage GitHub runners.
Installing or removing them consists of few steps such as downloading GitHub runner package,
installing the service and registering it. PyGRM wraps them all and allows to do it for a local,
or remote host. GitHub related actions are performed via rest API using a private token.



While running takes input from the user and performs required commands.

Implemented commands:
* install runner
* start runner
* stop runner
* remove runner

# Requirements
* python3 >= 3.5 (reported by [Vermin](https://github.com/netromdk/vermin), Copyright (c) 2018 Morten Kristensen)
* Python packages:
  * requests
  * scp
  * paramiko
* For remote host:
  * SSH server running
  * user in sudoers group

# Run
1. Clone repository `git clone https://github.com/pawelekg95/pygrm.git`.
2. Run `./pygrm/app/pygrm.py -u <github_user> -t <private_token>`.
3. Type command to perform or `help` to print description.

##### Note: `<private_token` ought to have permissions to read and write user's repositories  
