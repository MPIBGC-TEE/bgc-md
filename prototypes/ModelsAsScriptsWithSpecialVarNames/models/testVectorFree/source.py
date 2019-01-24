from sympy import symbols
from sympy.vector import CoordSysND,express
# fixme mm:
# add this boilerplatecode automatically
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel 

#C=get_CooordSystem()
I_vl,I_vw= symbols("I_vl I_vw")
InFluxes:dict={
     vl:I_vl
    ,vw:I_vw
}

vl,vw = symbols("vl vw")
k_vl,k_vw= symbols("k_vl k_vw")

OutFluxes:dict={
     vl:k_vl*vl
    ,vw:k_vw*vw
}

k_vl,k_vw= symbols("k_lw k_wl")
# the keys of the internal flux dictionary are tuples (source_pool,target_pool)
InternalFluxes():dict={
     (vl,vw):k_vl*vl
    ,(vw,vl):k_vw*vw
}


srm=SmoothReservoirModel.from_state_variable_indexed_fluxes(
     InFluxes
    ,OutFluxes
    ,InternalFluxes
)

#def get_cumulative_Vegetation_Input():
#    C=get_CooordSystem()
#    I=get_InputVector()
#    Icomp=express(I,C).to_matrix(C)  
#    return sum(Icomp[0:2])

specialVars={
    'InFluxes': InFluxes #Coordinate syste
    ,'OutFluxes':OutFluxes
    ,'time_symbol':time_symbol
    ,'stateVariableTupel':(vl,vw)
    ,'SmoothReservoirModel':srm
}
