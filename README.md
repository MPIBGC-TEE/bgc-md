# INSTALLATION
## Prerequisites:
  - venv
    To install we recommend using a virtual python environment.
    The python3 standard library provides the module *venv* already, so there is no need for third party
    software.
    Some distributions do not install it by default
    E.g. for ubuntu you have to say:
    *sudo apt-get install python3.4-venv*
  - pandoc
    E.g. for ubuntu you have to say:
    *sudo apt-get install pandoc*

## Create virtual environment (e.g. in ~/test)
```bash
    $ cd ~
    $ mkdir test
    $ python3 -m venv test
```
## Activate virtual environment
```bash
     $ source ~/test/bin/activate
```
    (from now on python3 and pip commands will operate in this virtual environment and install everything
     that is needed there)
## Install the package in development mode:
    Since the package will be used (tested) and edited at the same time we recommend to install it in
    development mode. This makes all the dependencies available but does not copy files to the virtual environment (or any other environment) .
    It just links them there, so that source code changes take immediate effect in the *installed* package.
    No reinstallation after source changes is necessary.
```bash    
    $ cd to_the_directory_of_this_file
    $ python3 setup.py develop
```
    It is possible that this already does the trick since the setup script tries to install
    missing dependencies automatically. Depending on your system some of those dependencies
    may have problems. We describe some workarounds in the next paragraph

## Troubleshooting:
    You can try to install the requirement beforehand (separately from the actual bgc_md package) by
```bash    
    $ pip3 install -r requirements.txt
```
    likely troublemakers are (due to their complex buildprocess)
    matplotlib ,numpy and scipy

    to identify the problems you can also try to install them separately
    e.g: pip3 install numpy


    on unbuntu building of these python packages requires non python libraries to be installed
    try:
```bash
    $ sudo apt-get install libfreetype6-dev
    $ sudo apt-get install libffi6 libffi-dev
    $ sudo apt-get install libssl-dev
```
