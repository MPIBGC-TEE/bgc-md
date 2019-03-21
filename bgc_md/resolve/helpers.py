
import os
import contextlib
import sys
from pathlib import Path
from .Mvars import mvars_1 as mvars
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

def get(var_name,model_id):
    # execute the user code
    gns=populated_namespace(model_id)
    
    #construct the name of the function to call from the var_name
    #mvar=getattr(resolver,var_name)
    mvar=getattr(mvars,var_name)
    special_vars=gns[special_var_string] 
    return mvar(special_vars)

   
    # check if the user has defined it directly 
    
    
def get_documented_variables(model_id):
    #gns=populated_namespace(model_id)
    return [v for v in gns.values() if isinstance(v,DescribedQuantity)]
    

    
     
    
    
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
