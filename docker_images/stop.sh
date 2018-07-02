#!/bin/bash
source conf
echo ${imageName}
id=$(docker ps|grep "${imageName}"|awk '{print $1}')
echo ${id}
docker stop ${id}
