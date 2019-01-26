from sympy import symbols
from sympy.vector import CoordSysND,express
# fixme mm:
# add this boilerplatecode automatically
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from bgc_md.prototype_helpers import srm_from_B_u_tens

def get_CooordSystem():
    vector_names=["e_vl","e_vw","e_sf","e_ss","e_sm"]
    C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')
    return C

def get_InputVector():
    C=get_CooordSystem()
    I_vl,I_vw= symbols("I_vl I_vw")
    I= I_vl*C.e_vl +I_vw*C.e_vw
    return I

def get_CompartmentalDyad():
    C=get_CooordSystem()
    B=-1*( #Fake (diagonal) Tensor  
        (C.e_vl|C.e_vl)
       +(C.e_vw|C.e_vw)
       +(C.e_sf|C.e_sf)
       +(C.e_ss|C.e_ss)
       +(C.e_sm|C.e_sm)
    )
    return B

def get_stateVector():
    C=get_CooordSystem()
    vl,vw,sf,ss,sm= symbols("vl vw sf ss sm")
    s=\
     vl*C.e_vl\
    +vw*C.e_vw\
    +sf*C.e_sf\
    +ss*C.e_ss\
    +sm*C.e_sm
    return s

def time_symbol():
    return Symbol('t')

def get_SmoothReservoirModel():
    C=get_CooordSystem()
    u=get_InputVector()
    stateVector=get_stateVector()
    B=get_CompartmentalDyad()
    md=srm_from_B_u_tens(C,stateVector,time_symbol,B,u)
    return md

def get_cumulative_Vegetation_Input():
    C=get_CooordSystem()
    I=get_InputVector()
    Icomp=express(I,C).to_matrix(C)  
    return sum(Icomp[0:2])
