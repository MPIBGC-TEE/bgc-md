
import unittest
from pathlib import Path
from testinfrastructure.helpers import pe
from testinfrastructure.InDirTest import InDirTest
#from sympy import Basic,Symbol,Matrix,symbols

#from sympy.vector import CoordSysND, Vector,express
#from bgc_md.prototype_helpers_script import get
from sympy import Symbol,Number
from typing import List
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun
#from CompartmentalSystems import smooth_reservoir_model 
from .ClassesStateLess import MVar3,Computer3
from .functions import srm_from_B_u_tens
import collections

class FrozenDict(collections.Mapping):
    """Don't forget the docstrings!!"""

    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)
        self._hash = None

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __hash__(self):
        # It would have been simpler and maybe more obvious to 
        # use hash(tuple(sorted(self._d.iteritems()))) from this discussion
        # so far, but this solution is O(n). I don't know what kind of 
        # n we are going to run into, but sometimes it's hard to resist the 
        # urge to optimize when it will gain improved algorithmic performance.
        if self._hash is None:
            self._hash = 0
            for pair in self.iteritems():
                self._hash ^= hash(pair)
        return self._hash
#    >>> x = FrozenDict(a=1, b=2)
#>>> y = FrozenDict(a=1, b=2)
#>>> x is y
#False
#>>> x == y
#True
#>>> x == {'a': 1, 'b': 2}
#True
#>>> d = {x: 'foo'}
#>>> d[y]
#'foo'

myMvars=frozenset({
      MVar3('coord_sys') 
    , MVar3('state_vector')
    , MVar3('time_symbol') 
    , MVar3('compartmental_dyad') 
    , MVar3('input_vector') 
    , MVar3('parameter_dictionary') 
    , MVar3('start_vector') 
    , MVar3('time_vector') 
    , MVar3('function_dictionary')
    , MVar3(
            'smooth_reservoir_model'
            ,computerNames=['srm_bu_tens']
            ,description='A smooth reservroir Model'
        )
    , MVar3(
            'smooth_model_run_dictionary'
            ,computerNames=[] # at the moment empty list, consequently 
            # only available when explicitly defined. 
            # Although automatic computation would be simple 
            # the keys make most sense if defined by the user
            ,description= """
            The dictionary values are SmoothModelRun objects. 
            The keys can be used in user code to refer to special 
            simulations. """
    )
    , MVar3(
            'smooth_model_run'
            ,computerNames=['smr']
            ,description= """A single simulation"""
    )
})

myComputers=frozenset({
        Computer3(
            'srm_bu_tens'
            ,func=srm_from_B_u_tens
            ,arg_names=[
                 'coord_sys'
                ,'state_vector' 
                ,'time_symbol' 
                ,'compartmental_dyad' 
                ,'input_vector' 
             ]
            ,description="""Produces a smoth reservoir model"""
        )
        ,Computer3(
             'smr'
            ,SmoothModelRun
            ,arg_names=[
                 'smooth_reservoir_model'
                ,'parameter_dictionary'
                ,'start_vector'
                ,'time_vector'
                ,'function_dictionary'
            ]
            ,description="""Creates a single instance of a SmoothModelRun"""
        )
})
