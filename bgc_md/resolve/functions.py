
from sympy import Symbol,Number
from sympy.vector import CoordSysND,express,Vector,Dyadic
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
def srm_from_B_u_tens(
    # fixme mm 21.03 2019
    # This could become an alternative constructor (@classmethod) 
    # for CompartmetalSystems.SmoothReservoirModel
    # It is still here because it requires our special branch of sympy
    # and CompartmentalSystems should not suffer from this dependency
    # on the other hand Compartmental systems does not care about tensors
    # and vectors and does not have to. So it would also make sense to
    # keep the conversion code out of it.
    
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
