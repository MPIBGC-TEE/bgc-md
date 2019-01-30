from sympy import Symbol,symbols,Number
from sympy.vector import CoordSysND,express,Vector,Dyadic
# fixme mm:
# add this boilerplatecode automatically
vector_names=["e_vl","e_vw"]
C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')

I_vl,I_vw= symbols("I_vl I_vw")
I= I_vl*C.e_vl +I_vw*C.e_vw

B=-1*( #Fake (diagonal) Tensor  
    (C.e_vl|C.e_vl)
   +(C.e_vw|C.e_vw)
)

vl,vw,sf,ss,sm= symbols("vl vw sf ss sm")
s=\
 vl*C.e_vl\
+vw*C.e_vw\

time_symbol=Symbol('t')
Icomp=express(I,C).to_matrix(C)  
cvi=sum(Icomp[0:2])
# this dictionary will be analysed the keys have special meaning
special_vars={
    'coord_sys':C #Coordinate syste
    ,'input_vector':I
    ,'compartmental_dyad':B
    ,'time_symbol':time_symbol
    ,'state_vector':s
    ,'cumulative_vegetation_input':cvi
}