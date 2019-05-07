# The purpose of this Schema is to work backwards from the minimal requirement that the 
# an Instance of CompartmentalModel can be created.
# So a model consists at minimum constructor call.
# and possibly some variable definitions to populate the namespace in which the constructor is called. 


import unittest
from pathlib import Path
from testinfrastructure.helpers import pe
from testinfrastructure.InDirTest import InDirTest
#from sympy import Basic,Symbol,Matrix,symbols

#from sympy.vector import CoordSysND, Vector,express
#from bgc_md.prototype_helpers_script import get
from sympy import Symbol,Number,symbols,Matrix,Rational
from sympy.vector import CoordSysND,express,Vector,Dyadic,matrix_to_vector
from bgc_md.resolve.MvarsAndComputers import Mvars as allMvars 
from bgc_md.resolve.MvarsAndComputers import Computers as allComputers
from typing import List
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun
#from CompartmentalSystems import smooth_reservoir_model 
from bgc_md.resolve.helpers import  get3, computable_mvars
from bgc_md.resolve.MVar import MVar
from bgc_md.resolve.Computer import Computer
from bgc_md.resolve.functions import srm_from_B_u_tens
from bgc_md.resolve.IndexedSet import IndexedSet

def remove_leading_whitespace(string,start):
    #remomve the first and last line and the whitespace from the remaining
    return '\n'.join([l[start:] for l in string.splitlines()[1:-1]])
        
