# This script calls pip to perform package installation and adds some packages that we usually use 
# in conjuntion with our package

pip3 install --upgrade pip setuptools wheel setuptools_git jupyter jupyter_contrib_nbextensions jupyter_nbextensions_configurator concurrencytest tox
# installs the libraries with pinned versions 
pip3 install -rrequirements.freeze

# installs all the libraries found in setup.py that do not need version pinning
# and runs setup.py develop afterwards (installs bgc_md by linking to the sourcecode in this directory(
# so that changes in the source code take immediate effect without neccessiation a reinstall.
pip3 install -e . 


## enable jupyter notebook nbextensions
jupyter contrib nbextension install --user
jupyter nbextensions_configurator enable --user
jupyter nbextension enable python-markdown/main

 
 
 
 
 
