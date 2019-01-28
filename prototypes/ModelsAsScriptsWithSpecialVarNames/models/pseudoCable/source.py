from sympy import symbols,Symbol,Min,Max
from sympy.vector import CoordSysND,express
# fixme mm:
# add this boilerplatecode automatically
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from bgc_md.resolver import srm_from_B_u_tens
from bgc_md.DescribedSymbol import DesribedSymbol
from bgc_md.DescribedQuantity import DescribedQuantity
# all variables starting with def_  are 
from sympy import symbols,solve, pi, Eq ,Matrix, Function, Piecewise, exp
from sympy import pprint
from sympy.physics.units import mass,time
from sympy.physics.units import year,day,second,minute
from sympy.physics.units import meter, kilogram
from sympy.physics.units.dimensions import dimsys_SI
from sympy.physics.units import convert_to
class DerivedVariable:
    def __init__(self,expr:str):
        self.expr=expr
        

syms=leaf,fine_root,wood,metabolic_lit,structural_lit,cwd,fast_soil,slow_soil,passive_soil= symbols(" leaf \
        fine_root \
        wood \
        metabolic_lit \
        structural_lit \
        cwd \
        fast_soil \
        slow_soil \
        passive_soil")

t=Symbol('t')
vector_names=["e_"+str(sym) for sym in syms]
CoordS=CoordSysND(name="CoordS",vector_names=vector_names,transformation='cartesian')

(   
     r_lign_leaf 
    ,r_lign_fine_root
    ,f_lign_leaf 
    ,f_lign_wood
    ,clay
    ,silt
    ,q_10
    ,w_a
    ,w_b
    ,w_c
    ,w_d
    ,w_e
    ,m_sat
    ,xk_opt_litter
    ,xk_opt_soil
) =symbols((
    "r_lign_leaf"
    ,"r_lign_fine_root"
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
    
))
#xk_leaf_cold = Function("xk_leaf_cold")
xk_leaf_dry  = Function("xk_leaf_dry")  
btran= Function("btran")
T_air= Function("T_air")
T_soil=Function("T_soil")
ms= Function("ms")
xk_n_limit= Function("xk_n_limit")

mu_leaf=DescribedQuantity("mu_leaf")
mu_leaf.set_dimension(1/time,"SI")
mu_leaf.set_description("Turnover rate of plant pool Leaf" )

mu_fine_root=DescribedQuantity("mu_fine_root")
mu_fine_root.set_dimension(1/time,"SI")
mu_fine_root.set_description("Turnover rate of plant pool Root" )

mu_wood=DescribedQuantity("mu_wood")
mu_wood.set_dimension(1/time,"SI")
mu_wood.set_description("Turnover rate of plant pool Wood" )

I_leaf,I_wood= symbols("I_leaf I_wood")
I= I_leaf*CoordS.e_leaf +I_wood*CoordS.e_wood
fac_l=Max(0.001,0.85-0.018*r_lign_leaf)
fac_r=Max(0.001,0.85-0.018*r_lign_leaf)


# formulate as piecewise
xk_leaf_cold_max=Symbol('xk_leaf_cold_max')
T_shed=Symbol('T_shed')
xk_leaf_cold_exp=Symbol('xk_leaf_cold_exp')
xk_leaf_cold=Piecewise((xk_leaf_cold_max,T_air(t)< T_shed-5),(xk_leaf_cold_max*(1-(T_air(t)-T_shed+5)/5)**(xk_leaf_cold_exp),(T_air(t)>=T_shed-5) & (T_air(t)<=T_shed)),(0,T_air(t)>T_shed))

xk_leaf_dry_max=Symbol('xk_leaf_dry_max')
xk_leaf_dry_exp=Symbol('xk_leaf_dry_exp')
xk_leaf_dry=(xk_leaf_dry_max*(1-btran(ms(t)))**(xk_leaf_dry_exp))

xk_temp=q_10**((T_soil(t)-35)/10)

xk_water=((ms(t)/m_sat-w_b)/(w_a-w_b))**w_e * ((ms(t)/m_sat-w_c)/(w_a-w_c))**w_d

eps_leaf=1+xk_leaf_cold + xk_leaf_dry

#def xk_leaf_cold_num(T_air):
#    if T_air>T_shed:
#        ret=0
#    elif T_air < T_shed-5:
#        ret=xk_leaf_cold_max
#    else:
#        xk_leaf_cold_max*(1-(T_air-T_shed+5)/5)
#    return ret
    

