from typing import List,Callable 
class MVar2:
    # A (M)ultiply defined (Var)iable that can possibly be computed 
    # in several ways defined by its computers
    # and can check if one of them works given a namespace
    def __init__(self, name:str,allComputers:dict, computerNames:List[str]=[] ,description:str=""):
        # The default [] for the computers means that the 
        # only known way to get the variable is that the user 
        # directly defined it.
        self.name        =name
        self.allComputers= allComputers
        self.computerNames  = computerNames
        self.description= description 

    @property
    def computers(self):
        return [ self.allComputers[key] for key in self.computerNames ]

    def is_computable(self,name_space:dict):
        if self.name in name_space.keys():
            return True
        else:
            return any( c.is_computable(name_space) for c in  self.computers) 

    def computable_computers(self,name_space):
        coms=[
            c for c in self.computers 
            if c.is_computable(name_space)
        ]
        return coms

    def __call__(self,name_space):
        if self.name in name_space.keys():
            return name_space[self.name]
        # check which computers actually are computable and
        # take the first one
        else:
            working_computers=self.computable_computers(name_space)
            if len(working_computers)>0:
                return working_computers[0](name_space)
            else:
                raise Exception("The Mvar can not be computed from the given namespace")


class Computer2:
    # this is like a function that knows what MVars it needs
    def __init__(
            self
            ,allMvars:dict 
            ,func:Callable
            ,arg_names:List[str]
            ,description:str=''):
        #to do:
        # make sure that the function func accomodates
        # the args 
        # (maybe also check the type if func has been annotated)
        self.allMvars    =allMvars
        self.func        =func
        self.arg_names  =arg_names
        self.description = description 
    
    @property
    def args(self):
        return [ self.allMvars[key] for key in self.arg_names]

    
    def is_computable(self,name_space):
        return all( mvar.is_computable for mvar in  self.args) 
    
    def __call__(self,name_space):
        vals=[arg(name_space) for arg in self.args]
        #pe('vals',locals())
        return self.func(*vals)

