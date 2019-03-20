from sympy import Symbol,symbols,Number
from sympy.vector import CoordSysND,express,Vector,Dyadic
# fixme mm:
# add this boilerplatecode automatically
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun
from CompartmentalSystems.helpers_reservoir import numerical_function_from_expression
from bgc_md.resolver import srm_from_B_u_tens
from bgc_md.DescribedSymbol import DesribedSymbol
from bgc_md.DescribedQuantity import DescribedQuantity
# all variables starting with def_  are 
from sympy import Symbol,symbols,solve, pi, Eq, Min, Max ,Matrix, Function, Piecewise, exp
from sympy import pprint
from sympy.physics.units import mass,time
from sympy.physics.units import year,day,second,minute
from sympy.physics.units import meter, kilogram
from sympy.physics.units.dimensions import dimsys_SI
from sympy.physics.units import convert_to
from numpy import linspace,array
from pathlib import Path
import csv
# local imports
from allocationFractions import bvec_leaf_num,bvec_wood_num,bvec_fine_root_num
from interpolationFunctions import timeLine2
from cable_dict import cable_dict
from interpolationFunctions import cable_sols_by_name
state_vector_syms=leaf,fine_root,wood,metabolic_lit,structural_lit,cwd,fast_soil,slow_soil,passive_soil= symbols(" leaf \
        fine_root \
        wood \
        metabolic_lit \
        structural_lit \
        cwd \
        fast_soil \
        slow_soil \
        passive_soil")

t=Symbol('t')
vector_names=["e_"+str(sym) for sym in state_vector_syms]
CoordS=CoordSysND(name="CoordS",vector_names=vector_names,transformation='cartesian')

symNames=[
    "r_lign_leaf"
    ,"r_lign_fine_root"
    ,"f_lign_fine_root"
    ,"f_lign_leaf"
    ,"f_lign_wood"
    ,"clay"
    ,"silt"
    ,"q_10"
    ,"w_a"
    ,"w_b"
    ,"w_c"
    ,"w_d"
    ,"w_e"
    ,"m_sat"
    ,"xk_opt_litter"
    ,"xk_opt_soil"
    ,"sla"
    ,"b_leaf"
    ,"b_wood"
    ,"b_fine_root"
    ,"glaimax"
    ,"phase_2"
    ,"planttype"
    ,"kleaf"
    ,"kwood"
    ,"kfroot"
    ,"kmet"
    ,"kstr"
    ,"kcwd"
    ,"kfast"
    ,"kslow"
    ,"kpass"
]
for name in symNames:
    exec("{0}=Symbol('{0}')".format(name))
#xk_leaf_cold = Function("xk_leaf_cold")
xk_leaf_dry  = Function("xk_leaf_dry")  
btran= Function("btran")
T_air= Function("T_air")
T_soil=Function("T_soil")
bvec_leaf=Function("bvec_leaf")
bvec_fine_root=Function("bvec_fine_root")
bvec_wood=Function("bvec_wood")


ms= Function("ms")
xk_n_limit= Function("xk_n_limit")
Npp = Function("Npp")
phase= Function("phase")

r_leaf=Function('r_leaf')
r_fine_root=Function('r_fine_root')
r_wood=Function('r_wood')


# allocation fraction bvec_leaf, bvec_wood and bvec_fine_root are from casa_cnp.F90: Line 250, Line 307-358; casa_inout.F90: Line 112-118
I_leaf=Npp(t)*bvec_leaf(leaf ,wood ,fine_root ,r_leaf(t) ,r_wood(t) ,r_fine_root(t) ,Npp(t) ,phase(t) ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype)
I_wood=Npp(t)*bvec_wood(leaf ,wood ,fine_root ,r_leaf(t) ,r_wood(t) ,r_fine_root(t) ,Npp(t) ,phase(t) ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype)
I_fine_root=Npp(t)*bvec_fine_root(leaf ,wood ,fine_root ,r_leaf(t) ,r_wood(t) ,r_fine_root(t) ,Npp(t) ,phase(t) ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype)

#NPP(t) = GPP(t) - Cplant * resipiration rate(T_air) , casa_cnp.F90 Line 1191-1192, Autotrophic respiration: casa_cnp.F90 Line 524-736, casa_inout.F90 Line 1368
#GPP is based on photosynthesis rate A (cable_canopy.F90 Line 1772-1780, Line 2005-2219). anxz = MIN(anrubiscoz,anrubpz,ansinkz) 

I=(I_leaf*CoordS.e_leaf 
    +I_wood*CoordS.e_wood
    +I_fine_root*CoordS.e_fine_root)

