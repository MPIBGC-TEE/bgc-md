#!/bin/bash
source conf
echo ${imageName} 
docker run  -w /workingfolder -it ${imageName} 
