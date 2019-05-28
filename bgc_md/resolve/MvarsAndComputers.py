
import unittest
from pathlib import Path
from testinfrastructure.helpers import pe
from testinfrastructure.InDirTest import InDirTest
#from sympy import Basic,Symbol,Matrix,symbols

#from sympy.vector import CoordSysND, Vector,express
#from bgc_md.prototype_helpers_script import get
import numpy as np
from sympy import Symbol,Number
from sympy.vector import CoordSysND,express,Vector,Dyadic,matrix_to_vector
from typing import List
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun
#from CompartmentalSystems import smooth_reservoir_model 
#from .ClassesStateLess import MVar3,Computer3
from bgc_md.reports import produce_model_report_markdown, produce_model_report_markdown_directory,  defaults,render
from . import functions 
from .IndexedSet import IndexedSet
from .MVar import MVar
from .Computer import Computer
Mvars=IndexedSet({
      MVar('coord_sys') 
    , MVar('example_MVar',description='A variable used in the tests to show how to extend the framework')
    , MVar('state_vector')
    , MVar('documented_identifiers_table')
    , MVar('documented_identifiers')
    , MVar('state_tuple')
    , MVar('time_symbol') 
    , MVar('compartmental_dyad') 
    , MVar('compartmental_matrix')
    , MVar('vegetation_base_vector_list') 
    , MVar('vegetation_cycling_matrix') 
    , MVar('soil_matrix') 
    , MVar('soil_scaling_matrix_xi') 
    , MVar('soil_decomposition_matrix_N') 
    , MVar('soil_transport_matrix_T') 
    , MVar('vegetation_to_soil_matrix') 
    , MVar('soil_to_vegetation_matrix') 
    , MVar('soil_base_vector_list') 
    , MVar('input_vector') 
    , MVar('input_tuple') 
    , MVar('carbon_allocation_tuple') 
    , MVar('relative_carbon_allocation_tuple') 
    , MVar('total_carbon_allocation') 
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
        Computer('soil_scaling_matrix_xi(smooth_reservoir_model)' 
            ,func=lambda srm : srm.xi_T_N_u_representation()[0]
            ,description="""Computes T of the SoilModel normal form B=xi*T*N"""
        )
        ,Computer('soil_transport_matrix_T(smooth_reservoir_model)' 
            ,func=lambda srm : srm.xi_T_N_u_representation()[1]
            ,description="""Computes T of the SoilModel normal form B=xi*T*N"""
        )
        ,Computer('soil_decomposition_matrix_N(smooth_reservoir_model)' 
            ,func=lambda srm : srm.xi_T_N_u_representation()[2]
            ,description="""Computes N of the SoilModel normal form B=xi*T*N"""
        )
        ,Computer('smooth_reservoir_model(coord_sys,state_vector,time_symbol,compartmental_dyad,input_vector)' 
            ,func=functions.srm_from_B_u_tens
            ,description="""Produces a smoth reservoir model"""
        )
        ,Computer('coord_sys(state_tuple)' 
            ,func=functions.default_coordinate_system
            ,description="""Produces a smoth reservoir model"""
        )
        ,Computer(
             'compartmental_matrix(compartmental_dyad,coord_sys)'
             ,func=lambda dyad,cs: express(dyad,cs).to_matrix(cs)
            ,description="""computes the matrix of the CompartmentalSystems with respect to the given coordinate frame"""
        )

        ,Computer(
             'vegetation_cycling_matrix(compartmental_dyad,vegetation_base_vector_list)'
             ,func=functions.matrix_from_dyad_and_vector_list
            ,description="""computes the block matrix V2V of the CompartmentalSystems desribing the transport from vegegetation to vegetation pools.
            . 
            v  = V2V   S2V
            s    V2S   S2S
            """
        )
        ,Computer(
             'vegetation_to_soil_matrix(compartmental_dyad,soil_base_vector_list,vegetation_base_vector_list)'
             ,func=functions.matrix_from_dyad_and_vector_lists
            ,description="""computes the block matrix V2S describing transport of material from vegetation to soil pools
            . 
            v  = V2V   S2V
            s    V2S   S2S
            """
        )
        ,Computer(
             'soil_to_vegetation_matrix(compartmental_dyad,vegetation_base_vector_list,soil_base_vector_list)'
             ,func=functions.matrix_from_dyad_and_vector_lists
            ,description="""
            computes the block matrix S2V of transports from soil to vegetation pools 
            . 
            v  = V2V   S2V
            s    V2S   S2S
            """
        )
        ,Computer(
             'soil_matrix(compartmental_dyad,soil_base_vector_list)'
             ,func=functions.matrix_from_dyad_and_vector_list
            ,description="""
            computes the block matrix S2S describing transports from soil to soil pools 
            . 
            v  = V2V   S2V
            s    V2S   S2S
            """
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
        ,Computer(
             'total_carbon_allocation(carbon_allocation_tuple)'
             ,func=lambda arr: np.sum(arr)
            ,description="""Computes the combined carbon input to vegetation pools."""
        )
        ,Computer(
             'relative_carbon_allocation_tuple(carbon_allocation_tuple,total_carbon_allocation)'
             ,func=lambda arr,tot: arr/tot
            ,description="""Computes the projections of the input vector to a list of vectors that represent vegetation pools."""
        )
        ,Computer(
             'carbon_allocation_tuple(input_vector,vegetation_base_vector_list)'
             ,func=lambda iv,l: np.array([iv.dot(bv) for bv in l])
            ,description="""Computes the projections of the input vector to a list of vectors that represent vegetation pools."""
        )
        # reports are also 'computed' and their availability depends on the 
        # the ohter MVars given. It makes sense to check if they can be
        # created 
        ,Computer(
             'documented_identifiers_table(documented_identifiers)'
             ,func=lambda l:render(
                 defaults()['paths']['static_report_templates'].joinpath('documented_identifiers.py')
                 ,l
                 )
            ,description="""creates a ReportElementList instance for
            the variables reported in the namespace"""
        )
})
