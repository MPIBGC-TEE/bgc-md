#!/bin/bash
source conf
export DOCKER_ID_USER="markusmueller1g"
docker login --username=markusmueller1g # --email=markus.mueller.1.g@googlemail.com
tagName="${DOCKER_ID_USER}/${imageName}:latest"
echo ${tagName}
docker tag "${imageName}:latest" ${tagName}
docker push ${DOCKER_ID_USER}/${imageName}

