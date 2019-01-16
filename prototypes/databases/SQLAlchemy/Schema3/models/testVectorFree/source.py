from sympy import symbols
from sympy.vector import CoordSysND,express
# fixme mm:
# add this boilerplatecode automatically
from bgc_md.ModelDescriptor import ModelDescriptor
def get_CooordSystem():
    vector_names=["e_vl","e_vw"]
    C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')
    return C

def get_ExternalInputs():
    #C=get_CooordSystem()
    I_vl,I_vw= symbols("I_vl I_vw")
    return {
         vl:I_vl
        ,vw:I_vw
    }

def get_ExternalOutFluxes():
    vl,vw=get_stateVariableTuple()
    k_vl,k_vw= symbols("k_vl k_vw")
    return {
         vl:k_vl*vl
        ,vw:k_vw*vw
    }

def get_CompartmentalMatrix():
    C=get_CooordSystem()
    B=-1*( #Fake (diagonal) Tensor  
        (C.e_vl|C.e_vl)
       +(C.e_vw|C.e_vw)
    )
    return B

def get_stateVariableTuple():
    vl,vw = symbols("vl vw")
    return (vl,vw)

def get_ModelDescriptor():
    md=ModelDescriptor.from_Fluxes(
         get_ExternalInFlux()
        ,get_ExternalOutFluxes()
        ,get_InternalFluxes()
    )
    return md

#def get_cumulative_Vegetation_Input():
#    C=get_CooordSystem()
#    I=get_InputVector()
#    Icomp=express(I,C).to_matrix(C)  
#    return sum(Icomp[0:2])
