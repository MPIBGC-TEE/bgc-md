
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
#from .ClassesStateLess import MVar3,Computer3
from .functions import srm_from_B_u_tens
from .IndexedSet import IndexedSet
from .MVar import MVar
from .Computer import Computer
#myMvars=frozenset({
#      MVar3('coord_sys') 
#    , MVar3('state_vector')
#    , MVar3('time_symbol') 
#    , MVar3('compartmental_dyad') 
#    , MVar3('input_vector') 
#    , MVar3('parameter_dictionary') 
#    , MVar3('start_vector') 
#    , MVar3('time_vector') 
#    , MVar3('function_dictionary')
#    , MVar3(
#            'smooth_reservoir_model'
#            ,computerNames=['srm_bu_tens']
#            ,description='A smooth reservroir Model'
#        )
#    , MVar3(
#            'smooth_model_run_dictionary'
#            ,computerNames=[] # at the moment empty list, consequently 
#            # only available when explicitly defined. 
#            # Although automatic computation would be simple 
#            # the keys make most sense if defined by the user
#            ,description= """
#            The dictionary values are SmoothModelRun objects. 
#            The keys can be used in user code to refer to special 
#            simulations. """
#    )
#    , MVar3(
#            'smooth_model_run'
#            ,computerNames=['smr']
#            ,description= """A single simulation"""
#    )
#})
#
#myComputers=frozenset({
#        Computer3(
#            'srm_bu_tens'
#            ,func=srm_from_B_u_tens
#            ,arg_names=[
#                 'coord_sys'
#                ,'state_vector' 
#                ,'time_symbol' 
#                ,'compartmental_dyad' 
#                ,'input_vector' 
#             ]
#            ,description="""Produces a smoth reservoir model"""
#        )
#        ,Computer3(
#             'smr'
#            ,SmoothModelRun
#            ,arg_names=[
#                 'smooth_reservoir_model'
#                ,'parameter_dictionary'
#                ,'start_vector'
#                ,'time_vector'
#                ,'function_dictionary'
#            ]
#            ,description="""Creates a single instance of a SmoothModelRun"""
#        )
#})
#p
Mvars=IndexedSet({
      MVar('coord_sys') 
    , MVar('state_vector')
    , MVar('time_symbol') 
    , MVar('compartmental_dyad') 
    , MVar('input_vector') 
    , MVar('parameter_dictionary') 
    , MVar('start_vector') 
    , MVar('time_vector') 
    , MVar('function_dictionary')
    , MVar(
            'smooth_reservoir_model'
            ,computerNames=['srm_bu_tens']
            ,description='A smooth reservroir Model'
        )
    , MVar(
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
    , MVar(
            'smooth_model_run'
            ,computerNames=['smr']
            ,description= """A single simulation"""
    )
})

Computers=IndexedSet({
        Computer(
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
        ,Computer(
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
