FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG CMAKE_VER=3.23.2
ARG CMAKE_URL=https://github.com/Kitware/CMake/releases/download/v${CMAKE_VER}/cmake-${CMAKE_VER}-linux-aarch64.tar.gz
ARG REPOSITORY
ARG GITHUB_TOKEN
ENV RUNNER_ALLOW_RUNASROOT="1"

WORKDIR /root

RUN echo APT::Install-Recommends "false"; >> /etc/apt/apt.conf && \
	echo APT::Install-Suggests "false"; >> /etc/apt/apt.conf && \
\
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

RUN echo APT::Install-Recommends "false"; >> /etc/apt/apt.conf && \
        echo APT::Install-Suggests "false"; >> /etc/apt/apt.conf && \
\
    apt-get update && \
    apt-get install -y curl && \
    mkdir actions-runner && cd actions-runner && \
    curl -o actions-runner-linux-arm64-2.296.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.296.1/actions-runner-linux-arm64-2.296.1.tar.gz && \
    tar xzf ./actions-runner-linux-arm64-2.296.1.tar.gz && \
    ./bin/installdependencies.sh

COPY --from=ubuntu:20.04 /root/* ./

RUN cd /root/actions-runner && \
    RUNNER_ALLOW_RUNASROOT="1" yes "" | /root/actions-runner/config.sh --url https://github.com/pawelekg95/${REPOSITORY} --token ${GITHUB_TOKEN}

RUN echo APT::Install-Recommends "false"; >> /etc/apt/apt.conf && \
        echo APT::Install-Suggests "false"; >> /etc/apt/apt.conf && \
\
    apt-get update && \
    apt-get install -y build-essential g++ llvm python3 python3-pip shellcheck git make clang-format clang-tidy wget xz-utils valgrind lcov libgpgme-dev

RUN pip3 install requests telnetlib3 pyserial pylint xmlrunner pandas scipy numpy
