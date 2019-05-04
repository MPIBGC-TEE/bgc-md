
import unittest
from pathlib import Path
from testinfrastructure.helpers import pe
from testinfrastructure.InDirTest import InDirTest
#from sympy import Basic,Symbol,Matrix,symbols

#from sympy.vector import CoordSysND, Vector,express
#from bgc_md.prototype_helpers_script import get
from sympy import Symbol,Number
from sympy.vector import CoordSysND,express,Vector,Dyadic,matrix_to_vector
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
    , MVar('state_tuple')
    , MVar('time_symbol') 
    , MVar('compartmental_dyad') 
    , MVar('compartmental_matrix')
    , MVar('input_vector') 
    , MVar('input_tuple') 
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
             'compartmental_dyad(compartmental_matrix,coord_sys)'
             ,func=functions.dyad_from_matrix_and_coord_sys
            ,description="""computes the compartmental dyad from the matrix of components with respect to the given coordinate frame"""
        )
        ,Computer(
             'smooth_model_run(smooth_reservoir_model,parameter_dictionary,start_vector,time_vector,function_dictionary)'
            ,SmoothModelRun
            ,description="""Creates a single instance of a SmoothModelRun"""
        )
        ,Computer(
             'input_tuple(input_vector,coord_sys)'
             ,func=lambda vector,cs: express(vector,cs).to_matrix(cs)
            ,description="""Computes the components of the input vector with respect to the given coordinate system."""
        )
        ,Computer(
             'input_vector(input_tuple,coord_sys)'
             ,func=lambda mat,cs: matrix_to_vector(mat,cs)
            ,description="""Given a coordinate system and the tuple of components (1D Matrix) with respect to  this coord system,  computes the vector (sympy.vectorND) instance."""
        )
        ,Computer(
             'state_vector(state_tuple,coord_sys)'
             ,func=lambda mat,cs: matrix_to_vector(mat,cs)
            ,description="""Given a coordinate system and the tuple of the pool_names (1D Matrix) with respect to  this coord system,  computes the state vector (sympy.vectorND) instance."""
        )
        ,Computer(
             'state_tuple(state_vector,coord_sys)'
             ,func=lambda vector,cs: express(vector,cs).to_matrix(cs)
            ,description="""Computes the components of the state vector with respect to the given coordinate system."""
        )
})
