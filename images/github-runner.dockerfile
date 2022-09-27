FROM ubuntu:20.04

# Hack to have access to bash useful utilities such as 'declare'
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ARG DEBIAN_FRONTEND=noninteractive

# Version >= 3.21 is welcome due to presence of presets
ARG CMAKE_VER=3.23.2

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
RUN echo APT::Install-Recommends "false"; >> /etc/apt/apt.conf && \
        echo APT::Install-Suggests "false"; >> /etc/apt/apt.conf && \
\
    apt-get update && \
    apt-get install -y build-essential g++ llvm python3 python3-pip shellcheck git make clang-format clang-tidy wget \
    xz-utils valgrind lcov libgpgme-dev ca-certificates curl gnupg lsb-release dpkg diffutils

# Install custom CMake version
RUN echo APT::Install-Recommends "false"; >> /etc/apt/apt.conf && \
	echo APT::Install-Suggests "false"; >> /etc/apt/apt.conf && \
\
    declare -A ARCHS=( ["amd64"]="x86_64" ["arm64"]="aarch64") && \
    ARCH=$(dpkg --print-architecture) && \
    CMAKE_URL="https://github.com/Kitware/CMake/releases/download/v${CMAKE_VER}/cmake-${CMAKE_VER}-linux-${ARCHS[${ARCH}]}.tar.gz" && \
    apt-get update && \
    apt-get install -y wget && \
    wget --no-check-certificate ${CMAKE_URL} && \
    mkdir -p /opt/cmake/${CMAKE_VER} && \
    tar -xf $(basename ${CMAKE_URL}) -C /opt/cmake/${CMAKE_VER} --strip-components=1 && \
    rm $(basename ${CMAKE_URL}) && \
    ln -s /opt/cmake/${CMAKE_VER}/bin/* /usr/bin/ && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download GitHub runner
RUN echo APT::Install-Recommends "false"; >> /etc/apt/apt.conf && \
        echo APT::Install-Suggests "false"; >> /etc/apt/apt.conf && \
\
    declare -A ARCHS=( ["amd64"]="x64" ["arm64"]="arm64" ["arm"]="arm") && \
    ARCH=$(dpkg --print-architecture) && \
    apt-get update && \
    apt-get install -y curl && \
    mkdir actions-runner && cd actions-runner && \
    curl -o actions-runner-linux-${ARCH}-2.296.1.tar.gz -L "https://github.com/actions/runner/releases/download/v2.296.1/actions-runner-linux-${ARCHS[${ARCH}]}-2.296.1.tar.gz" && \
    tar xzf ./actions-runner-linux-${ARCH}-2.296.1.tar.gz

COPY --from=ubuntu:20.04 /root/* ./

# Install GitHub runner
RUN cd /root/actions-runner && \
    /root/actions-runner/bin/installdependencies.sh && \
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
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install additional packages
RUN apt-get update && \
    IFS=',' read -ra PACKAGES <<< "${ADDITIONAL_PACKAGES}" && \
    if (( ${#PACKAGES[@]} != 0 )); then apt-get install "${PACKAGES[@]}"; fi

# Install base python packages
RUN pip3 install requests telnetlib3 pyserial pylint xmlrunner pandas scipy numpy pdoc3 scp paramiko html2text

# Install additional python packages
RUN IFS=',' read -ra PACKAGES <<< "${ADDITIONAL_PYTHON_PACKAGES}" && \
    if (( ${#PACKAGES[@]} != 0 )); then pip3 install "${PACKAGES[@]}"; fi


COPY entrypoint.sh /root/
RUN chmod 775 /root/entrypoint.sh
ENTRYPOINT ["/root/entrypoint.sh"]
