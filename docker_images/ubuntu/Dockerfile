FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y git
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv
RUN apt-get install -y texlive-binaries
RUN apt-get install -y pandoc
RUN apt-get install -y vim
RUN mkdir workingfolder
WORKDIR /workingfolder
RUN python3 -m venv virtual_env
COPY jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
COPY LAPM LAPM
WORKDIR /workingfolder/LAPM
RUN /bin/bash -c "source /workingfolder/virtual_env/bin/activate && ./install.sh develop"
WORKDIR /workingfolder
COPY CompartmentalSystems /workingfolder/CompartmentalSystems
WORKDIR /workingfolder/CompartmentalSystems
RUN /bin/bash -c "source /workingfolder/virtual_env/bin/activate && ./install_developer.sh"
WORKDIR /workingfolder
RUN git clone https://github.com/MPIBGC-TEE/bgc-md.git 
WORKDIR /workingfolder/bgc-md
RUN git pull
RUN /bin/bash -c "source /workingfolder/virtual_env/bin/activate && ./install_developer.sh"
EXPOSE 8888/tcp



#
#WORKDIR /workingfolder/bgc-md/
#RUN ./install.sh
#CMD ["useradd", "-m","bgc_user"]
#WORKDIR /home/bgc_user
#CMD ["git","clone","https://github.com/MPIBGC-TEE/bgc-md.git"]
#RUN mkdir virtual_env
#CMD ["python3","-m","venv","virtual_env" ]
#CMD ["source", "virtual_env/bin/activate"]
#WORKDIR /home/bgc_user/bgc-md
#RUN chmod +x install.sh
#RUN chmod +x install_developer.sh
#RUN install.s
