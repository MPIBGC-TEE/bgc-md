from sympy import symbols,Symbol
from sympy.vector import CoordSysND,express
# fixme mm:
# add this boilerplatecode automatically
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from bgc_md.resolver import srm_from_B_u_tens
# all variables starting with def_  are 

vector_names=["e_vl","e_vw","e_sf","e_ss","e_sm"]
C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')

I_vl,I_vw= symbols("I_vl I_vw")
I= I_vl*C.e_vl +I_vw*C.e_vw

B=-1*( #Fake (diagonal) Tensor  
    (C.e_vl|C.e_vl)
   +(C.e_vw|C.e_vw)
   +(C.e_sf|C.e_sf)
   +(C.e_ss|C.e_ss)
   +(C.e_sm|C.e_sm)
)

vl,vw,sf,ss,sm= symbols("vl vw sf ss sm")
s=\
 vl*C.e_vl\
+vw*C.e_vw\
+sf*C.e_sf\
+ss*C.e_ss\
+sm*C.e_sm


time_symbol=Symbol('t')
srm=srm_from_B_u_tens(C,s,time_symbol,B,I)

Icomp=express(I,C).to_matrix(C)  
cvi=sum(Icomp[0:2])


# this dictionary will be analysed
special_vars={
    'coord_sys':C #Coordinate syste
    ,'input_vector':I
    ,'compartmental_dyad':B
    ,'time_symbol':time_symbol
    ,'state_vector':s
    ,'smooth_reservoir_model':srm
    ,'u_func_phot':cvi
}

