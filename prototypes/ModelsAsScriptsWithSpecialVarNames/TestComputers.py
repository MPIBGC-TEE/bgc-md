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
from sympy import Symbol,Number,symbols,Matrix
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
    def test_b_comparison(self):
        # Assume we have two different models (here represented by two namespaces)
        # that both define carbon allocation with respect to their own pool names
        # We want to be able to compare the structure of the vector b describing the distribution
        # to different pools
        # There are different levels of similarity possible.
        # a)  Both models have the same metastructure with respect to the 
        #     vegetation pools e.g.(a wood and a leaf pool). In this case the b vectors
        #     have not only the same size but their components also have the same meaning.
        #     A discription in terms of the meta variables wood and leafs that is identical
        #     would point to an identical carbon allocation scheme
        # b)  The metastructure is different but with possible overlap. 
        #     Model 1 may have two vegetation pools (wood,leafs)
        #     while model 2 has three (wood,roots,leafs)
        #     It would still be interesting to compare the overlapping part.  
        C_1=CoordSysND(name="C_1",vector_names=["e_vl","e_vw","e_s"],transformation='cartesian')
        I_vl,I_vw,I_s= symbols("I_vl I_vw I_s")
        I_veg=Matrix([I_vl,I_vw]) #only pick out the vegetatio part
        name_space_1={
                'coord_sys':C_1
                ,'input_tuple':I_veg
        }
        
        C_2a=CoordSysND(name="C_2a",vector_names=["e_leaf,","e_wood","e_soil"],transformation='cartesian')
        u_leaf,u_wood,u_soil = symbols("u_leaf u_wood u_soil")
        I_veg=Matrix([u_leaf,u_wood])#only pick out the vegetatio part
        name_space_2a={
                'coord_sys':C_2a
                ,'input_tuple':I_veg
        }

        
        C_2b=CoordSysND(name="C_2b",vector_names=["e_leaf,","e_wood","e_root","e_soil"],transformation='cartesian')
        u_leaf,u_wood,u_root,u_soil = symbols("u_leaf u_wood u_root u_soil")
        I_veg=Matrix([u_leaf,u_wood,u_root])#only pick out the vegetatio part
        name_space_2={
                'coord_sys':C_2
                ,'input_tuple':I_veg
        }
        raise(Exception("not implemented yet"))
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
