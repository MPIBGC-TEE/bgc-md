from typing import List,Tuple,Callable 
from functools import reduce
from testinfrastructure.helpers import pe
from .NamedObject import NamedObject
from .IndexedSet import IndexedSet

class Computer(NamedObject):
    # this is like a function that knows what MVars it needs
    def __init__(
            self
            ,name
            ,func:Callable
            ,description:str=''):
        #to do:
        # make sure that the function func accomodates
        # the args 
        # (maybe also check the type if func has been annotated)
        self._name       =name
        self.func        =func
        #self.arg_names  =tuple(arg_names) #internally we want immutable tuples rather than lists
        self.description = description 
    
    def split_name(self):
        return IndexedSet.normalizeKey(self._name).split('(')

    @property
    def target_name(self):
        return self.split_name()[0]
    
    @property
    def _arg_name_string(self):
        return self.split_name()[1][:-1]

    @property
    def arg_names(self):
        return self._arg_name_string.split(',')

    @property
    def arg_name_set(self):
        # the set of necessary arguments
        return frozenset(self.arg_names)
    
    @property
    def name(self):
        return self._name 

    
    def args(self,allMvars):
        # the order of the arg_names must be preserved since the are related to
        # the signature of self.func
        return [ allMvars[mv_name] for mv_name in self.arg_names]

    
    def is_computable(
            self
            ,allMvars:IndexedSet
            ,allComputers:IndexedSet
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

    def __hash__(self):
        l=[self.name,self.func,frozenset(self.arg_names)]
        return reduce(lambda ac,el:ac^hash(el),l,0)