#fraction from plant to different litter pools: casa_cnp.F90 Line 969, 970
fac_l=Max(0.001,0.85-0.018*r_lign_leaf)
fac_r=Max(0.001,0.85-0.018*r_lign_fine_root)


# formulate as piecewise
xk_leaf_cold_max=Symbol('xk_leaf_cold_max')
T_shed=Symbol('T_shed')
xk_leaf_cold_exp=Symbol('xk_leaf_cold_exp')
#xk_leaf_cold is temperature scalar for leaf: casa_cnp.F90 Line 785-787
xk_leaf_cold=Piecewise(
         (xk_leaf_cold_max,T_air(t)< T_shed-5)
        ,(xk_leaf_cold_max*(1-(T_air(t)-T_shed+5)/5)**(xk_leaf_cold_exp)
        ,(T_air(t)>=T_shed-5) & (T_air(t)<=T_shed))
        ,(0,T_air(t)>T_shed)
)

xk_leaf_dry_max=Symbol('xk_leaf_dry_max')
xk_leaf_dry_exp=Symbol('xk_leaf_dry_exp')
#xk_leaf_dry is water scalar for leaf: casa_cnp.F90 Line 788-790
xk_leaf_dry=(xk_leaf_dry_max*(1-btran(t))**(xk_leaf_dry_exp))

xk_temp=q_10**((T_soil(t)-35-273.15)/10) # Temperature scalar for litter and soil: casa_cnp.F90 Line 875

xk_water=((ms(t)/m_sat-w_b)/(w_a-w_b))**w_e * ((ms(t)/m_sat-w_c)/(w_a-w_c))**w_d # Water scalar for litter and soil: casa_cnp.F90 Line 876-877

eps_leaf=1 + xk_leaf_cold/kleaf + xk_leaf_dry/kleaf # Leaf environmental scalar: casa_cnp.F90 Line 975-976

#def xk_leaf_cold_num(T_air):
#    if T_air>T_shed:
#        ret=0
#    elif T_air < T_shed-5:
#        ret=xk_leaf_cold_max
#    else:
#        xk_leaf_cold_max*(1-(T_air-T_shed+5)/5)
#    return ret
    

A=(  fac_l                                          *(CoordS.e_metabolic_lit   |CoordS.e_leaf)           # casacnp.F90: Line 969
    +fac_r                                          *(CoordS.e_metabolic_lit   |CoordS.e_fine_root)      # casacnp.F90: Line 970
    +(1-fac_l)                                      *(CoordS.e_structural_lit  |CoordS.e_leaf)           # casacnp.F90: Line 971
    +(1-fac_r)                                      *(CoordS.e_structural_lit  |CoordS.e_fine_root)      # casacnp.F90: Line 972
    +1                                              *(CoordS.e_cwd             |CoordS.e_wood)           # casacnp.F90: Line 973
    +0.45                                           *(CoordS.e_fast_soil       |CoordS.e_metabolic_lit)  # casacnp.F90: Line 1051
    +0.45* (1-f_lign_leaf)                          *(CoordS.e_fast_soil       |CoordS.e_structural_lit) # casacnp.F90: Line 1053
    +0.7 * f_lign_leaf                              *(CoordS.e_slow_soil       |CoordS.e_structural_lit) # casacnp.F90: Line 1055
    +0.4 * (1-f_lign_wood)                          *(CoordS.e_fast_soil       |CoordS.e_cwd)            # casacnp.F90: Line 1057
    +0.7 * f_lign_wood                              *(CoordS.e_slow_soil       |CoordS.e_cwd)            # casacnp.F90: Line 1059
    +(0.85-0.68*(clay+silt))*(0.997-0.032*clay)     *(CoordS.e_slow_soil       |CoordS.e_fast_soil)      # casacnp.F90: Line 1066
    +(0.85-0.68*(clay+silt))*((1-0.997)+0.032*clay) *(CoordS.e_passive_soil    |CoordS.e_fast_soil)      # casacnp.F90: Line 1068
    +0.45*((1-0.997)+0.009*clay)                    *(CoordS.e_passive_soil    |CoordS.e_slow_soil)      # casacnp.F90: Line 1070
    -                                                (CoordS.e_leaf            |CoordS.e_leaf)
    -                                                (CoordS.e_fine_root       |CoordS.e_fine_root)
    -                                                (CoordS.e_wood            |CoordS.e_wood)
    -                                                (CoordS.e_metabolic_lit   |CoordS.e_metabolic_lit)
    -                                                (CoordS.e_structural_lit  |CoordS.e_structural_lit)
    -                                                (CoordS.e_cwd             |CoordS.e_cwd)
    -                                                (CoordS.e_fast_soil       |CoordS.e_fast_soil)
    -                                                (CoordS.e_slow_soil       |CoordS.e_slow_soil)
    -                                                (CoordS.e_passive_soil    |CoordS.e_passive_soil)
) 

