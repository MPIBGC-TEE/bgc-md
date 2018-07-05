# Docker support
## Decription
The images create a virtual environment and install the packages [LAPM](https://www.bgc-jena.mpg.de/TEE/index.html) [CompartmentalSystems](https://www.bgc-jena.mpg.de/TEE/index.html) and [bgc-md](https://www.bgc-jena.mpg.de/TEE/index.html) (this package) in development mode.
In consequence you can pull recent changes (by git pull in the respective directory) or play around with the source and see
the effects immediately. 
The containers contain also a jupyter installation in the same virtual_env. We provide some examples how to run it in the 
container and connect with your browser from outside the container.
This makes it really easy to try out the packages.

## Getting the images from dockerhub
```bash
docker pull markusmueller1g/bgc_md_centos7
```
or
```bash
docker pull markusmueller1g/bgc_md_ubuntu
```


## Run an image
This directory has a subdirectory for every container we provide. 
The syubdirectories contain some tiny bash scripts.
Let us assume we want to run the ubuntu container.
```bash
cd centos7
```
We can then run the container by.
```bash
./run_with_jupyterstarted.sh
```
This will map the port 8888 of the container to port 8888 of your computer and start firefox at localhost:8888
You are connected with the jupyter server in the container
The required password is just set to "test".
You do not have to run the scripts. They are just there to demonstrate the docker commands you would have to use (e.g. on a Windows machine without bash).

## Changing your image
You can of course extend and personalize the downloaded image and even use it to contribute.
