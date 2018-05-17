# bgc_md: biogeochemical model database
This package consists of two components:
- A folder with yaml files which encode several soil, vegetation, and ecosystem models in a unified way.
- A python package that can be used (and extended) to run queries against single models or subsets of the encoded models.


## INSTALLATION
### Prerequisites:
  - To install we recommend using a virtual python environment.
    The python3 standard library provides the module *venv* already, so there is no need for third party
    software.
    Some distributions do not install it by default
    E.g. for ubuntu you have to say:```bash
    sudo apt-get install python3.4-venv*```
  - pandoc
    E.g. for ubuntu you have to say:
    ```bash sudo apt-get install pandoc*```

### Create virtual environment (e.g. in ~/test)
```bash
    $ cd ~
    $ mkdir test
    $ python3 -m venv test
```
### Activate virtual environment
```bash
     $ source ~/test/bin/activate
```
From now on python3 and pip commands will operate in this virtual environment and install everything
that is needed there.
### Install the package in user only mode:
- Assuming that you just want to use the package and are not going to change any of the packages it depends on
  you can just type the following commands:
```bash
     $ pip install -r requirements.freeze
     $ python setup.py develop
```
- You can also run the script 
```bash
     $ ./install.sh 
```
  which does the same but installs some additional software that is
  usefull in connection with the package.


## Install the package for development:
The package depends on other packages which will often be edited and tested at the same time:
(testinfrastructure, LAPM, CompartmentalSystems)
If you develop those packages it is recommended to install them also in development mode.
If you do that for the first time it means to go to run setup.py (or the install script ) 
in the respective directories of th packages on your system in the following order: 
- testinfrastructure, 
- LAPM , 
- CompartmentalSystems.
After this you can type.
```bash    
     $ pip install -r requirements.developer
     $ python setup.py develop
```
or run the script 
```bash    
    $ ./install_developer.sh 
``` 
which does the same.
All the changes you make to the source code of either package will then 
be immidiately visible in your virtualenv since 
```bash    
    $ python setup.py develop 
``` 
does not copy files to the virtual environment (or any other environment) .
It just links them there, so that source code changes take immediate effect in the *installed* package.
No reinstallation after source changes is necessary.
    
## Troubleshooting:
Likely troublemakers are (due to their complex buildprocess) matplotlib ,numpy and scipy.
To identify the problems you can also try to install them separately e.g: 
```bash
pip3 install numpy
```
on unbuntu building of these python packages requires non python libraries to be installed try:
```bash
    $ sudo apt-get install libfreetype6-dev
    $ sudo apt-get install libffi6 libffi-dev
    $ sudo apt-get install libssl-dev
```
