#ASSIGNE FUNDATION IMAGE
FROM centos:7
#INSTALL NEEDED COMPONENTS
RUN yum -y update
RUN yum -y install git
RUN yum -y groupinstall development
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install python36u
RUN yum -y install python36u-pip
RUN yum -y install python36u-devel
RUN mkdir workingfolder
WORKDIR /workingfolder
RUN python3.6 -m venv virtual_env
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

##RUN git clone https://github.com/MPIBGC-TEE/bgc-md.git
##RUN python3.6 -m venv virtual_env
##RUN source virtual_env/bin/activate; cd bgc-md/; ./install.sh
##WORKDIR /workingfolder/bgc-md/
##RUN ./install.sh
