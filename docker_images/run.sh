#!/bin/bash
source conf
echo ${imageName} 
docker run -it ${imageName}
