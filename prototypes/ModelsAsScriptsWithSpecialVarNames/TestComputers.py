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
from sympy import Symbol,Number
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
        from bgc_md.resolve.MvarsAndComputers import Mvars as myMvars
        from bgc_md.resolve.MvarsAndComputers import Computers as myComputers
        
        
        # compute the set of computable Mvars from the names of defined variables 
        # this is the set of mvars supposedly given in the model file 
        C=myComputers['smooth_reservoir_model(coord_sys,state_vector,time_symbol,compartmental_dyad,input_vector)']
        ref=[ 'coord_sys' ,'state_vector' ,'time_symbol' ,'compartmental_dyad' ,'input_vector' ]
        self.assertEqual( C.arg_names , ref)
        
    def test_input_tuple(self):
        from sympy import Symbol,symbols,Matrix
        from sympy.vector import CoordSysND,express,Vector,Dyadic
        from bgc_md.resolve.MvarsAndComputers import Mvars as allMvars 
        from bgc_md.resolve.MvarsAndComputers import Computers as allComputers
        vector_names=["e_vl","e_vw"]
        C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')
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
        from sympy import Symbol,symbols,Matrix
        from sympy.vector import CoordSysND,express,Vector,Dyadic,matrix_to_vector
        from bgc_md.resolve.MvarsAndComputers import Mvars as allMvars 
        from bgc_md.resolve.MvarsAndComputers import Computers as allComputers
        vector_names=["e_vl","e_vw"]
        C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')
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
    def test_compartmental_matrix(self):
        from sympy import Symbol,symbols,Matrix
        from sympy.vector import CoordSysND,express,Vector,Dyadic
        from bgc_md.resolve.MvarsAndComputers import Mvars as allMvars 
        from bgc_md.resolve.MvarsAndComputers import Computers as allComputers
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
        from sympy import Symbol,symbols,Matrix
        from sympy.vector import CoordSysND,express,Vector,Dyadic,matrix_to_vector
        from bgc_md.resolve.MvarsAndComputers import Mvars as allMvars 
        from bgc_md.resolve.MvarsAndComputers import Computers as allComputers
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