epsilon_leaf=(1 +xk_leaf_cold/kleaf+xk_leaf_dry/kleaf) # Leaf environmental scalar: casa_cnp.F90 Line 975-976
epsilon= (
     epsilon_leaf                                         * (CoordS.e_leaf            |CoordS.e_leaf)          # casa_cnp.F90: Line 975-976
    + 1                                                   * (CoordS.e_fine_root       |CoordS.e_fine_root)     # casa_cnp.F90: Line 978
    + 1                                                   * (CoordS.e_wood            |CoordS.e_wood)          # casa_cnp.F90: Line 979
    + xk_opt_litter*xk_temp*xk_water*xk_n_limit(t)        * (CoordS.e_metabolic_lit   |CoordS.e_metabolic_lit) # casa_cnp.F90: Line 880, 1030
    + xk_opt_litter*xk_temp*xk_water*xk_n_limit(t)*exp(-3*f_lign_leaf)                                         # casa_cnp.F90: Line 880, 1031-1032
                                                          * (CoordS.e_structural_lit  |CoordS.e_structural_lit)
    + xk_opt_litter*xk_temp*xk_water*xk_n_limit(t)        * (CoordS.e_cwd             |CoordS.e_cwd)           # casa_cnp.F90: Line 880, 1033
    + xk_opt_soil*xk_temp*xk_water*(1-0.75*(silt+clay))   * (CoordS.e_fast_soil       |CoordS.e_fast_soil)     # casa_cnp.F90: Line 884, 1035-1036
    + xk_opt_soil*xk_temp*xk_water                        * (CoordS.e_slow_soil       |CoordS.e_slow_soil)     # casa_cnp.F90: Line 884, 1037
    + xk_opt_soil*xk_temp*xk_water                        * (CoordS.e_passive_soil    |CoordS.e_passive_soil)  # casa_cnp.F90: Line 884, 1038
) 
test_expr=epsilon_leaf*kleaf

delta_xleaf=Npp(t)*bvec_leaf(leaf ,wood ,fine_root ,r_leaf(t) ,r_wood(t) ,r_fine_root(t) ,Npp(t) ,phase(t) ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype)-kleaf*epsilon_leaf*leaf

k=(   kleaf       * (CoordS.e_leaf            |CoordS.e_leaf)
    + kfroot      * (CoordS.e_fine_root       |CoordS.e_fine_root)
    + kwood       * (CoordS.e_wood            |CoordS.e_wood)
    + kmet        * (CoordS.e_metabolic_lit   |CoordS.e_metabolic_lit)
    + kstr        * (CoordS.e_structural_lit  |CoordS.e_structural_lit)
    + kcwd        * (CoordS.e_cwd             |CoordS.e_cwd)
    + kfast       * (CoordS.e_fast_soil       |CoordS.e_fast_soil)
    + kslow       * (CoordS.e_slow_soil       |CoordS.e_slow_soil)
    + kpass       * (CoordS.e_passive_soil    |CoordS.e_passive_soil) 
)

Mepsilon=express(epsilon,CoordS).to_matrix(CoordS)

B=A.dot(k.dot(epsilon))
s=(
     leaf					*CoordS.e_leaf
    +fine_root				*CoordS.e_fine_root
    +wood					*CoordS.e_wood
    +metabolic_lit 			*CoordS.e_metabolic_lit 
    +structural_lit 		*CoordS.e_structural_lit 
    +cwd 					*CoordS.e_cwd               
    +fast_soil				*CoordS.e_fast_soil
    +slow_soil				*CoordS.e_slow_soil
    +passive_soil			*CoordS.e_passive_soil
)  
#vector_names=["e_vl","e_vw"]
#C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')

#I_vl,I_vw= symbols("I_vl I_vw")
#I= I_vl*C.e_vl +I_vw*C.e_vw

#B=-1*( #Fake (diagonal) Tensor  
#    (C.e_vl|C.e_vl)
#   +(C.e_vw|C.e_vw)
#)

#vl,vw,sf,ss,sm= symbols("vl vw sf ss sm")
#s=\
# vl*C.e_vl\
#+vw*C.e_vw\

time_symbol=Symbol('t')
#Icomp=express(I,C).to_matrix(C)  
Icomp=express(I,CoordS).to_matrix(CoordS)  
cvi=sum(Icomp[0:2])
# this dictionary will be analysed the keys have special meaning
special_vars={
    'coord_sys':CoordS #Coordinate syste
    ,'input_vector':I
    ,'compartmental_dyad':B
    ,'time_symbol':time_symbol
    ,'state_vector':s
    ,'cumulative_vegetation_input':cvi
}
