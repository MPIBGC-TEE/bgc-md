# The purpose of this Schema is to work backwards from the minimal requirement that the 
# an Instance of CompartmentalModel can be created.
# So a model consists at minimum constructor call.
# and possibly some variable definitions to populate the namespace in which the constructor is called. 


import unittest
#import exampleModels
from sqlalchemy import Table, Column, Integer, String, MetaData,ForeignKey,ForeignKeyConstraint
from sqlalchemy import create_engine
from sqlalchemy.sql import select
#from sympy import Matrix,sympify,symbols,Symbol,IndexedBase
from testinfrastructure.helpers import pe
#from createTables import createTables
#from sympy import Basic,Symbol,Matrix,symbols
from sympy.vector import CoordSysND, Vector,express
from helpers import getModelDescriptor
from helpers import get


class TestSchema(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the information that is neccessary to build the 
    # compartmental Matrix
    # Conceptually we want to separate this information from the database, which should only hold
    # the Variables and the statevectorpositions which together already determine the matrices

    #def setUp(self):
    #    engine = create_engine('sqlite:///:memory:')
    #    metadata = MetaData()
    #    
    #    # build the tables
    #    Models=Table(
    #        'Models'
    #        ,metadata
    #    	,Column('id', String, primary_key=True)
    #    	,Column('name', String)
    #    )
    #    metadata.create_all(engine)

    #    self.metadata=metadata
    #    self.engine=engine

    def test_CS_creation(self):
        #metadata = self.metadata
        #engine   = self.engine
        #Models=Table("Models",metadata,autoload=True,autoload_with=engine)
        #model_id="testFivePool"
        #model_name="test"
        #conn=engine.connect()
        #conn.execute(
        #    Models.insert(),
        #    [
        #        {'id':model_id,'name':model_name},
        #    ]
        #)
        md=get(model_id='testFivePool',callString='get_ModelDescriptor()')
        pe('md.compartmental_matrix',locals())




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
        

