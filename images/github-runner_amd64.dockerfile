FROM ubuntu:20.04
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG DEBIAN_FRONTEND=noninteractive

# Version >= 3.21 is welcome due to presence of presets
ARG CMAKE_VER=3.23.2
ARG CMAKE_URL="https://github.com/Kitware/CMake/releases/download/v${CMAKE_VER}/cmake-${CMAKE_VER}-linux-x86_64.tar.gz"
ARG GITHUB_RUNNER_URL="https://github.com/actions/runner/releases/download/v2.296.1/actions-runner-linux-x64-2.296.1.tar.gz"
ARG HADOLINT_URL="https://github.com/hadolint/hadolint/releases/download/v2.10.0/hadolint-Linux-x86_64"

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
    apt-get install -y --no-install-recommends build-essential=12.8ubuntu1.1 g++=4:9.3.0-1ubuntu2 llvm=1:10.0-50~exp1 && \
    apt-get install -y --no-install-recommends python3=3.8.2-0ubuntu2 python3-pip=20.0.2-5ubuntu1.6 shellcheck=0.7.0-2build2 git=1:2.25.1-1ubuntu3.5 make=4.2.1-1.2 && \
    apt-get install -y --no-install-recommends clang-format=1:10.0-50~exp1 clang-tidy=1:10.0-50~exp1 wget=1.20.3-1ubuntu2 xz-utils=5.2.4-1ubuntu1.1 valgrind=1:3.15.0-1ubuntu9.1 && \
    apt-get install -y --no-install-recommends lcov=1.14-2 libgpgme-dev=1.13.1-7ubuntu2 ca-certificates=20211016~20.04.1 curl=7.68.0-1ubuntu2.13 gnupg=2.2.19-3ubuntu2.2 && \
    apt-get install -y --no-install-recommends lsb-release=11.1.0ubuntu2 dpkg=1.19.7ubuntu3.2 diffutils=1:3.7-3 && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install custom CMake version
RUN curl -o "cmake_v${CMAKE_VER}" -L "${CMAKE_URL}" && \
    mkdir -p "/opt/cmake/${CMAKE_VER}" && \
    tar -xf "$(basename cmake_v${CMAKE_VER})" -C "/opt/cmake/${CMAKE_VER}" --strip-components=1 && \
    rm "$(basename cmake_v${CMAKE_VER})" && \
    ln -s "/opt/cmake/${CMAKE_VER}/bin/*" /usr/bin/ && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install hadolint - Dockerfile linter
RUN curl -o /usr/bin/hadolint -L "${HADOLINT_URL}" && \
    chmod 775 /usr/bin/hadolint

# Download GitHub runner
RUN mkdir actions-runner
WORKDIR /root/actions-runner
RUN curl -o "actions-runner-linux-x86_64-2.296.1.tar.gz" -L "${GITHUB_RUNNER_URL}" && \
    tar xzf "./actions-runner-linux-x86_64-2.296.1.tar.gz"

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
RUN pip3 --no-cache-dir install requests==2.26.0 telnetlib3==1.0.4 pyserial==3.5 pylint==2.12.2 xmlrunner==1.7.7 \
    pandas==1.3.5 scipy==1.7.3 numpy==1.21.4 pdoc3==0.10.0 scp==0.14.4 paramiko==2.11.0 html2text==2020.1.16

# Install additional python packages
# hadolint ignore=DL3013
RUN IFS=',' read -ra PACKAGES <<< "${ADDITIONAL_PYTHON_PACKAGES}" && \
    if (( ${#PACKAGES[@]} != 0 )); then pip3 --no-cache-dir install "${PACKAGES[@]}"; fi


COPY entrypoint.sh /root/
RUN chmod 775 /root/entrypoint.sh
ENTRYPOINT ["/root/entrypoint.sh"]
