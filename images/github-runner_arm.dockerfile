FROM debian:bullseye-slim
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG DEBIAN_FRONTEND=noninteractive
ARG GITHUB_RUNNER_URL="https://github.com/actions/runner/releases/download/v2.296.1/actions-runner-linux-arm-2.296.1.tar.gz"

# Required arguments
ARG REPOSITORY
ARG GITHUB_TOKEN
ARG GITHUB_USER
ARG RUNNER_NAME

# Optional arguments
ARG ADDITIONAL_PACKAGES
ARG ADDITIONAL_PYTHON_PACKAGES

ENV RUNNER_ALLOW_RUNASROOT="1"

WORKDIR /root

# Install base packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential=12.9 g++=4:10.2.1-1 llvm=1:11.0-51+nmu5 \
    python3=3.9.2-3 python3-pip=20.3.4-4+deb11u1 shellcheck=0.7.1-1+deb11u1 git=1:2.30.2-1 make=4.3-4.1 \
    clang-format=1:11.0-51+nmu5 clang-tidy=1:11.0-51+nmu5 wget=1.21-1+deb11u1 xz-utils=5.2.5-2.1~deb11u1 valgrind=1:3.16.1-1 \
    lcov=1.14-2 libgpgme-dev=1.14.0-1 ca-certificates=20210119 curl=7.74.0-1.3+deb11u3 gnupg=2.2.27-2+deb11u2 \
    lsb-release=11.1.0 dpkg=1.20.12 diffutils=1:3.7-5 cmake=3.18.4-2+deb11u1 && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download GitHub runner
RUN mkdir actions-runner
WORKDIR /root/actions-runner
RUN curl -o "actions-runner-linux-arm-2.296.1.tar.gz" -L "${GITHUB_RUNNER_URL}" && \
    tar xzf "./actions-runner-linux-arm-2.296.1.tar.gz"

# Install GitHub runner
RUN ./bin/installdependencies.sh && \
    RUNNER_ALLOW_RUNASROOT="1" /root/actions-runner/config.sh --unattended \
    --url "https://github.com/${GITHUB_USER}/${REPOSITORY}" --token "${GITHUB_TOKEN}" --name "${RUNNER_NAME}" --labels "docker_service"

# Import docker repository
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install docker
RUN apt-get update && \
    apt-get install -y --no-install-recommends docker-ce=5:20.10.18~3-0~ubuntu-focal docker-ce-cli=5:20.10.18~3-0~ubuntu-focal \
    containerd.io=1.6.8-1 docker-compose-plugin=2.10.2~ubuntu-focal && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install additional packages
# hadolint ignore=DL3008
RUN apt-get update && \
    IFS=',' read -ra PACKAGES <<< "${ADDITIONAL_PACKAGES}" && \
    if (( ${#PACKAGES[@]} != 0 )); then apt-get install --no-install-recommends -y "${PACKAGES[@]}"; fi && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install base python packages
RUN pip3 --no-cache-dir install requests==2.28.1 telnetlib3==1.0.4 pyserial==3.5 pylint==2.15.3 xmlrunner==1.7.7 \
    pandas==1.5.0 scipy==1.9.1 numpy==1.23.3 pdoc3==0.10.0 scp==0.14.4 paramiko==2.11.0 html2text==2020.1.16

# Install additional python packages
# hadolint ignore=DL3013
RUN IFS=',' read -ra PACKAGES <<< "${ADDITIONAL_PYTHON_PACKAGES}" && \
    if (( ${#PACKAGES[@]} != 0 )); then pip3 --no-cache-dir install "${PACKAGES[@]}"; fi


COPY entrypoint.sh /root/
RUN chmod 775 /root/entrypoint.sh
ENTRYPOINT ["/root/entrypoint.sh"]
