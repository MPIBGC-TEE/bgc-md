# This prototype uses the SQL Expression Language of SQLAlchemy
# possibly we could have done the it simpler using the ORM
# The purpose is however to identify the relational model

# to do:
# 1.) There are datbase constraints that are not reflected yet 
#     1.) A variable can be either BaseVariable or DerivedVariable not both
#         so the BaseVariables table needs a constraint that blocks the addition of a Symbol already present
#         in DerivedVariables and vice versa
import unittest
import exampleModels
from sqlalchemy import Table, Column, Integer, String, MetaData,ForeignKey,ForeignKeyConstraint
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sympy import Matrix,sympify,symbols,Symbol,IndexedBase
from testinfrastructure.helpers import pe
from createTables import createTables
from sympy import Basic,Symbol,Matrix,symbols
from sympy.vector import CoordSysND, Vector,express
from helpers import (
         defaultOrderingName
        ,addModel
        ,resolve
        ,addStateVariableOrdering
        ,getStateVector
        ,addDerivedVariable
        ,getHighestExecutionOrder
)


class TestSchema(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the information that is neccessary to build the 
    # compartmental Matrix
    # Conceptually we want to separate this information from the database, which should only hold
    # the Variables and the statevectorpositions which together already determine the matrices

    def setUp(self):
        #engine = create_engine('sqlite:///:memory:', echo=True)
        #metadata = MetaData()

        metadata,engine=createTables()
        self.metadata=metadata
        self.engine=engine


    def test_state_vector(self):
        metadata=self.metadata
        engine=self.engine
        conn=engine.connect()
        model_id='default_2'
        exampleModels.addTwoPoolModel(metadata,engine,model_id,'twoPoolModel')
        stateVector=getStateVector(metadata,engine,model_id)
        vl, vw = symbols('vl,vw')
        ref=Matrix([vl, vw])
        self.assertEqual(stateVector,ref)
    
    def test_second_state_variable_ordering(self):
        metadata=self.metadata
        engine=self.engine
        conn=engine.connect()
        model_id='default_2'
        exampleModels.addTwoPoolModel(metadata,engine,model_id,'twoPoolModel')
        # add a new ordering  
        my_ordering_name='veg_2'

        # make sure that an attempt to add an ordering with more state variables raises an exception
        with self.assertRaises(Exception) as cm:
            addStateVariableOrdering(metadata,engine,model_id,state_variable_symbols=["vw", "vl", "sf", "ss", "sb"],coord_system_id=my_ordering_name)

        # add a new ordering with positions reversed
        addStateVariableOrdering(metadata,engine,model_id,state_variable_symbols=["vw", "vl"],coord_system_id=my_ordering_name)
        stateVector=getStateVector(metadata,engine,model_id,my_ordering_name)
        vl, vw = symbols('vl,vw')
        ref=Matrix([vw,vl])
        self.assertEqual(stateVector,ref)

    #@unittest.skip
    def test_resolve_derived_variable(self):
        metadata=self.metadata
        engine=self.engine
        model_id='default_2'
        exampleModels.addOnePoolModel(metadata,engine,model_id,'test')

        res=resolve(metadata,engine,"NetFlux",model_id)
        ref=sympify('kIvl*vl-kOvl*vl')
        # also base variables should be resolved (just to Symbols) 
        res=resolve(metadata,engine,"Ivl",model_id)
        ref=sympify('Ivl')
