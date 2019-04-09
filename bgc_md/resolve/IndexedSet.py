from typing import Set
import collections
import re
from .NamedObject import NamedObject
class IndexedSet(collections.Mapping):
    """
    An immutable and therefore hashable set of objects with a name attribute, which will
    be used to index the objects in the set. 
    It is very much like a dictionary with the difference that the names of its elements have 
    itselv a meaning. (not only as keys in a dict) 
    We need it to access Computers and Mvars quickly (for which we need dict features) and cache the results
    of computations involving arguments of this type (for which purpose it has to be hashable and immutable)
    """
    @classmethod
    def normalizeKey(cls,string):
        # remove whitespace 
        rexp=re.compile('\s*')
        return re.sub(rexp,'',string)

    def __init__(self, s:Set[NamedObject]):
        #create a private dictionary indexed by the name attribute of the variable
        self._d = {v.name: v for v in s}
        self._hash = frozenset(s).__hash__()
    
    def __eq__(self,other):
        return self._hash == other.__hash__()

    def __iter__(self):
        return iter(self._d.values())

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        cls=self.__class__
        nkey=cls.normalizeKey(key)
        return self._d[nkey]

    def __hash__(self):
        return self._hash
        #values=self._d.values()
        #if self._hash is None:
        #    self._hash = 0
        #    for val in values:
        #        self._hash ^= hash(val)
        #return self._hash
