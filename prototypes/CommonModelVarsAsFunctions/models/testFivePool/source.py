from sympy import symbols
from sympy.vector import CoordSysND,express
# fixme mm:
# add this boilerplatecode automatically
from bgc_md.ModelDescriptor import ModelDescriptor
def get_CooordSystem():
    vector_names=["e_vl","e_vw","e_sf","e_ss","e_sm"]
    C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')
    return C

def get_InputVector():
    C=get_CooordSystem()
    I_vl,I_vw= symbols("I_vl I_vw")
    I= I_vl*C.e_vl +I_vw*C.e_vw
    return I

def get_CompartmentalMatrix():
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
     vl*C.e_vl
    +vw*C.e_vw
    +sf*C.e_sf
    +ss*C.e_ss
    +sm*C.e_sm
    return s

def get_ModelDescriptor():
    I=get_InputVector()
    stateVector=get_stateVector()
    B=get_CompartmentalMatrix()
    md=ModelDescriptor.from_B_I(stateVector,B,I)
    return md

def get_cumulative_Vegetation_Input():
    C=get_CooordSystem()
    I=get_InputVector()
    Icomp=express(I,C).to_matrix(C)  
    return sum(Icomp[0:2])
