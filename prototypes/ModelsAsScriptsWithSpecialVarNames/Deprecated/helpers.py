
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
    # execute the model code
    gns=populated_namespace(model_id)
    
    #take the name of the MVar in the module as equivalent to the var_name
    mvar=getattr(mvars,var_name)
    special_vars=gns[special_var_string] 
    return mvar(special_vars)

def get2(var_name:str,allMvars,model_id:str):
    # execute the model code
    gns=populated_namespace(model_id)
    
    #get the mvar by its name from the dictionary 
    mvar=allMvars[var_name]
    special_vars=gns[special_var_string] 
    return mvar(special_vars)
