from sympy import symbols
from sympy.vector import CoordSysND,express
# fixme mm:
# add this boilerplatecode automatically
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel 

def get_InFluxes()->dict:
    #C=get_CooordSystem()
    I_vl,I_vw= symbols("I_vl I_vw")
    return {
         vl:I_vl
        ,vw:I_vw
    }

def get_OutFluxes()->dict:
    vl,vw=get_stateVariableTuple()
    k_vl,k_vw= symbols("k_vl k_vw")
    return {
         vl:k_vl*vl
        ,vw:k_vw*vw
    }

def get_InternalFluxes()->dict:
    vl,vw=get_stateVariableTuple()
    k_vl,k_vw= symbols("k_lw k_wl")
    # the keys of the internal flux dictionary are tuples (source_pool,target_pool)
    return {
         (vl,vw):k_vl*vl
        ,(vw,vl):k_vw*vw
    }

def get_StateVariableTuple()->tuple:
    vl,vw = symbols("vl vw")
    return (vl,vw)

def get_SmoothReservoirModel():
    md=SmoothReservoirModel.from_state_variable_indexed_fluxes(
         get_InFlux()
        ,get_OutFluxes()
        ,get_InternalFluxes()
    )
    return md

#def get_cumulative_Vegetation_Input():
#    C=get_CooordSystem()
#    I=get_InputVector()
#    Icomp=express(I,C).to_matrix(C)  
#    return sum(Icomp[0:2])
