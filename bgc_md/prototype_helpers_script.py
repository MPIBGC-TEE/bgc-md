from testinfrastructure.helpers import pe
from sympy.core.compatibility import exec_
from pathlib import Path
from inspect import currentframe,getmembers,isfunction
from typing import get_type_hints
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems import smooth_reservoir_model 
from sympy.vector import Vector,Dyadic,CoordSysND,express
from sympy import Symbol
from bgc_md import resolver
from bgc_md.resolver import special_var_string

import sys

srcFileName="source.py"
modelFolderName="models"
def srcPath(model_id):
    return Path(modelFolderName).joinpath(model_id,srcFileName)


def get(var_name,model_id):
    # this is the proxy function 
    # It will compile the user code and populate a sandbox by executing the code  

    # find the user code
    p=srcPath(model_id)

    with p.open() as f:
        code= compile(f.read(),p,mode='exec')
        #code= f.read()
    gns={}
    #prepare the execution environment
    exec(code,gns)
    
    #construct the name of the function to call from the var_name
    mvar=getattr(resolver,var_name)
    special_vars=gns[special_var_string] 
    return mvar(special_vars)

   
    # check if the user has defined it directly 
    
    
    
     
    
    
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

