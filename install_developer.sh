# This script calls pip to perform a package installation
# under the assumption that you already have populated your virtual environment with
# the packages:
# LAPM
# testinfrastructure
# CompartmentalSystems
# in develop mode by (setup.py develop or pip install -e)


pip3 install --upgrade pip setuptools wheel setuptools_git tox concurrencytest 

pip3 install -rrequirements.developer 
pip3 install -e .

## enable jupyter notebook nbextensions
#pip3 install --upgrade jupyter jupyter_contrib_nbextensions jupyter_nbextensions_configurator
#
#jupyter contrib nbextension install --user
#jupyter nbextensions_configurator enable --user
#jupyter nbextension enable python-markdown/main

 
 
 
 
 
