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
from sympy.physics.units import mass,time
from sympy.physics.units import Quantity 
from sympy.physics.units import year,day,second,minute
from sympy.physics.units import meter, kilogram
from sympy.physics.units.dimensions import dimsys_SI
from sympy.physics.units import convert_to
from bgc_md.resolve.MvarsAndComputers import Mvars as allMvars 
from bgc_md.resolve.MvarsAndComputers import Computers as allComputers
from typing import List
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun
#from CompartmentalSystems import smooth_reservoir_model 
from bgc_md.DescribedSymbol import DescribedSymbol
from bgc_md.DescribedQuantity import DescribedQuantity
from bgc_md.resolve.helpers import  get3, computable_mvar_names
from bgc_md.resolve.MVar import MVar
from bgc_md.resolve.Computer import Computer
from bgc_md.resolve.functions import permutationMatrix
from bgc_md.resolve.IndexedSet import IndexedSet

def remove_leading_whitespace(string,start):
    #remomve the first and last line and the whitespace from the remaining
    return '\n'.join([l[start:] for l in string.splitlines()[1:-1]])
        
class TestComputersBgc(unittest.TestCase):

    def test_arg_names(self):
        # here we test the (growing) sets of Mvars and Computers included in the package
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
        # fixme: mm 9 5 
        vl,vw= symbols("vl vw")
        st=Matrix([vl,vw])
        name_space={
                'state_tuple':st
        }
        self.assertEqual(
                 allMvars['coord_sys'](allMvars,allComputers,name_space)
                ,CoordSysND(name="C",vector_names=["e_vl","e_vw"],transformation='cartesian')
        )
    
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
    
