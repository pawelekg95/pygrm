#!/bin/bash

DOCKER_IMAGES=$(docker images --filter "dangling=false" -q --no-trunc)

mkdir /tmp/docker_backup

for image in ${DOCKER_IMAGES}; do
  sudo docker save -o "/tmp/docker_backup/${image}.tar" "${image}"
done

sudo service docker stop
sudo rm -rf /var/lib/docker
sudo service docker restart

for file in /tmp/docker_backup/*.tar; do
  sudo docker load -i "${file}"
done

rm -rf /tmp/docker_backup/
