
import unittest
from pathlib import Path
from testinfrastructure.helpers import pe
from testinfrastructure.InDirTest import InDirTest
#from sympy import Basic,Symbol,Matrix,symbols

#from sympy.vector import CoordSysND, Vector,express
#from bgc_md.prototype_helpers_script import get
from sympy import Symbol,Number
from sympy.vector import CoordSysND,express,Vector,Dyadic
from typing import List
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun
#from CompartmentalSystems import smooth_reservoir_model 
#from .ClassesStateLess import MVar3,Computer3
from . import functions 
from .IndexedSet import IndexedSet
from .MVar import MVar
from .Computer import Computer
Mvars=IndexedSet({
      MVar('coord_sys') 
    , MVar('state_vector')
    , MVar('time_symbol') 
    , MVar('compartmental_dyad') 
    , MVar('compartmental_matrix')
    , MVar('input_vector') 
    , MVar('parameter_dictionary') 
    , MVar('start_vector') 
    , MVar('time_vector') 
    , MVar('function_dictionary')
    , MVar( 'smooth_reservoir_model')
    , MVar( 'smooth_model_run_dictionary'
            ,description= """
            The dictionary values are SmoothModelRun objects. 
            The keys can be used in user code to refer to special 
            simulations. """
    )
    , MVar(
            'smooth_model_run'
            ,description= """A single simulation"""
    )
})

Computers=IndexedSet({
        Computer('smooth_reservoir_model(coord_sys,state_vector,time_symbol,compartmental_dyad,input_vector)' 
            ,func=functions.srm_from_B_u_tens
            ,description="""Produces a smoth reservoir model"""
        )
        ,Computer(
             'compartmental_matrix(compartmental_dyad,coord_sys)'
             ,func=lambda dyad,cs: express(dyad,cs).to_matrix(cs)
            ,description="""computes the matrix of the CompartmentalSystems with respect to the given coordinate frame"""
        )
        ,Computer(
             'smooth_model_run(smooth_reservoir_model,parameter_dictionary,start_vector,time_vector,function_dictionary)'
            ,SmoothModelRun
            ,description="""Creates a single instance of a SmoothModelRun"""
        )
})
