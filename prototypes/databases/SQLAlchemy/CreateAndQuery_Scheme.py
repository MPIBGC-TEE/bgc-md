# This prototype uses the SQL Expression Language of SQLAlchemy
# we could have done the same much simpler using the ORM
import unittest
from sqlalchemy import Table, Column, Integer, String, MetaData,ForeignKey,ForeignKeyConstraint
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sympy import Matrix,sympify,symbols,Symbol
from testinfrastructure.helpers import pe

class TestStructureOfCompartmentalMatrix(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the structure of the different ways to structure the 
    # compartmental Matrix
    # Conceptually we want to separate this information from the database, which should only hold
    # the Variables and the statevectorpositions which together already determine the matrices
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        metadata = MetaData()
        
        # build the tables
        Models=Table('Models', metadata,
        	Column('folder_name', String(50), primary_key=True),
        	Column('name', String(100))
        )
        Variables= Table('Variables', metadata,
            Column('symbol', String(100), primary_key=True),
            Column('description', String),
            Column('unit', String),
            Column('model_id', None, ForeignKey('Models.folder_name') , primary_key=True)
        )
        
        StateVectorPositions= Table('StateVectorPositions', metadata,
        	Column('pos_id', Integer ),
        	Column('variables_symbol',None),
        	Column('variables_model_id',None),
        	ForeignKeyConstraint(['variables_symbol', 'variables_model_id'], ['Variables.symbol', 'Variables.model_id'])
        )
        metadata.create_all(engine)
        
        # insert data
        conn=engine.connect()
        
        conn.execute(
        	Models.insert(),
        	[
        		{'folder_name':"default_1.yaml",'name':"Hilbert"},
        		{'folder_name':"default_2.yaml",'name':"Ceballos"},
        		{'folder_name':"default_3.yaml",'name':"Ceballos_new"}
        	]
        )
        	
        conn.execute(
        	Variables.insert(),
        	[
                {'symbol':"y"  ,'description':"leaf carbon stock",'unit':"kg",'model_id':"default_1.yaml"},
                {'symbol':"x"  ,'description':"root carbon stock",'unit':"kg",'model_id':"default_1.yaml"},
                {'symbol':"k_r",'description':"root decomprate"  ,'unit':"kg",'model_id':"default_1.yaml"}
        	]
        )
        conn.execute(
        	StateVectorPositions.insert(),
        	[
                {'pos_id':0,'variables_symbol':"x",'variables_model_id':"default_1.yaml"},
                {'pos_id':1,'variables_symbol':"y",'variables_model_id':"default_1.yaml"}
        	]
        )
        self.conn=                  conn
        self.StateVectorPositions=  StateVectorPositions
        self.Variables=             Variables
        self.Models=                Models

    def test_StateVector(self):
        conn=                 self.conn
        StateVectorPositions= self.StateVectorPositions
        Variables=            self.Variables
        Models=               self.Models
        # now query
        # we use the c collection for the columns
        s = select([StateVectorPositions.c.variables_symbol]).where(StateVectorPositions.c.variables_model_id== 'default_1.yaml').order_by(StateVectorPositions.c.pos_id)
        sym_list=[Symbol(str(row[0])) for row in conn.execute(s)]
        pe('sym_list',locals())
        stateVector=Matrix(sym_list)
        x,y=symbols('x,y')
        ref=Matrix([x,y])
        self.assertEqual(stateVector,ref)
    def test_b_vector(self):
        # we create an extra table outside the database in the usercode
        conn=                 self.conn
        StateVectorPositions= self.StateVectorPositions
        Variables=            self.Variables
        Models=               self.Models




