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
from bgc_md.resolve.ClassesStateLess import MVar3,Computer3
from bgc_md.resolve.functions import srm_from_B_u_tens
from bgc_md.resolve.MvarsAndComputers import myMvars,myComputers
def remove_leading_whitespace(string,start):
    #remomve the first and last line and the whitespace from the remaining
    return '\n'.join([l[start:] for l in string.splitlines()[1:-1]])

class TestModels(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the information that is neccessary to build the 
    # compartmental Matrix 
    # Here we execute a python script in a special sandbox environment
    
    def test_CS_creation(self):
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
        # NO explicit variable smooth_reservoir_model
        srm=get3(var_name="smooth_reservoir_model",allMvars=myMvars,allComputers=myComputers,model_id='miniCable')
        #smrs=get3(var_name="smooth_model_run_dictionary",allMvars=myMvars,allComputers=myComputers,model_id='miniCable')
        ##smr=get(var_name="smooth_model_run",model_id='miniCable')
        #self.assertTrue('default' in smrs.keys())


    @unittest.skip
    def test_Symbols_and_Quanteties(self):
        md=get(var_name="smooth_reservoir_model",model_id='pseudoCable')


class TestKnowledge(unittest.TestCase):

    def test_computability(self):
        
        # Here we explore the possibility to define both the 'args; of the 
        # Computer instance and the 'computers' in a MVar instance
        # not as objects but as strings interpreted with respect to a
        # set of Mvars or Computers respectively and resolve
        # the relationship at runtime by the name attribute of both. 
        # This finally removes the duplication and allows any kind of cross 
        # referencing even if the variables or computers do not 
        # exist yet or not at all. The latter possibility must be excluded
        # by a consistence check
        
        myMvars=frozenset({
              MVar3('coord_sys') 
            , MVar3('state_vector')
            , MVar3('time_symbol') 
            , MVar3('compartmental_dyad') 
            , MVar3('input_vector') 
            , MVar3('parameter_dictionary') 
            , MVar3('start_vector') 
            , MVar3('time_vector') 
            , MVar3('function_dictionary')
            , MVar3(
                    'smooth_reservoir_model'
                    ,computerNames=['srm_bu_tens']
                    ,description='A smooth reservroir Model'
                )
            , MVar3(
                    'smooth_model_run_dictionary'
                    ,computerNames=[] # at the moment empty list, consequently 
                    # only available when explicitly defined. 
                    # Although automatic computation would be simple 
                    # the keys make most sense if defined by the user
                    ,description= """
                    The dictionary values are SmoothModelRun objects. 
                    The keys can be used in user code to refer to special 
                    simulations. """
            )
            , MVar3(
                    'smooth_model_run'
                    ,computerNames=['smr']
                    ,description= """A single simulation"""
            )
        })
        
        myComputers=frozenset({
                Computer3(
                    'srm_bu_tens'
                    ,func=srm_from_B_u_tens
                    ,arg_names=[
                         'coord_sys'
                        ,'state_vector' 
                        ,'time_symbol' 
                        ,'compartmental_dyad' 
                        ,'input_vector' 
                     ]
                    ,description="""Produces a smoth reservoir model"""
                )
                ,Computer3(
                     'smr'
                    ,SmoothModelRun
                    ,arg_names=[
                         'smooth_reservoir_model'
                        ,'parameter_dictionary'
                        ,'start_vector'
                        ,'time_vector'
                        ,'function_dictionary'
                    ]
                    ,description="""Creates a single instance of a SmoothModelRun"""
                )
        })
        # assert that we can build the reservoir model
        
        #compute the set of computable Mvars 
        names_of_available_mvars=frozenset([
                         'coord_sys'
                        ,'state_vector' 
                        ,'time_symbol' 
                        ,'compartmental_dyad' 
                        ,'input_vector']) 
        mvars=computable_mvars(
                allMvars=myMvars
                ,allComputers=myComputers
                ,names_of_available_mvars=frozenset([
                                 'coord_sys'
                                ,'state_vector' 
                                ,'time_symbol' 
                                ,'compartmental_dyad' 
                                ,'input_vector']) 
                        #,model_id='testFivePool'i
                )
        pe('mvars',locals())



        


    #def test_computable_mvars(self):
    #    # this is the forward simulation
    #    # 
    #    availableVars=frozenset('SmoothModelRun
        


        


#    #@unittest.skip
#    def test_compare_GPP_distribution_for_different_models(self):
#        # many (if not all) vegetation models have similar structure       
#        # and are build from the same components.
#        # E.g. many have a state variable describing the amount of         
#        # carbon in the leafs. 
#        # However the Variable Name (Symbol) will be different in different publications
#        # Let us assume that we have 2 different models that both have 
#        # spread the NetInFlux evenly between leaf and wood pools.
#        # we want to be able to prove that
#        # now we define a category distribution vector
#        #b_five=VegDistVector(leaf=Ivl/u_org,
#        print(
#            get(model_id='testFivePool',callString='get_cumulative_Vegetation_Input()')
#            ,get(model_id='testFivePool',callString='get_cumulative_Vegetation_Input()')
#        )
#        
#    def test_polymorph(self):
#        # many model properties can be computed from different sources
#        # We will implement the following strategy
#        # 1.) Check if the user provided a function to compute the desired property
#        # 2.) Check if the property  can be computed from other properties provided by the user.
#        # 3.) If there are more then one ways to get the result check for consistency
#         
#        # we demonstrate this by a model that does not any function for get_InputVector but 
#        # only for the separate fluxes
#        get(model_id='testVectorFree',callString='get_InputVector()')
#        

