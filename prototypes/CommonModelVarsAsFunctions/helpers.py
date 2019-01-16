from testinfrastructure.helpers import pe
from sympy.core.compatibility import exec_
from pathlib import Path

srcFileName="source.py"
modelFolderName="models"
def srcPath(model_id):
    return Path(modelFolderName).joinpath(model_id,srcFileName)

def getModelDescriptor(model_id,nr):
    p=srcPath(model_id)
    pe('p',locals())

    with p.open() as f:
        code= compile(f.read(),p,mode='exec')
        #code= f.read()
    gns={}
    #prepare the execution environment
    #exec_('from bgc_md.ModelDescriptor import ModelDescriptor',gns,lns) #
    #exec(code,gns,lns)
    exec(code,gns)
    #call the function
    md=eval("get_ModelDescriptor()",gns)
    pe('md',locals())
    return md
    
    
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

