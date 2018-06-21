FROM ubuntu:latest
RUN apt-get update 
RUN apt-get upgrade -y
RUN apt-get install -y git
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv
RUN apt-get install -y texlive-binaries
RUN apt-get install -y pandoc
RUN mkdir virtual_env
CMD ["python3","-m","venv","virtual_env" ]
CMD source virtual_env/bin/activate
CMD ["git","clone","https://github.com/MPIBGC-TEE/bgc-md.git"]
CMD ["cd", "bgc-md"]
RUN chmod +x install.sh
RUN chmod +x install_developer.sh
RUN install.sh