class TestComputers(unittest.TestCase):

    def test_arg_names(self):
        # here we test the (growing) sets of Mvars and Computers included in the packe
        # compute the set of computable Mvars from the names of defined variables 
        # this is the set of mvars supposedly given in the model file 
        C=allComputers['smooth_reservoir_model(coord_sys,state_vector,time_symbol,compartmental_dyad,input_vector)']
        ref=[ 'coord_sys' ,'state_vector' ,'time_symbol' ,'compartmental_dyad' ,'input_vector' ]
        self.assertEqual( C.arg_names , ref)
        
    def test_input_tuple(self):
        C=CoordSysND(name="C",vector_names=["e_vl","e_vw"],transformation='cartesian')
        I_vl,I_vw= symbols("I_vl I_vw")
        I= I_vl*C.e_vl +I_vw*C.e_vw
        name_space={
                'coord_sys':C
                ,'input_vector':I
        }
        self.assertEqual(
                 allMvars['input_tuple'](allMvars,allComputers,name_space)
                ,Matrix([I_vl,I_vw])
        )

    def test_input_vector(self):
        C=CoordSysND(name="C",vector_names=["e_vl","e_vw"],transformation='cartesian')
        I_vl,I_vw= symbols("I_vl I_vw")
        I=Matrix([I_vl,I_vw])
        name_space={
                'coord_sys':C
                ,'input_tuple':I
        }
        self.assertEqual(
                 allMvars['input_vector'](allMvars,allComputers,name_space)
                ,I_vl*C.e_vl +I_vw*C.e_vw
        )
    def test_state_tuple(self):
        C=CoordSysND(name="C",vector_names=["e_vl","e_vw"],transformation='cartesian')
        vl,vw= symbols("vl vw")
        sv= vl*C.e_vl +vw*C.e_vw
        name_space={
                'coord_sys':C
                ,'state_vector':sv
        }
        self.assertEqual(
                 allMvars['state_tuple'](allMvars,allComputers,name_space)
                ,Matrix([vl,vw])
        )

    def test_state_vector(self):
        C=CoordSysND(name="C",vector_names=["e_vl","e_vw"],transformation='cartesian')
        vl,vw= symbols("vl vw")
        st=Matrix([vl,vw])
        name_space={
                'coord_sys':C
                ,'state_tuple':st
        }
        self.assertEqual(
                 allMvars['state_vector'](allMvars,allComputers,name_space)
                ,vl*C.e_vl +vw*C.e_vw
        )

    def test_coord_sys(self):
        # construct the coordinate system from the ordered tuple of statevariables
        vl,vw= symbols("vl vw")
        st=Matrix([vl,vw])
        name_space={
                'state_tuple':st
        }
        raise(Exception("not implemented yet"))
        self.assertEqual(
                 allMvars['state_vector'](allMvars,allComputers,name_space)
                ,CoordSysND(name="C",vector_names=["e_vl","e_vw"],transformation='cartesian')
        )
    def test_vegetation_and_soil_parts(self):
        # The vegetation part of a model is defined by the set of state variables that represent vegetation pools
        # This information automatically determines all the components of the normal form of a vegetation part of a model 
        # d/dt C = A *C + b* u
        # The same is true for the soil part
        # d/dt C = B*C+ I = T* N *C + I 

        C=CoordSysND(name="C",vector_names=["e_vl","e_vw","e_vr","e_ss","e_sf"],transformation='cartesian')
        vl,vw,ss,fs= symbols("vl vw ss _sf")
        I_vl,I_vw,I_ss,I_sf= symbols("I_vl I_vw I_ss I_sf")
        R_vl,R_vw,R_ss,R_sf= symbols("R_vl R_vw R_ss R_sf")
        k_phot= symbols("k_phot")
        gamma_vl,gamma_vw,gamma_vr= symbols("gamma_vl,gamma_vw,gamma_vr")
        name_space_1={
                'coord_sys':C
                ,'input_vector':(k_phot*vl-R_vl*vl)*C.e_vl + (k_phot*vl-R_vw*vw)*C.e_vw + I_ss*C.e_ss + I_ss*C.e_ss
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
        
        # we can now look at the projections onto the vegetation pools 
        at    =allMvars['carbon_allocation_tuple'](allMvars,allComputers,name_space_1)
        pe('at',locals())
        ta     =allMvars['total_carbon_allocation'](allMvars,allComputers,name_space_1)
        pe('ta',locals())
        rt    =allMvars['relative_carbon_allocation_tuple'](allMvars,allComputers,name_space_1)
        pe('rt',locals())
        cyc=allMvars['vegetation_cycling_matrix'](allMvars,allComputers,name_space_1)
        pe('cyc',locals())
        A=allMvars['soil_matrix'](allMvars,allComputers,name_space_1)
        pe('A',locals())
        SV=allMvars['soil_to_vegetation_matrix'](allMvars,allComputers,name_space_1)
        pe('SV',locals())
        VS=allMvars['vegetation_to_soil_matrix'](allMvars,allComputers,name_space_1)
        pe('VS',locals())
        
    def test_b_comparison(self):
        # Assume we have two different models (here represented by two namespaces)
        # that both define carbon allocation with respect to their own pool names
        # We want to be able to compare the structure of the vector b describing the distribution
        # to different pools
        # Different levels of similarity are possible:
        # a)  Both models have the same meta-structure with respect to the 
        #     vegetation pools e.g.(a wood and a leaf pool). In this case the b vectors
        #     have not only the same size but their components also have the same meaning.
        #     A description in terms of the meta variables wood and leafs that is identical
        #     would point to an identical carbon allocation scheme
        # b)  The metastructure is different but with a possible intersection of the sets of vegetation pools. 
        #     Model 1 may have two vegetation pools (wood,leafs)
        #     while model 2 has three (wood,roots,leafs)
        #     It would still be interesting to compare the overlapping part.  
        C=CoordSysND(name="C",vector_names=["e_vl","e_vw","e_s"],transformation='cartesian')
        I_vl,I_vw,I_s= symbols("I_vl I_vw I_s")
        name_space_1={
                'coord_sys':C
                ,'input_vector':I_vl*C.e_vl + I_vw*C.e_vw + I_s*C.e_s 
                ,'vegetation_base_vector_list':[C.e_vl ,C.e_vw] 
                # the elements of the list could even be expressions depending on several of the basevectors
                # The order is important for the comparison and represents the knowledghe of the model author
                # about the allocation. 
                # To simplify the interpretation of the resulting allocation tuples 
                # and make them comparable it would be SENSIBLE to always use the same order 
                # of (leaf, wood, root, ..., other vegetation pools) 
                # On the other hand it is not REQUIRED to be able to compute the distribution of the 
                # carbon influx to different pools.
                # E.g. we do not insist on pointing out which pool is a 'wood' pool 
                # or even that a "wood' pool exists. 
                # If this information is contained in the model description we can point out the connction.
        }
        
        C_2a=CoordSysND(name="C_2a",vector_names=["e_leaf","e_wood","e_soil"],transformation='cartesian')
        u_leaf,u_wood,u_soil = symbols("u_leaf u_wood u_soil")
        name_space_2a={
                'coord_sys':C_2a
                ,'input_vector':u_leaf*C_2a.e_leaf + u_wood*C_2a.e_wood + u_soil*C_2a.e_soil
                ,'vegetation_base_vector_list':[C_2a.e_leaf ,C_2a.e_wood] 
        }

        C_2b=CoordSysND(name="C_2b",vector_names=["e_leaf","e_wood","e_root","e_soil"],transformation='cartesian')
        u_leaf,u_wood,u_root,u_soil = symbols("u_leaf u_wood u_root u_soil")
        name_space_2b={
                'coord_sys':C_2b
                ,'input_vector':u_leaf*C_2b.e_leaf + u_wood*C_2b.e_wood + u_root*C_2b.e_root + u_soil*C_2b.e_soil 
                ,'vegetation_base_vector_list':[C_2b.e_leaf, C_2b.e_wood ,C_2b.e_root ]
        }
        C_2c=CoordSysND(name="C_2c",vector_names=["e_leaf","e_wood","e_root","e_soil"],transformation='cartesian')
        u, u_leaf,u_wood,u_root,u_soil = symbols("u u_leaf u_wood u_root u_soil")

        name_space_2c={
                'coord_sys':C_2c
                ,'input_vector':Rational(1,2)*u*C_2c.e_leaf + Rational(1,4)*u*C_2c.e_wood + Rational(1,4)*u*C_2c.e_root + u_soil*C_2c.e_soil 
                ,'vegetation_base_vector_list':[C_2c.e_leaf, C_2c.e_wood ,C_2c.e_root ]
                ,'total_carbon_allocation': u #this overrides the actual computation of u . The 
        }
        # we can now look at the projections onto the vegetation pools 
        at_1    =allMvars['carbon_allocation_tuple'](allMvars,allComputers,name_space_1)
        t_1     =allMvars['total_carbon_allocation'](allMvars,allComputers,name_space_1)
        rt_1    =allMvars['relative_carbon_allocation_tuple'](allMvars,allComputers,name_space_1)
        
        at_2a   =allMvars['carbon_allocation_tuple'](allMvars,allComputers,name_space_2a)
        t_2a     =allMvars['total_carbon_allocation'](allMvars,allComputers,name_space_2a)
        rt_2a    =allMvars['relative_carbon_allocation_tuple'](allMvars,allComputers,name_space_2a)

        at_2b   =allMvars['carbon_allocation_tuple'](allMvars,allComputers,name_space_2b)
        t_2b     =allMvars['total_carbon_allocation'](allMvars,allComputers,name_space_2b)
        rt_2b    =allMvars['relative_carbon_allocation_tuple'](allMvars,allComputers,name_space_2b)

        at_2c   =allMvars['carbon_allocation_tuple'](allMvars,allComputers,name_space_2c)
        t_2c     =allMvars['total_carbon_allocation'](allMvars,allComputers,name_space_2c)
        rt_2c    =allMvars['relative_carbon_allocation_tuple'](allMvars,allComputers,name_space_2c)
        #pe('at_1',locals())
        #pe('t_1',locals())
        #pe('rt_1',locals())
        #
        #pe('at_2a',locals())
        #pe('t_2a',locals())
        #pe('rt_2a',locals())
        #
        #pe('at_2b',locals())
        #pe('t_2b',locals())
        #pe('rt_2b',locals())
        #
        pe('at_2c',locals())
        pe('t_2c',locals())
        pe('rt_2c',locals())

    def test_compartmental_matrix(self):
        vector_names=["e_vl","e_vw"]
        C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')
        B=-1*( #(diagonal) Tensor  
            (C.e_vl|C.e_vl)
           +(C.e_vw|C.e_vw)
        )
        name_space={
                'coord_sys':C
                ,'compartmental_dyad':B
        }
        self.assertEqual(
                 allMvars['compartmental_matrix'](allMvars,allComputers,name_space)
                ,-1*Matrix([[1,0],[0,1]])
        )

    def test_compartmental_dyad(self):
        vector_names=["e_vl","e_vw"]
        C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')
        B=-1*Matrix([[1,0],[0,1]])
        name_space={
                'coord_sys':C
                ,'compartmental_matrix':B
        }
        self.assertEqual(
                 allMvars['compartmental_dyad'](allMvars,allComputers,name_space)
                , -1*( (C.e_vl|C.e_vl) +(C.e_vw|C.e_vw))
        )
