#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:

# This is the standard pyhon install script.
# Only if it does not work use the shell script ../install_bgc_md.sh in the folder above
# Keep the requirements.txt clean and to a minimum.

from setuptools import setup,find_packages
def readme():
    with open('README.md') as f:
        return f.read()
    
setup(name='bgc_md',
        version='0.1',
        test_suite="example_package.tests",#http://pythonhosted.org/setuptools/setuptools.html#test
        description='Model Database for Carbon Allocation',
        long_description=readme(),#avoid duplication 
        author='Veronika, Holger, Markus',
        author_email='markus.mueller.1.g@gmail.com',
        url='https://projects.bgc-jena.mpg.de/hg/SOIL-R/Code/packageTests/bgc_md',
        packages=find_packages(), #find all packages (multifile modules) recursively
        py_modules=['external_module'], # external_module.py is a module living outside this dir as an example how to iclude something not 
        classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education "
        ],
        entry_points={
        'console_scripts': [
                'generate_website= bgc_md.reports:generate_website' # creates an executable with name generate_website
                ,'generate_model_run_reports= bgc_md.reports:generate_model_run_reports' # ...
                ,'generate_model_run_report= bgc_md.reports:generate_model_run_report' # ...
                ,'generate_miniaml_model_report= bgc_md.reports:generate_miniaml_model_report' # ...
                ,'generate_miniaml_model_reports= bgc_md.reports:generate_miniaml_model_reports' # ...
                ]
        },
        #dependency_links=[
        #    'git+https://git@github.com/MPIBGC-TEE/LAPM.git#egg=LAPM',
        #    'git+https://git@github.com/MPIBGC-TEE/CompartmentalSystems.git#egg=CompartmentalSystems',
        #    'git+https://git@github.com/mamueller/testinfrastructure.git#egg=testinfrastructure', 
        #],   
        install_requires=[
            "bibtexparser"
           # ,"CacheControl"
            ,"CompartmentalSystems"
            ,"testinfrastructure"
            ,"concurrencytest"
           # ,"future == 0.14.3"
           # ,"arrow == 0.5.0"
           # ,"memoized_property == 1.0.2"
           # ,"##for mendeley"
           # ,"requests == 2.5.1"
            ,"mendeley "
           # ,"chardet"
           # ,"ipython"
           # ,"matplotlib >= 1.5.3"
           # ,"ndg-httpsclient"
           # ,"Pygments"
           # ,"python-subunit"
            ,"PyYAML"
           # ,"tqdm"
           # ,"numpy >=1.11.2"
           # ,"scipy >=0.17.0"
           # ,"# mpi4py >=2.0.0"
           # ,"linecache2"
           # ,"pyasn1"
           # ,"# pathos"
           # ,"plotly"
           # ,"urllib3"
           # ,"certifi"
           # ,"idna"
        ],
        include_package_data=True,
        zip_safe=False)

 
 
 
