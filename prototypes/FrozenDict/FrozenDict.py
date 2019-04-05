
import collections
class FrozenDict(collections.Mapping):
    """
    An immutable and therefore hashable dictionary
    We need it to access Computers and Mvars quickly (for which we need dict features) and cache the results
    of computations involving arguments of this type (for which purpose it has to be hashable)
    https://stackoverflow.com/a/2704866/10393639
    """
    @classmethod
    def from_MVarSet(cls,mvs:set):
        normalDict={ mv.name: mv for mv in mvs}
        return cls(normalDict)

    def __init__(self, d):
        self._d = d
        self._hash = None
    
    #def __init__(self, *args, **kwargs):
    #    self._d = dict(*args, **kwargs)
    #    self._hash = None

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __hash__(self):
        if self._hash is None:
            self._hash = 0
            for pair in self.items():
                self._hash ^= hash(pair)
        return self._hash
