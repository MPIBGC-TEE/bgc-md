# This script calls pip to perform package installation and adds some packages that we usually use 
# in conjuntion with our package

pip3 install --upgrade pip setuptools wheel

pip3 install -rrequirements.txt -e .
#python3 setup.py develop

## enable jupyter notebook nbextensions
#pip3 install tox #testtool to chech the lib against different python versions
#pip3 install concurrencytest 
#pip3 install --upgrade jupyter jupyter_contrib_nbextensions jupyter_nbextensions_configurator
#
#jupyter contrib nbextension install --user
#jupyter nbextensions_configurator enable --user
#jupyter nbextension enable python-markdown/main

 
