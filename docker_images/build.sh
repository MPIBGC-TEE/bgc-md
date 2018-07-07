#!/bin/bash
source conf
docker build -t ${imageName} . # --no-cache 
