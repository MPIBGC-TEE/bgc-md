from sympy import symbols
from sympy.vector import CoordSysND,express,Vector,Dyadic,Number
# fixme mm:
# add this boilerplatecode automatically
def get_CooordSystem()->CoordSysND:
    vector_names=["e_vl","e_vw"]
    C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')
    return C

def get_InputVector()->Vector:
    C=get_CooordSystem()
    I_vl,I_vw= symbols("I_vl I_vw")
    I= I_vl*C.e_vl +I_vw*C.e_vw
    return I

def get_CompartmentalDyad()->Dyadic:
    C=get_CooordSystem()
    B=-1*( #Fake (diagonal) Tensor  
        (C.e_vl|C.e_vl)
       +(C.e_vw|C.e_vw)
    )
    return B

def get_stateVector()->Vector:
    C=get_CooordSystem()
    vl,vw,sf,ss,sm= symbols("vl vw sf ss sm")
    s=\
     vl*C.e_vl
    +vw*C.e_vw
    return s

def get_cumulative_Vegetation_Input()->Number:
    C=get_CooordSystem()
    I=get_InputVector()
    Icomp=express(I,C).to_matrix(C)  
    return sum(Icomp[0:2])
