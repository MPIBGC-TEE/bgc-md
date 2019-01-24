from sympy import symbols,Symbol
from sympy.vector import CoordSysND,express
# fixme mm:
# add this boilerplatecode automatically
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from bgc_md.resolver import srm_from_B_u_tens
from bgc_md.DescribedSymbol import DesribedSymbol
from bgc_md.DescribedQuantity import DescribedQuantity
# all variables starting with def_  are 
from sympy import symbols,solve, pi, Eq ,Matrix
from sympy.physics.units import mass,time
from sympy.physics.units import year,day,second,minute
from sympy.physics.units import meter, kilogram
from sympy.physics.units.dimensions import dimsys_SI
from sympy.physics.units import convert_to


vector_names=["e_C_leaf","e_C_root","e_C_wood","e_sf","e_ss","e_sm"]
C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')

mu_leaf=DescribedQuantity("mu_leaf")
mu_leaf.set_dimension(1/time,"SI")
mu_leaf.set_description("Turnover rate of plant pool Leaf" )

mu_root=DescribedQuantity("mu_root")
mu_root.set_dimension(1/time,"SI")
mu_root.set_description("Turnover rate of plant pool Root" )

mu_wood=DescribedQuantity("mu_wood")
mu_wood.set_dimension(1/time,"SI")
mu_wood.set_description("Turnover rate of plant pool Wood" )

I_C_leaf,I_C_wood= symbols("I_C_leaf I_C_wood")
I= I_C_leaf*C.e_C_leaf +I_C_wood*C.e_C_wood

#Fake the soil(diagonal) Tensor  
A=( 
   -mu_leaf*(C.e_C_leaf|C.e_C_leaf)
   -mu_root*(C.e_C_root|C.e_C_root)
   -mu_wood*(C.e_C_wood|C.e_C_wood)
)
D= (
   -(C.e_sf|C.e_sf)
   -(C.e_ss|C.e_ss)
   -(C.e_sm|C.e_sm)
)
B=A+D

C_leaf,C_root,C_wood,sf,ss,sm= symbols("C_leaf C_root C_wood sf ss sm")
s=\
 C_leaf*C.e_C_leaf\
+C_root*C.e_C_root\
+C_wood*C.e_C_wood\
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
    ,'cyc_dyad':A
}

