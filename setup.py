#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:

# This is the standard pyhon install script.
# Only if it does not work use the shell script ../install_bgc_md.sh in the folder above
# Keep the requirements.freeze clean and to a minimum.

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
        #py_modules=['external_module'], # external_module.py is a module living outside this dir as an example how to iclude something not 
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
                'render= bgc_md.reports:render_parse'
                ]
        },
        install_requires=[
            "bibtexparser"
            ,"CompartmentalSystems"
            ,"testinfrastructure"
            ,"concurrencytest"
        #    ,"mendeley "
            ,"PyYAML"
            ,"pandas"
            ,'netCDF4'
            ,'sqlalchemy'
            ,'oslash'
            ,'pypandoc'
        ],
        include_package_data=True,
        #zip_safe=False
     )

 
 
 
