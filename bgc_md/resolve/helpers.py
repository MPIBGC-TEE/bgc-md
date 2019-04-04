
import os
import contextlib
import sys
from pathlib import Path
from . import MvarsAndComputers as mvars
srcFileName="source.py"
modelFolderName="models"
special_var_string="special_vars"
def srcDirPath(model_id):
    return Path(modelFolderName).joinpath(model_id)

def srcPath(model_id):
    return srcDirPath(model_id).joinpath(srcFileName)

@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
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

    
def get3(var_name:str,allMvars,allComputers,model_id:str):
    # execute the model code
    gns=populated_namespace(model_id)
    
    # get the mvar by its name from the set by its index
    # this should be cached (hashed) as dict of cause
    mvar=[var for var in allMvars if var.name==var_name][0]
    special_vars=gns[special_var_string] 
    return mvar(allMvars,allComputers,special_vars)
    

def computable_mvars(
        allMvars:frozenset
        ,allComputers:frozenset
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
  
   # check if the user has defined it directly 
    
    
#def get_documented_variables(model_id):
#    #gns=populated_namespace(model_id)
#    return [v for v in gns.values() if isinstance(v,DescribedQuantity)]
    

    
     
    
    
#def get(model_id,callString):
#    p=srcPath(model_id)
#    with p.open() as f:
#        code= compile(f.read(),p,mode='exec')
#        #code= f.read()
#    gns={}
#    #prepare the execution environment
#    #exec_('from bgc_md.ModelDescriptor import ModelDescriptor',gns,lns) #
#    #exec(code,gns,lns)
#    exec(code,gns)
#    #call the function
#    res=eval(callString,gns)
#    return res


# alternative constructor based on the formulation f=u+Bx but with 
# statevector and u bein sympy.vector.nd-vector Vectors
# functions like the following could be sourced out into a helper module

