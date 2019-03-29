
from typing import List,Callable 
class MVar3:
    # A (M)ultiply defined (Var)iable that can possibly be computed 
    # in several ways defined by its computers
    # and can check if one of them works given a namespace
    def __init__(self, name:str, computerNames:List[str]=[] ,description:str=""):
        # The default [] for the computers means that the 
        # only known way to get the variable is that the user 
        # directly defined it.
        self.name        =name
        self.computerNames  = computerNames
        self.description= description 

    def computers(self,allComputers):
        return [ allComputers[key] for key in self.computerNames ]

    def is_computable(self,allMvars,allComputers,name_space:dict):
        if self.name in name_space.keys():
            return True
        else:
            return any( c.is_computable(allMvars,allComputers,name_space) for c in  self.computers(allComputers)) 

    def computable_computers(self,allMvars,allComputers,name_space):
        coms=[
            c for c in self.computers(allComputers) 
            if c.is_computable(allMvars,allComputers,name_space)
        ]
        return coms

    def __call__(self,allMvars,allComputers,name_space):
        if self.name in name_space.keys():
            return name_space[self.name]
        # check which computers actually are computable and
        # take the first one
        else:
            working_computers=self.computable_computers(allMvars,allComputers,name_space)
            if len(working_computers)>0:
                return working_computers[0](name_space)
            else:
                raise Exception("The Mvar can not be computed from the given namespace")
    
class Computer3:
    # this is like a function that knows what MVars it needs
    def __init__(
            self
            ,name
            ,func:Callable
            ,arg_names:List[str]
            ,description:str=''):
        #to do:
        # make sure that the function func accomodates
        # the args 
        # (maybe also check the type if func has been annotated)
        self.name        =name
        self.func        =func
        self.arg_names  =arg_names
        self.description = description 
    
    def args(self,allMvars):
        return [ allMvars[key] for key in self.arg_names]

    
    def is_computable(self,allMvars,allComputers,name_space):
        return all( mvar.is_computable(allComputers) for mvar in  self.args(allMvars)) 
    
    def __call__(self,allMvars,allComputers,name_space):
        vals=[arg(allMvars,allComputers,name_space) for arg in self.args(allMvars)]
        #pe('vals',locals())
        return self.func(*vals)

