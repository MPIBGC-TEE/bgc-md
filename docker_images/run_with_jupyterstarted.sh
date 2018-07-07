#!/bin/bash
source conf
echo ${imageName} 
docker run -p 127.0.0.1:8888:8888 -w /workingfolder -d -t ${imageName} bash -c "source virtual_env/bin/activate && jupyter notebook --no-browser --allow-root --ip 0.0.0.0 "
sleep 3
firefox 127.0.0.1:8888 &
