# The purpose of this Schema is to work backwards from the minimal requirement that the 
# an Instance of CompartmentalModel can be created.
# So a model consists at minimum constructor call.
# and possibly some variable definitions to populate the namespace in which the constructor is called. 


import unittest
from testinfrastructure.helpers import pe
#from sympy import Basic,Symbol,Matrix,symbols

#from sympy.vector import CoordSysND, Vector,express
from bgc_md.prototype_helpers_script import get


class TestSchema(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the information that is neccessary to build the 
    # compartmental Matrix 
    # Here we execute a python script in a special sandbox environment
    
    def test_CS_creation(self):
        md=get(var_name="smooth_reservoir_model",model_id='pseudoCable')



