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
from bgc_md.DescribedSymbol import DesribedSymbol
from bgc_md.DescribedQuantity import DescribedQuantity
import sys

srcFileName="source.py"
uiDataFileName="gui.py"
modelFolderName="models"
def srcPath(model_id):
    return Path(modelFolderName).joinpath(model_id,srcFileName)

def uiDataPath(model_id):
    return Path(modelFolderName).joinpath(model_id,uiDataFileName)

class BaseQuantity:
    def __init__(self,name:str,dim:str,dimsys:str,description:str=""):
        self.name=name
        self.dim=dim
        self.dimsys=dimsys
        self.desription=description
    def to_code(self):
        code="""
{0}=DescribedQuantity('{0}')
{0}.set_dimension({1},'{2}')
{0}.set_description('{3}')""".format(self.name,self.dim,self.dimsys,self.desription)
        return code

class DerivedVariable:
    def __init__(self,name:str,expr:str,description:str=""):
        self.name=name
        self.expr=expr
        self.description=description
    def to_code(self):
        code="""
{0}={1}
""".format(self.name,self.expr)
        return code

class SemanticVariable:
    def __init__(self,name:str,expr:str,description:str=""):
        # to do:
        # 1.)   check if an MVar definition of this name exists
        #       in the resolver module otherwise refuse with
        #       the hint to implement one first
        # 2.)   intherit from Derived
        self.name=name
        self.expr=expr
        self.description=description
    def to_code(self):
        code="""
{0}={1}
""".format(self.name,self.expr)
        return code

def namespace_from_path(p):
    with p.open() as f:
        code= compile(f.read(),p,mode='exec')
        #code= f.read()
    gns={}
    #prepare the execution environment
    exec(code,gns)
    return gns

    

def get(var_name,model_id):
    # execute the user code
    gns=namespace_from_path(srcPath(model_id))
    
    #construct the name of the function to call from the var_name
    mvar=getattr(resolver,var_name)
    special_vars=gns[special_var_string] 
    return mvar(special_vars)

   
    # check if the user has defined it directly 
def getBaseQuantities(model_id):
    # todo: implement some caching 
    # first execute the source.py of th model
    script_ns=namespace_from_path(srcPath(model_id))
    gui_ns   =namespace_from_path(uiDataPath(model_id))
    # then define the baseQuanteties 
    for tup in gui_ns['baseQuantities']:
        exec(BaseQuantity(*tup).to_code(),script_ns)

    return [v for v in script_ns.values() if isinstance(v,DescribedQuantity)]

def getDerivedValues(model_id):
    # todo: implement some caching 
    # first execute the source.py of th model
    script_ns=namespace_from_path(srcPath(model_id))
    gui_ns   =namespace_from_path(uiDataPath(model_id))
    for tup in gui_ns['baseQuantities']:
        exec(BaseQuantity(*tup).to_code(),script_ns)
    dv_tup=gui_ns['derivedVariables']
    for tup in dv_tup:
        exec(DerivedVariable(*tup).to_code(),script_ns)
    
    return [script_ns[tup[0]] for tup in dv_tup ]

def getSemanticValues(model_id):
    # todo: implement some caching 
    # first execute the source.py of th model
    script_ns=namespace_from_path(srcPath(model_id))
    gui_ns   =namespace_from_path(uiDataPath(model_id))
    for tup in gui_ns['baseQuantities']:
        exec(BaseQuantity(*tup).to_code(),script_ns)
    dv_tup=gui_ns['derivedVariables']
    for tup in dv_tup:
        exec(DerivedVariable(*tup).to_code(),script_ns)
    sv_tup=gui_ns['semanticVariables']
    for tup in sv_tup:
        exec(SemanticVariable(*tup).to_code(),script_ns)

    return [script_ns[tup[0]] for tup in sv_tup ]