A=(  fac_l                                          *(CoordS.e_metabolic_lit   |CoordS.e_leaf)
    +fac_r                                          *(CoordS.e_metabolic_lit   |CoordS.e_fine_root)
    +(1-fac_l)                                      *(CoordS.e_structural_lit  |CoordS.e_leaf)
    +(1-fac_r)                                      *(CoordS.e_structural_lit  |CoordS.e_fine_root)
    +1                                              *(CoordS.e_cwd             |CoordS.e_wood)
    +0.45                                           *(CoordS.e_fast_soil       |CoordS.e_metabolic_lit)
    +0.45*(1-f_lign_leaf)                           *(CoordS.e_fast_soil       |CoordS.e_structural_lit)
    +0.7 *(1-f_lign_leaf)                           *(CoordS.e_slow_soil       |CoordS.e_structural_lit)
    +0.4 *(1-f_lign_wood)                           *(CoordS.e_fast_soil       |CoordS.e_cwd)
    +0.7 *(1-f_lign_wood)                           *(CoordS.e_slow_soil       |CoordS.e_cwd)
    +(0.85-0.68*(clay+silt))*(0.997-0.032*clay)     *(CoordS.e_slow_soil       |CoordS.e_fast_soil)
    +(0.85-0.68*(clay+silt))*((1-0.997)-0.032*clay) *(CoordS.e_passive_soil    |CoordS.e_fast_soil)
    +0.45*((1-0.997)+0.009*clay)                    *(CoordS.e_passive_soil    |CoordS.e_slow_soil)
    -                                                (CoordS.e_leaf            |CoordS.e_leaf)
    -                                                (CoordS.e_fine_root       |CoordS.e_fine_root)
    -                                                (CoordS.e_wood            |CoordS.e_wood)
    -                                                (CoordS.e_metabolic_lit   |CoordS.e_metabolic_lit)
    -                                                (CoordS.e_structural_lit  |CoordS.e_structural_lit)
    -                                                (CoordS.e_cwd             |CoordS.e_cwd)
    -                                                (CoordS.e_fast_soil       |CoordS.e_fast_soil)
    -                                                (CoordS.e_slow_soil       |CoordS.e_slow_soil)
    -                                                (CoordS.e_passive_soil    |CoordS.e_passive_soil)) 
epsilon= (
     (1 +xk_leaf_cold+xk_leaf_dry)                              * (CoordS.e_leaf            |CoordS.e_leaf)
    + 1                                                         * (CoordS.e_fine_root       |CoordS.e_fine_root)
    + 1                                                         * (CoordS.e_wood            |CoordS.e_wood)
    + xk_opt_litter*xk_temp*xk_water*xk_n_limit(t)              * (CoordS.e_metabolic_lit   |CoordS.e_metabolic_lit)
    + xk_opt_litter*xk_temp*xk_water*xk_n_limit(t)*exp(-3*f_lign_leaf) 
                                                                * (CoordS.e_structural_lit  |CoordS.e_structural_lit)
    + xk_opt_litter*xk_temp*xk_water*xk_n_limit(t)              * (CoordS.e_cwd             |CoordS.e_cwd)
    + xk_opt_soil*xk_temp*xk_water*(1-0.75*(silt+clay))         * (CoordS.e_fast_soil       |CoordS.e_fast_soil)
    + xk_opt_soil*xk_temp*xk_water                              * (CoordS.e_slow_soil       |CoordS.e_slow_soil)
    + xk_opt_soil*xk_temp*xk_water                              * (CoordS.e_passive_soil    |CoordS.e_passive_soil)) 


Mepsilon=express(epsilon,CoordS).to_matrix(CoordS)
pprint(Mepsilon)

B=A


s=\
 leaf*CoordS.e_leaf\
+fine_root*CoordS.e_fine_root\
+wood*CoordS.e_wood\
+metabolic_lit *CoordS.e_metabolic_lit \
+structural_lit *CoordS.e_structural_lit \
+cwd *CoordS.e_cwd               \
+fast_soil*CoordS.e_fast_soil\
+slow_soil*CoordS.e_slow_soil\
+passive_soil*CoordS.e_passive_soil
    
MB=express(B,CoordS).to_matrix(CoordS)
#print("MB=")
#pprint(MB)
srm=srm_from_B_u_tens(CoordS,s,t,B,I)

Icomp=express(I,CoordS).to_matrix(CoordS)  
cvi=sum(Icomp[0:2])


# this dictionary will be analysed
special_vars={
    'coord_sys':CoordS #Coordinate syste
    ,'input_vector':I
    ,'compartmental_dyad':B
    ,'time_symbol':t
    ,'state_vector':s
    ,'smooth_reservoir_model':srm
    ,'u_func_phot':cvi
    ,'cyc_dyad':A
}

