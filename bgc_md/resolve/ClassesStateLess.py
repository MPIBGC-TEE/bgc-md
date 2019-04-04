
from typing import List,Callable 
def getElement(s:frozenset,name:str)->'MVar3':
    # fixme: mm This function is a workaround
    # actually mvars and Computers should internally be
    # represented by some kind of 'immutable indexed sets'
    # that basically work like dictionaries but until then
    # this function replaces the index operator []
    for v in s:
        if v.name==name:
            return v

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

    def __repr__(self):
        return """object of class {s.__class__}
        name: {s.name}
        computerNames: {s.computerNames}
        """.format( s=self)


    def computers(self,allComputers):
        return [ c for c in allComputers if c.name in self.computerNames ]

    def is_computable(
            self
            ,allMvars:frozenset
            ,allComputers:frozenset
            #,name_space:dict
            ,names_of_available_mvars:frozenset
        )->bool:
        #if self.name in name_space.keys():
        if self.name in names_of_available_mvars:
            # edge case because mvar is directly defined
            return True
        else:
            return any( 
                c.is_computable(
                    allMvars
                    ,allComputers
                    ,names_of_available_mvars
                ) for c in  self.computers(allComputers)) 

    def computable_computers(
            self
            ,allMvars:frozenset
            ,allComputers:frozenset
            ,names_of_available_mvars
        )->frozenset: 
        coms=[
            c for c in self.computers(allComputers) 
            if c.is_computable(
                allMvars
                ,allComputers
                ,names_of_available_mvars
            )
        ]
        return coms

    def __call__(self,allMvars,allComputers,name_space):
        if self.name in name_space.keys():
            return name_space[self.name]
        # check which computers actually are computable and
        # take the first one
        else:
            names_of_available_mvars=frozenset([k for k in name_space.keys()])
            working_computers=self.computable_computers(
                allMvars
                ,allComputers
                ,names_of_available_mvars
            )
            if len(working_computers)>0:
                return working_computers[0](allMvars,allComputers,name_space)
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
        # the order of the arg_names must be preserved
        #return [mv for mv in allMvars if mv.name in self.arg_names]
        return [getElement(allMvars,mv_name) for mv_name in self.arg_names]

    
    def is_computable(
            self
            ,allMvars:frozenset
            ,allComputers:frozenset
            ,names_of_available_mvars:frozenset
        )->bool:
        return all( mvar.is_computable(
            allMvars
            ,allComputers
            ,names_of_available_mvars
            ) for mvar in  self.args(allMvars)) 
    
    def __call__(self,allMvars,allComputers,name_space):
        vals=[arg(allMvars,allComputers,name_space) for arg in self.args(allMvars)]
        #pe('vals',locals())
        return self.func(*vals)

