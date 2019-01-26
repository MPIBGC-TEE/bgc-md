# The purpose of this Schema is to work backwards from the minimal requirement that the 
# an Instance of CompartmentalModel can be created.
# and possibly some variable definitions to populate the namespace in which the constructor is called. 
# To be able to reproduce expressions we represent them as expression strings to be executed 
# (This can also be done with input received from the UI)
# The expressions are evaluated in the Namespace created by the python script part of the model, which 
# can contain arbitrary inputs and function definitions.
# A model can be thought of as composed from two parts.
#   1.) Some file source.py to be executed firs.
#   2.) A list of expressions (The user is responisble to arrange them in the right order)
#       A minimal model desription could contain a single expression of the form special[srm]=smooth_reservoir_model
#       special variables

import unittest
from testinfrastructure.helpers import pe
#from sympy import Basic,Symbol,Matrix,symbols

#from sympy.vector import CoordSysND, Vector,express
#from bgc_md.prototype_helpers import get_SmoothReservoirModel
from bgc_md.prototype_helpers_expression import get,getBaseQuantities,getDerivedValues,getSemanticValues


class TestSchema(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the information that is neccessary to build the a smooth reservoir model
    



    #@unittest.skip
    def test_Base_and_Derived_Vars(self):
        #md=get(var_name="smooth_reservoir_model",model_id='pseudoCable')
        bq=getBaseQuantities(model_id='pseudoCable')
        pe('bq',locals())
        
        dv=getDerivedValues(model_id='pseudoCable')
        pe('dv',locals())
        
        sv=getSemanticValues(model_id='pseudoCable')
        pe('sv',locals())
    
    
    @unittest.skip
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
        pass
        
    @unittest.skip
    # compartmental Matrix
    def test_polymorph(self):
        # many model properties can be computed from different sources
        # We will implement the following strategy
        # 1.) Check if the user provided a function to compute the desired property
        # 2.) Check if the property  can be computed from other properties provided by the user.
        # 3.) If there are more then one ways to get the result check for consistency
         
        # we demonstrate this by a model that does not any function for get_InputVector but 
        # only for the separate fluxes
        pass
        

