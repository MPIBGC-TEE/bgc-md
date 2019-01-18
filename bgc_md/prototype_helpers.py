from testinfrastructure.helpers import pe
from sympy.core.compatibility import exec_
from pathlib import Path
from inspect import currentframe,getmembers,isfunction
from typing import get_type_hints
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems import smooth_reservoir_model 
from sympy.vector import Vector,Dyadic,CoordSysND,express
from sympy import Symbol
import sys

srcFileName="source.py"
modelFolderName="models"
def srcPath(model_id):
    return Path(modelFolderName).joinpath(model_id,srcFileName)

#def get_Constructors(cls):
#    # look for other constructors  or factories returning that return
#    # an instance of cls
#    funcnames=[t[0] for t in getmembers(cls)]
#    funcs=[getattr(cls,fn) for fn in funcnames]
#    def isConstructor(func,cls):
#        if hasattr(func,'__annotations__'):
#            hints=get_type_hints(func)
#            if 'return' in hints:
#                return hints['return']==cls
#            else:
#                return False
#        else:
#            return False
#    srm_constructors=[ f for f in funcs if isConstructor(f,cls)]
#    return srm_constructors
#
#def get_factories(module,cls):
#    # look for constructors in this module
#    current_module=sys.modules[__name__]
#    print(current_module)
#    funcnames= [f[0] for f in getmembers(current_module,isfunction)] 
#    pe('funcnames',locals())
#    funcs=[getattr(current_module,fn) for fn in funcnames]
#    pe('funcs',locals())
#    factories_in_this_module=[ f for f in funcs if isConstructor(f,cls)]
#    constructors = srm_constructors+factories_in_this_module 
#    print(constructors)

def get_SmoothReservoirModel(model_id):
    # this is the proxy function 
    # It will examine the user code for a direct 
    # first remember the function name 
    myName=currentframe().f_code.co_name 
    pe('myName',locals())

    # find the user code
    p=srcPath(model_id)
    pe('p',locals())

    with p.open() as f:
        code= compile(f.read(),p,mode='exec')
        #code= f.read()
    gns={}
    #prepare the execution environment
    exec(code,gns)
    
    # check if the user has defined a direct implementation 
    # (a function with the same name and call it)
    if myName in gns.keys(): 
        md=eval(myName+"()",gns)
        pe('md',locals())
        return md
    # now recursively find out if we can get one of them to produce a SmoothReservoirModel with ingredients provided by the User
    elif {
    
    
     
    
    
def get(model_id,callString):
    p=srcPath(model_id)
    with p.open() as f:
        code= compile(f.read(),p,mode='exec')
        #code= f.read()
    gns={}
    #prepare the execution environment
    #exec_('from bgc_md.ModelDescriptor import ModelDescriptor',gns,lns) #
    #exec(code,gns,lns)
    exec(code,gns)
    #call the function
    res=eval(callString,gns)
    return res

# alternative constructor based on the formulation f=u+Bx but with 
# statevector and u bein sympy.vector.nd-vector Vectors
def srm_from_B_u_tens(C:CoordSysND,state_vector:Vector, time_symbol:Symbol, B:Dyadic, u:Vector)->'SmoothReservoirModel':
    state_vector_mat=express(state_vector,C).to_matrix(C)
    B_mat=express(B,C).to_matrix(C)
    u_mat=express(u,C).to_matrix(C)
    #pe('state_vector',locals())
    #pe('state_vector_mat',locals())
    #pe('B_mat',locals())
    #pe('u_mat',locals())
    return SmoothReservoirModel.from_B_u(state_vector_mat,time_symbol,B_mat,u_mat)

