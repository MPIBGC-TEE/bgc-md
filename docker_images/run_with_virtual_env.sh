#!/bin/bash
source conf
echo ${imageName} 
docker run -p 127.0.0.1:8888:8888 -w /workingfolder -it ${imageName} bash --init-file /workingfolder/virtual_env/bin/activate -i 

