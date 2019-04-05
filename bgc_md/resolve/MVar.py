from typing import List,Tuple,Callable 
from testinfrastructure.helpers import pe
from .NamedObject import NamedObject
from .Computer import Computer
from .IndexedSet import IndexedSet

class MVar(NamedObject):
    # A (M)ultiply defined (Var)iable that can possibly be computed 
    # in several ways defined by its computers
    # and can check if one of them works given a namespace
    def __init__(
            self
            ,name:str
            ,computerNames:List[str]=[]
            # We use an ordered List instead of an unordered set in order to express preferences in the order of attempts to obtain a specific result (to save time)
            # The default () for the computers means that the 
            # only known way to get the variable is that the user 
            # directly defined it.
            ,description:str=""):
        self._name        =name
        self.computerNames  = tuple(computerNames) # internally we rather have immutable tuples than an list
        self.description= description 
    
    @property
    def name(self):
        return self._name


    def __repr__(self):
        return """object of class {s.__class__}
        name: {s.name}
        computerNames: {s.computerNames}
        """.format( s=self)


    def computers(
            self
            ,allComputers:IndexedSet
        )->List[Computer]:
        return [ allComputers[cname]  for cname in self.computerNames ]


    def is_computable(
            self
            ,allMvars:frozenset
            ,allComputers:frozenset
            #,name_space:dict
            ,names_of_available_mvars:frozenset
        )->bool:
        
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

    
    def __hash__(self):
        h1=self.name.__hash__()
        h2=frozenset(self.computerNames).__hash__()
        return h1^h2


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
    
