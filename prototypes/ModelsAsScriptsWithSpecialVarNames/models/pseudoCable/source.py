from sympy.vector import CoordSysND,express
# fixme mm:
# add this boilerplatecode automatically
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun
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
from interpolationFunctions import timeLine

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
    ,sla
    ,b_leaf
    ,b_wood
    ,b_fine_root
    ,glaimax
    ,phase_2
    ,planttype
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
    ,"sla"
    ,"b_leaf"
    ,"b_wood"
    ,"b_fine_root"
    ,"glaimax"
    ,"phase_2"
    ,"planttype"
))
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



mu_leaf=DescribedQuantity("mu_leaf")
mu_leaf.set_dimension(1/time,"SI")
mu_leaf.set_description("Turnover rate of plant pool Leaf" )

mu_fine_root=DescribedQuantity("mu_fine_root")
mu_fine_root.set_dimension(1/time,"SI")
mu_fine_root.set_description("Turnover rate of plant pool Root" )

mu_wood=DescribedQuantity("mu_wood")
mu_wood.set_dimension(1/time,"SI")
mu_wood.set_description("Turnover rate of plant pool Wood" )

I_leaf=Npp(t)*bvec_leaf(leaf ,wood ,fine_root ,r_leaf(t) ,r_wood(t) ,r_fine_root(t) ,Npp(t) ,phase(t) ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype)
I_wood=Npp(t)*bvec_wood(leaf ,wood ,fine_root ,r_leaf(t) ,r_wood(t) ,r_fine_root(t) ,Npp(t) ,phase(t) ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype)
I_fine_root=Npp(t)*bvec_fine_root(leaf ,wood ,fine_root ,r_leaf(t) ,r_wood(t) ,r_fine_root(t) ,Npp(t) ,phase(t) ,glaimax ,b_leaf ,b_fine_root ,b_wood ,sla,planttype)

I=(I_leaf*CoordS.e_leaf 
    +I_wood*CoordS.e_wood
    +I_fine_root*CoordS.e_fine_root)

fac_l=Max(0.001,0.85-0.018*r_lign_leaf)
fac_r=Max(0.001,0.85-0.018*r_lign_fine_root)


# formulate as piecewise
xk_leaf_cold_max=Symbol('xk_leaf_cold_max')
T_shed=Symbol('T_shed')
xk_leaf_cold_exp=Symbol('xk_leaf_cold_exp')
xk_leaf_cold=Piecewise(
         (xk_leaf_cold_max,T_air(t)< T_shed-5)
        ,(xk_leaf_cold_max*(1-(T_air(t)-T_shed+5)/5)**(xk_leaf_cold_exp)
        ,(T_air(t)>=T_shed-5) & (T_air(t)<=T_shed))
        ,(0,T_air(t)>T_shed)
)

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

B=A.dot(epsilon)
#B=A


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
srm=srm_from_B_u_tens(CoordS,s,t,B,I)

Icomp=express(I,CoordS).to_matrix(CoordS)  
cvi=sum(Icomp[0:2])
# read part of the parameterdict from a file

with Path('Tumbarumba/T_independent/soilscalar.txt').open() as f:
    r=csv.DictReader(f,delimiter=",")
    lindicts=[row for row in r]
cable_soil={key.strip():val for key,val in lindicts[0].items()}

with Path('Tumbarumba/T_independent/vegpara.txt').open(newline='') as f:
    r=csv.DictReader(f,delimiter=",")
    vlindicts=[row for row in r]
cable_veg={key.strip():val for key,val in vlindicts[0].items()}

# we translate the cable param names to ours
par_dict={
     clay:cable_soil['soil%clay']
    ,f_lign_leaf:cable_veg['fracLigninleaf']
    ,f_lign_wood:cable_veg['fracLigninfroot']
    ,r_lign_leaf:cable_veg['ratioLigninleaf']
    ,r_lign_fine_root:cable_veg['ratioLigninfroot']
    ,silt:cable_soil['soil%silt']
    ,sla:cable_veg['sla']
    ,glaimax:cable_veg['glaimax']
    ,b_wood:cable_veg['b_wood']
    ,b_leaf:cable_veg['b_leaf']
    ,b_fine_root:cable_veg['b_fine_root']
    ,planttype:cable_veg['planttype']
	,xk_leaf_dry_max:cable_soil['xkleafdrymax']
	,T_shed:cable_soil['phen%TKshed']
	,xk_leaf_cold_exp:cable_soil['xkleafcoldexp']
    ,xk_opt_soil:cable_soil['xkoptsoil']
	,xk_leaf_cold_max:cable_soil['xkleafcoldmax']
	,q_10:cable_soil['q10soil']
	,xk_leaf_dry_exp:cable_soil['xkleafdryexp']
	,w_a:cable_soil['wfpscoefa']
	,w_b:cable_soil['wfpscoefb']
	,w_c:cable_soil['wfpscoefc']
	,w_d:cable_soil['wfpscoefd']
	,w_e:cable_soil['wfpscoefe']
	,m_sat:cable_soil['soil%ssat']
    ,xk_opt_litter:cable_soil['xkoptlitter']
}

start_values=array([
     100#          leaf
    ,100#     fine_root
    ,100#          wood
    ,100# metabolic_lit
    ,100#structural_lit
    ,100#           cwd
    ,100#     fast_soil
    ,100#     slow_soil
    ,100#  passive_soil
])
times=linspace(0,10,1400)

func_dict={
    bvec_leaf       : bvec_leaf_num 
   ,bvec_fine_root  : bvec_fine_root_num 
   ,bvec_wood       : bvec_wood_num 
   ,btran           : timeLine(Path('Tumbarumba/T_dependent/b_tran.txt'))
   ,T_air           : timeLine(Path('Tumbarumba/T_dependent/T_air.txt'))
   ,T_soil          : timeLine(Path('Tumbarumba/T_dependent/T_soil.txt'))
   ,ms              : timeLine(Path('Tumbarumba/T_dependent/ms.txt'))
   ,xk_n_limit      : timeLine(Path('Tumbarumba/T_dependent/xk_n_limit.txt'))
   ,Npp             : timeLine(Path('Tumbarumba/T_dependent/NPP.txt'))
   ,phase           : timeLine(Path('Tumbarumba/T_dependent/phase.txt'))
   ,r_leaf          : timeLine(Path('Tumbarumba/T_dependent/r_leaf.txt'))
   ,r_wood          : timeLine(Path('Tumbarumba/T_dependent/r_wood.txt'))
   ,r_fine_root     : timeLine(Path('Tumbarumba/T_dependent/r_froot.txt'))
}
smr=SmoothModelRun(
         model=srm
        ,parameter_set=par_dict
        ,start_values=start_values
        ,times=times
        ,func_set=func_dict)
# this dictionary will be analysed
solutions=smr.solve()
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

################################################################
################################################################
import matplotlib.pyplot  as plt
fig=plt.figure(figsize=(7,50))
smr.plot_solutions(fig, fontsize=10)
#ax1=fig.add_subplot(1,1,1)
#ax1.plot(times,solutions[:,0],'*')
fig.savefig("pool_contents.pdf")
