import os
#import contextlib
from ..helpers import working_directory
import sys
from pathlib import Path
from testinfrastructure.helpers import pe
#from . import MvarsAndComputers as mvars
from .MvarsAndComputers import Mvars as myMvars
from .MvarsAndComputers import Computers as myComputers
from .IndexedSet import IndexedSet
from bgc_md.reports import defaults

srcFileName="source.py"
d=defaults() 
modelFolderName=d['paths']['new_models_path']
special_var_string="special_vars"
def srcDirPath(model_id):
    return Path(modelFolderName).joinpath(model_id)

def srcPath(model_id):
    p=srcDirPath(model_id).joinpath(srcFileName)
    pe('p',locals())
    return p

def populated_namespace_from_path(p:Path):
    # this is the proxy function 
    # It will compile the user code and populate a sandbox by executing the code  
    

    with p.open() as f:
        code= compile(f.read(),p,mode='exec')
        #code= f.read()
    gns={}
    
    # prepare the execution environment
    # and execute in the directory since the model might need input files and 
    # also other python code in the same directory
    with working_directory(p.parent):
        exec(code,gns)
    return gns

def populated_namespace(model_id):
    # this is the proxy function 
    # It will compile the user code and populate a sandbox by executing the code  
    
    # find the user code
    p=srcPath(model_id)

    with p.open() as f:
        code= compile(f.read(),p,mode='exec')
        #code= f.read()
    gns={}
    
    # prepare the execution environment
    # and execute in the directory since the model might need input files and 
    # also other python code
    with working_directory(srcDirPath(model_id)):
        exec(code,gns)
    return gns

def get_bgc(var_name:str,model_id:str):
    return get3(var_name,myMvars,myComputers,model_id)

def is_computable_bgc(var_name:str,model_id:str):
    return myMvars[var_name].is_computable(myMvars,myComputers,names_of_available_mvars(model_id))
    
def get3(var_name:str,allMvars,allComputers,model_id:str):
    # execute the model code
    #gns=populated_namespace(model_id)
    
    #mvar=[var for var in allMvars if var.name==var_name][0]
    #special_vars=gns[special_var_string] 
    mvar=allMvars[var_name]
    return mvar(allMvars,allComputers,special_vars(model_id))
    
def special_vars(model_id):
    gns=populated_namespace(model_id)
    return gns[special_var_string] 

def names_of_available_mvars(model_id):
    return [str(k) for k in special_vars(model_id).keys()]


def computable_mvars(
        allMvars:IndexedSet
        ,allComputers:IndexedSet
        ,names_of_available_mvars:frozenset
    )->frozenset:
    #top down approach: for every mvar in all Mvars check if we can compute it:
    l= [mvar for mvar in allMvars 
            if mvar.is_computable(
                allMvars
                ,allComputers
                ,names_of_available_mvars
            )]
    return frozenset(l)
  
