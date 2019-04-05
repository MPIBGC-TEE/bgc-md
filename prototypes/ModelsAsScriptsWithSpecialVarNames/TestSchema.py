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
#from bgc_md.resolve.ClassesStateLess import MVar3,Computer3
from bgc_md.resolve.MVar import MVar
from bgc_md.resolve.Computer import Computer
from bgc_md.resolve.functions import srm_from_B_u_tens
from bgc_md.resolve.IndexedSet import IndexedSet

def remove_leading_whitespace(string,start):
    #remomve the first and last line and the whitespace from the remaining
    return '\n'.join([l[start:] for l in string.splitlines()[1:-1]])
        
class TestModels(unittest.TestCase):
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

        myMvars=IndexedSet({
            MVar(
                    'a'
                    ,computerNames=[] # empty list, consequently only available when explicitly defined. 
                    ,description= """ a varible we assume to be given """
            )
            ,MVar(
                    'b'
                    ,computerNames=['b_from_a']
            )
            ,MVar(
                    'c'
                    ,computerNames=['c_from_b']
            )
            ,MVar(
                    'd'
                    ,computerNames=['d_from_a_c']
            )
            ,MVar( 'f' ,computerNames=['f_from_e'])
            ,MVar( 'e' )
        })
        myComputers=IndexedSet({
            Computer(
                'd_from_a_c'
                ,func=lambda a,c:(a+3)+c # we make it consistent to the other computeer d_from_b_c
                ,arg_names=[ 'a' ,'c' ]
                ,description="""computes d from a  and c """
            )
            ,Computer(
                'd_from_b_c'
                ,func=lambda b,c:b+c
                ,arg_names=[ 'b' ,'c' ]
                ,description="""computes d from a  and c """
            )
            ,Computer(
                'c_from_b'
                ,func=lambda b:2*b
                ,arg_names=['b']
                ,description="""computes c from b"""
            )
            ,Computer(
                'b_from_a'
                ,func=lambda a: a+3
                ,arg_names=['a']
                ,description="""computes b from a"""
            )
            ,Computer(
                'f_from_e'
                ,func=lambda e: e**2
                ,arg_names=['e']
                ,description="""computes f from e"""
            )
        })
        names_of_available_mvars=frozenset(['a']) 
        
        # check computers 
        
        self.assertTrue(    myComputers['b_from_a'].is_computable(myMvars,myComputers,names_of_available_mvars))

        #c is recursively computable through b
        self.assertTrue(    myComputers['c_from_b'].is_computable(myMvars,myComputers,names_of_available_mvars))
        
        #d is recursively computable through c
        self.assertTrue(    myComputers['d_from_a_c'].is_computable(myMvars,myComputers,names_of_available_mvars))
        
        #d is recursively computable through b and c
        self.assertTrue(    myComputers['d_from_b_c'].is_computable(myMvars,myComputers,names_of_available_mvars))
        
        #f is not computable since e is neither defined nor computable
        self.assertTrue(not myComputers['f_from_e'].is_computable(myMvars,myComputers,names_of_available_mvars))
      
        # check mvars separately
        self.assertTrue(    myMvars['a'].is_computable(myMvars,myComputers,names_of_available_mvars))
        self.assertTrue(    myMvars['b'].is_computable(myMvars,myComputers,names_of_available_mvars))
        self.assertTrue(    myMvars['c'].is_computable(myMvars,myComputers,names_of_available_mvars))
        self.assertTrue(    myMvars['d'].is_computable(myMvars,myComputers,names_of_available_mvars))
        self.assertTrue(not myMvars['e'].is_computable(myMvars,myComputers,names_of_available_mvars))
        self.assertTrue(not myMvars['f'].is_computable(myMvars,myComputers,names_of_available_mvars))

        mvars=computable_mvars(
                allMvars=myMvars
                ,allComputers=myComputers
                ,names_of_available_mvars=frozenset(['a']) 
        )
        pe('mvars',locals())


    def test_computability_bgc(self):
        # here we test the (growing) sets of Mvars and Computers included in the packe
        from bgc_md.resolve.MvarsAndComputers import Mvars as myMvars
        from bgc_md.resolve.MvarsAndComputers import Computers as myComputers
        
        
        ##compute the set of computable Mvars from the names of defined variables 
        names_of_available_mvars=frozenset([
                         'coord_sys'
                        ,'state_vector' 
                        ,'time_symbol' 
                        ,'compartmental_dyad' 
                        ,'input_vector']) 
        C=myComputers['srm_bu_tens']
        ref=( 'coord_sys' ,'state_vector' ,'time_symbol' ,'compartmental_dyad' ,'input_vector' )
        #pe('C.arg_names',locals())
        #pe('ref',locals())
        self.assertEqual( C.arg_names , ref)
        
        mvars=computable_mvars(
                allMvars=myMvars
                ,allComputers=myComputers
                ,names_of_available_mvars=names_of_available_mvars
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

