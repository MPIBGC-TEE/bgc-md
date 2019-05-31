from sympy import Symbol,Number,symbols,Matrix,Rational
from sympy.vector import CoordSysND,express,Vector,Dyadic,matrix_to_vector

from bgc_md.resolve.MvarsAndComputers import Mvars as allMvars 
from bgc_md.resolve.MvarsAndComputers import Computers as allComputers
from bgc_md.resolve.helpers import get3, computable_mvars
from bgc_md.resolve.functions import permutationMatrix
class NameSpace:
    def funcMaker(self,name,specialVars):
        def f(self,name):
            mvar=allMvars[name]
            return mvar(allMvars,allComputers,specialVars)
        return f
    
    def __init__(self,specialVars:dict):
        self.specialVars=specialVars

    def produce_getters(self):
        cmvs=computable_mvars(allMvars,allComputers,self.specialVars)
        for mv in cmvs:
            f=self.funcMaker(mv.name,self.specialVars)
            self.__setattr__('get_'+mv.name,f)

C=CoordSysND(name="C",vector_names=["e_vl","e_vw","e_vr","e_ss","e_sf"],transformation='cartesian')
t = Symbol("t")
vl,vw,vr,ss,sf= symbols("vl vw vr ss sf")
I_vl,I_vw,I_ss,I_sf= symbols("I_vl I_vw I_ss I_sf")
R_vl,R_vw,R_ss,R_sf= symbols("R_vl R_vw R_ss R_sf")
k_phot= symbols("k_phot")
gamma_vl,gamma_vw,gamma_vr= symbols("gamma_vl,gamma_vw,gamma_vr")
name_space_1={
        'coord_sys':C
        ,'input_vector':(k_phot*vl-R_vl*vl)*C.e_vl + (k_phot*vl-R_vw*vw)*C.e_vw + I_ss*C.e_ss + I_ss*C.e_ss
        ,'state_vector':vl*C.e_vl + vw*C.e_vw + vr*C.e_vr+ ss*C.e_ss + sf*C.e_sf
        ,'time_symbol':t
        ,'compartmental_dyad': -1*( 
            (C.e_vl|C.e_vl) 
            + (C.e_vw|C.e_vw) 
            + (C.e_vr|C.e_vr) 
            + R_ss*(C.e_ss|C.e_ss)
            + R_sf*(C.e_sf|C.e_sf)
        )
        ,'vegetation_base_vector_list':[C.e_vl ,C.e_vw,C.e_vr] 
        ,'soil_base_vector_list':[C.e_ss ,C.e_sf] 
        # the elements of the list could even be expressions depending on several of the basevectors
        }
ns=NameSpace(name_space_1)
ns.produce_getters()
