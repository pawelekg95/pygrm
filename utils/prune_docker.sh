#!/bin/bash

DOCKER_IMAGES=$(sudo docker images --format="{{.Repository}}")
DOCKER_CONTAINERS=$(sudo docker container ls --format="{{.Image}}")
declare -a CONTAINERS_TO_RESTART=()

mkdir /tmp/docker_backup

for image in ${DOCKER_IMAGES}; do
  if [[ " ${DOCKER_CONTAINERS[*]} " =~  ${image}  ]]; then
    CONTAINERS_TO_RESTART+=("${image}")
  fi
  sudo docker save -o "/tmp/docker_backup/${image}.tar" "${image}" || { echo -e "Failed to export image ${image}"; exit 1; }
done

sudo service docker stop
sudo rm -rf /var/lib/docker
sudo service docker restart

for file in /tmp/docker_backup/*.tar; do
  sudo docker load -i "${file}"
done

for container in "${CONTAINERS_TO_RESTART[@]}"; do
  sudo docker run -d --restart unless-stopped --network host -v /var/run/docker.sock:/var/run/docker.sock "${container}"
done

rm -rf /tmp/docker_backup/
