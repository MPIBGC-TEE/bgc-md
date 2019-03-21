from sympy import Symbol,Number
from sympy.vector import CoordSysND,express,Vector,Dyadic
from typing import List
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
#from CompartmentalSystems import smooth_reservoir_model 
from testinfrastructure.helpers import pe
from ..Classes import MVar,Computer

# first define some functions

def srm_from_B_u_tens(
    # fixme mm 21.03 2019
    # This should become an alternative constructor (@classmethod) 
    # for CompartmetalSystems.SmoothReservoirModel
    # It is still here because it requires our special branch of sympy
    # and CompartmentalSystems should not suffer from this dependency
    
        C:CoordSysND
        ,state_vector:Vector
        ,time_symbol:Symbol
        ,B:Dyadic
        ,u:Vector
    )->'SmoothReservoirModel':
    state_vector_mat=express(state_vector,C).to_matrix(C)
    B_mat=express(B,C).to_matrix(C)
    u_mat=express(u,C).to_matrix(C)
    return SmoothReservoirModel.from_B_u(state_vector_mat,time_symbol,B_mat,u_mat)

srm_bu_tens=Computer(
    func=srm_from_B_u_tens
    ,args=[
         MVar(name='coord_sys') 
        ,MVar(name='state_vector') 
        ,MVar(name='time_symbol') 
        ,MVar(name='compartmental_dyad') 
        ,MVar(name='input_vector') 
     ]
    ,description="""Produces a smoth reservoir model"""

)
