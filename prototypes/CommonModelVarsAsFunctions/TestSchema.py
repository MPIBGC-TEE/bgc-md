# The purpose of this Schema is to work backwards from the minimal requirement that the 
# an Instance of CompartmentalModel can be created.
# So a model consists at minimum constructor call.
# and possibly some variable definitions to populate the namespace in which the constructor is called. 


import unittest
from testinfrastructure.helpers import pe
#from sympy import Basic,Symbol,Matrix,symbols

#from sympy.vector import CoordSysND, Vector,express
from bgc_md.prototype_helpers import get_SmoothReservoirModel
from bgc_md.prototype_helpers import get


class TestSchema(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the information that is neccessary to build the 
    # compartmental Matrix
    
    def test_CS_creation(self):
        # explicit function in models/testFivePool/source.py
        md=get(model_id='testFivePool',callString='get_SmoothReservoirModel()')
        pe('md.compartmental_matrix',locals())
         NO explicit function in models/testTwoPool/source.py
        md=get_SmoothReservoirModel(model_id='testTwoPool')




    #@unittest.skip
    def test_compare_GPP_distribution_for_different_models(self):
        # many (if not all) vegetation models have similar structure       
        # and are build from the same components.
        # E.g. many have a state variable describing the amount of         
        # carbon in the leafs. 
        # However the Variable Name (Symbol) will be different in different publications
        # Let us assume that we have 2 different models that both have 
        # spread the NetInFlux evenly between leaf and wood pools.
        # we want to be able to prove that
        # now we define a category distribution vector
        #b_five=VegDistVector(leaf=Ivl/u_org,
        print(
            get(model_id='testFivePool',callString='get_cumulative_Vegetation_Input()')
            ,get(model_id='testFivePool',callString='get_cumulative_Vegetation_Input()')
        )
        
    def test_polymorph(self):
        # many model properties can be computed from different sources
        # We will implement the following strategy
        # 1.) Check if the user provided a function to compute the desired property
        # 2.) Check if the property  can be computed from other properties provided by the user.
        # 3.) If there are more then one ways to get the result check for consistency
         
        # we demonstrate this by a model that does not any function for get_InputVector but 
        # only for the separate fluxes
        get(model_id='testVectorFree',callString='get_InputVector()')
        

