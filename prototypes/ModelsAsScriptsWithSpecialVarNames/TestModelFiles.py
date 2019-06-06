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
from bgc_md.resolve.helpers import  get3, computable_mvar_names
from bgc_md.resolve.MVar import MVar
from bgc_md.resolve.Computer import Computer
from bgc_md.resolve.functions import srm_from_B_u_tens
from bgc_md.resolve.IndexedSet import IndexedSet

def remove_leading_whitespace(string,start):
    #remomve the first and last line and the whitespace from the remaining
    return '\n'.join([l[start:] for l in string.splitlines()[1:-1]])
        
class TestModelFiles(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the information that is neccessary to build the 
    # compartmental Matrix 
    # Here we execute a python script in a special sandbox environment
    
    def test_CS_creation(self):
        from bgc_md.resolve.MvarsAndComputers import Mvars as myMvars
        from bgc_md.resolve.MvarsAndComputers import Computers as myComputers
        # There are many different ways to provide the ingredients for 
        # explicit function in models/testFivePool/source.py
        #md=get3(var_name="smooth_reservoir_model",model_id='testFivePool')
        md=get3(var_name="smooth_reservoir_model",allMvars=myMvars,allComputers=myComputers,model_id='testFivePool')
        pe('md.compartmental_matrix',locals())
        #pe('md.compartmental_matrix',locals())
        # NO explicit function in models/testTwoPool/source.py
        #md=get3(var_name="smooth_reservoir_model",allMvars=myMvars,allComputers=myComputers,model_id='testTwoPool')
        #pe('md',locals())

    def test_miniCable(self):
        from bgc_md.resolve.MvarsAndComputers import Mvars as myMvars
        from bgc_md.resolve.MvarsAndComputers import Computers as myComputers
        # NO explicit variable smooth_reservoir_model
        srm=get3(var_name="smooth_reservoir_model",allMvars=myMvars,allComputers=myComputers,model_id='miniCable')
        #smrs=get3(var_name="smooth_model_run_dictionary",allMvars=myMvars,allComputers=myComputers,model_id='miniCable')
        ##smr=get(var_name="smooth_model_run",model_id='miniCable')
        #self.assertTrue('default' in smrs.keys())


    @unittest.skip
    def test_Symbols_and_Quanteties(self):
        md=get(var_name="smooth_reservoir_model",model_id='pseudoCable')


