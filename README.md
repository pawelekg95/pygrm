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
installing the service and registering it. PyGRM wraps them all and allows to do it on a local,
or remote host. GitHub related actions are performed via rest API using a private token.

### Shell

Shell runners are just simply installed on the host's native system. GitHub runner package is being downloaded,
unpacked and installed as systemd service.

### Docker

Launching runner on system boot is possible via systemd which is not supported by docker containers.
Due to that it is not possible to install GitHub runner service.
Nonetheless, PyGRM allows configuring it inside docker image and launching it with custom entrypoint script on container creation.
Container itself is set to be automatically relaunched.

See dockerfiles inside `images` directory to 

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

# Run
1. Clone repository `git clone https://github.com/pawelekg95/pygrm.git`.
2. Run `./pygrm/app/pygrm.py -u <github_user> -t <private_token>`.
3. Type command to perform or `help` to print description.

##### Note: `<private_token` ought to have permissions to read and write user's repositories