class TestResolveBgc(unittest.TestCase):
    def test_computability_bgc(self):
        # here we test the (growing) sets of Mvars and Computers included in the packe
        from bgc_md.resolve.MvarsAndComputers import Mvars as myMvars
        from bgc_md.resolve.MvarsAndComputers import Computers as myComputers
        
        
        # compute the set of computable Mvars from the names of defined variables 
        # this is the set of mvars supposedly given in the model file 
        names_of_available_mvars=frozenset([
             'coord_sys'
            ,'state_vector' 
            ,'time_symbol' 
            ,'compartmental_dyad' 
            ,'input_vector'
        ]) 
        C=myComputers['smooth_reservoir_model(coord_sys,state_vector,time_symbol,compartmental_dyad,input_vector)']
        ref=[ 'coord_sys' ,'state_vector' ,'time_symbol' ,'compartmental_dyad' ,'input_vector' ]
        self.assertEqual( C.arg_names , ref)
        
        mvars=computable_mvar_names(
                allMvars=myMvars
                ,allComputers=myComputers
                ,names_of_available_mvars=names_of_available_mvars
        )
        res=set([v.name for v in mvars])
        ref=set([
            'coord_sys'
            ,'state_vector'
            ,'state_tuple'
            ,'time_symbol'
            ,'compartmental_dyad'
            ,'input_vector'
            ,'input_tuple'
            ,'smooth_reservoir_model' # new (provided by computers)
            ,'compartmental_matrix'   # new (provided by computers)
        ])
        self.assertEqual(res,ref)
    
    def test_documented_Quanteties(self):
        s=DescribedQuantity("s")
        s.set_dimension(mass,"SI")
        s=DescribedQuantity("s")
        s.set_dimension(mass,"SI")
        s.set_description("Soil carbon ")
        
        l=DescribedQuantity("l")
        l.set_dimension(mass,"SI")
        l.set_description("Leaf carbon ")
        
        k_s=DescribedQuantity("k_s")
        k_s.set_dimension(mass/time,"SI")
        k_s.set_description("Soil respiration rate")
        
        k_l=DescribedQuantity("k_l")
        k_l.set_dimension(mass/time,"SI")
        k_l.set_description("Leaf respiration rate")

        B=Matrix([[k_l,0],[0,k_s]])
        

        #s.set_description("Soil carbon ")
        # the model defining script or the UI can add symbols and quanteties to the model
        # It should an ordered dict to give control to the user
        model_name_space_a={
                'documented_identifiers':[k_s,k_l,l,s]
                ,'compartmental_matrix':B
                ,'state_tuple':Matrix([l,s])
        }

    def test_alternative_coordinate_systems_for_model_comparison(self):
        # Assume that we have a bunch of  different pool systems that are actually quite
        # similar but have a very different ordering of state variables.
        # To make the similarity obvious a user could add alternative coordinate systems to 
        # the respective models that lead to comparable matrices
        # Assume that all systems to be compared consist of 2 soil layers with a fast and slow
        # soil pool  pool in each layer and that we want to compare them by a layer-wise view
        # with first the fast and then the slow pools:
        # comp_ord=["e_soilfast1","e_soilslow1",  "e_soilfast2","e_soilslow2"]

        # Assume that The base vectors of the first system are called

        vector_names_a=["e_1", "e_2", "e_3" ,"e_4"]  
        Ca=CoordSysND(name="Ca",vector_names=vector_names_a,transformation='cartesian')
        a,b,c,d,e,f,g,h=symbols("a,b,c,d,e,f,g,h")
        #and the vector to be compared is 
        v_a=a*Ca.e_1+b*Ca.e_2+d*Ca.e_3
        # and that reordered by the user with knowledge of which pools are fast 
        # to the comparison order would be 
        ord_a=["e_3", "e_2", "e_1", "e_4"]  
        pm_a=permutationMatrix(vector_names_a,ord_a)
        Ca_comp=CoordSysND(name="Ca_comp",parent=Ca,rotation_matrix=pm_a)
        v_a_ord=express(v_a,Ca_comp)

        # Now suppose the vectors in a second model are called 
        vector_names_b=["E_1", "E_2", "E_3" ,"E_4"]  
        Cb=CoordSysND(name="Cb",vector_names=vector_names_b,transformation='cartesian')
        A,B,C,D,E,F,G,H=symbols("A,B,C,D,E,F,G,H")
        v_b=A*Cb.E_1+B*Cb.E_2+D*Cb.E_4
        # and that reordered by the user with knowledge of which pools are fast 
        # to the comparison order would be 
        ord_b=["E_3", "E_2", "E_4", "E_1"]  
        pm_b=permutationMatrix(vector_names_b,ord_b)
        Cb_comp=CoordSysND(name="Cb_comp",parent=Cb,rotation_matrix=pm_b)
        v_b_ord=express(v_b,Cb_comp)
        
        # with respect to the new coordinate systems the tupels look similar
        ta=v_a_ord.to_matrix(Ca_comp)
        tb=v_b_ord.to_matrix(Cb_comp)
        self.assertEqual(ta,Matrix([[d], [b], [a], [0]]))
        self.assertEqual(tb,Matrix([[D], [B], [A], [0]]))
        # now suppose that the computed tuple are to be compared
        # in a table containing all models that define it.
        # In this case it aquires a meaning that transcends 
        # a single model. (e.g. like the state vector which 
        #is present in all, or the "vegetation_cycling_matrix" 
        # which is present in some models)
        # a user would have to define a new MVar instance in the 
        # source code of the package with a name that does 
        # not exist and refer 
        # For this test we added 'exampleMvar' to the 
        # appropriate file so that we can use it in the namespaces
        # describing the two models :
        model_name_space_a={'example_MVar':ta}
        model_name_space_b={'example_MVar':tb}
        # a report could now access this variable in all models 
        # that define 'example_MVar'
        ta_found=allMvars['example_MVar'](allMvars,allComputers,model_name_space_a)
        tb_found=allMvars['example_MVar'](allMvars,allComputers,model_name_space_b)
        # if the variable to be compared can be computed from 
        # other MVars Computer instances can be added  


        
    
    def test_vegetation_and_soil_parts(self):
        # The vegetation part of a model is defined by the set of state variables that represent vegetation pools
        # This information automatically determines all the components of the normal form of a vegetation part of a model 
        # d/dt C = A *C + b* u
        # The same is true for the soil part
        # d/dt C = B*C+ I = T* N *C + I 

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
        
        # we can now look at the projections onto the vegetation pools 
        at    =allMvars['carbon_allocation_tuple'](allMvars,allComputers,name_space_1)
        ta     =allMvars['total_carbon_allocation'](allMvars,allComputers,name_space_1)
        rt    =allMvars['relative_carbon_allocation_tuple'](allMvars,allComputers,name_space_1)
        cyc=allMvars['vegetation_cycling_matrix'](allMvars,allComputers,name_space_1)
        A=allMvars['soil_matrix'](allMvars,allComputers,name_space_1)

        xi=allMvars['soil_scaling_matrix_xi'](allMvars,allComputers,name_space_1)
        T=allMvars['soil_transport_matrix_T'](allMvars,allComputers,name_space_1)
        N=allMvars['soil_decomposition_matrix_N'](allMvars,allComputers,name_space_1)
        
        SV=allMvars['soil_to_vegetation_matrix'](allMvars,allComputers,name_space_1)
        VS=allMvars['vegetation_to_soil_matrix'](allMvars,allComputers,name_space_1)
        
        #pe('at',locals())
        #pe('ta',locals())
        #pe('rt',locals())
        #pe('cyc',locals())
        #pe('A',locals())
        #pe('xi',locals())
        #pe('T',locals())
        #pe('N',locals())
        #pe('SV',locals())
        #pe('VS',locals())
        computable_mvar_names(allMvars,allComputers,frozenset(name_space_1.keys()))

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
