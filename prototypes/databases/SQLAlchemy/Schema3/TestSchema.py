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
f#rom sympy import Basic,Symbol,Matrix,symbols
from sympy.vector import CoordSysND, Vector,express


class TestSchema(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the information that is neccessary to build the 
    # compartmental Matrix
    # Conceptually we want to separate this information from the database, which should only hold
    # the Variables and the statevectorpositions which together already determine the matrices

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        metadata = MetaData()
        
        # build the tables
        Models=Table('Models', metadata,
        	Column('folder_name', String(50), primary_key=True),
        	Column('name', String(100))
        )
        CsCreatorExpressions= Table(
            'DerivedVariables'
            ,metadata
            ,Column('model_id', String(),   primary_key=True)
            ,Column('nr',       Integer,    primary_key=True) # there could be more than one way to define a model and not all definitions can be mapped to all others so we could check for consistency instead of avoiding duplication
            Column('expression', String)
        )
        metadata.create_all(engine)

        self.metadata=metadata
        self.engine=engine

    def test_CS_creation(self):
        metadata = self.metadata
        engine   = self.engine
        Models=Table("Models",metadata,autoload=True,autoload_with=engine)
        CsCreatorExpressions=Table("CsCreatorExpressions",metadata,autoload=True,autoload_with=engine)
        model_id="default_1"
        model_name="test"
        conn=engine.connect()
        conn.execute(
            Models.insert(),
            [
                {'folder_name':model_id,'name':model_name},
            ]
        )
        conn.execute(
            CsCreatorExpressions.insert(),
            [
                {'folder_name':model_id,'nr':1,'expression':CS_from },
            ]
        )




        

