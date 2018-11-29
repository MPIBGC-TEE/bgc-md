# This prototype uses the SQL Expression Language of SQLAlchemy
# we could have done the same much simpler using the ORM
# to do:
# in the tests retrieve the tables from the database instead of attaching them to the TestInstance
# since this reflects
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
        	Column('symbol',None),
        	Column('model_id',None),
        	ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        )
        
        InFluxes= Table('InFluxes', metadata,
            Column('expression', String(100)),
            Column('description', String(100)),
        	Column('target_symbol',None, primary_key=True),
        	Column('model_id',None, primary_key=True),
        	ForeignKeyConstraint(['target_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
        )
        OutFluxes= Table('OutFluxes', metadata,
            Column('expression', String(100)),
            Column('description', String(100)),
        	Column('source_symbol',None, primary_key=True),
        	Column('model_id',None, primary_key=True),
        	ForeignKeyConstraint(['source_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
        )
        InternalFluxes= Table('InternalFluxes', metadata,
            Column('expression', String(100)),
            Column('description', String(100)),
        	Column('source_symbol',None, primary_key=True),
        	Column('target_symbol',None, primary_key=True),
        	Column('model_id',None, primary_key=True),
        	ForeignKeyConstraint(['source_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id']),
        	ForeignKeyConstraint(['target_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
        )
        
        metadata.create_all(engine)
        
        # insert data
        conn=engine.connect()
        
        conn.execute(
        	Models.insert(),
        	[
        		{'folder_name':"default_1.yaml",'name':"Ceballos_eco"},
        		{'folder_name':"default_2.yaml",'name':"Ceballos"},
        	]
        )
        	
        conn.execute(
        	Variables.insert(),
        	[
                {'symbol':"v_a"  ,'description':"leaf carbon stock",'unit':"kg",'model_id':"default_1.yaml"},
                {'symbol':"v_b"  ,'description':"root carbon stock",'unit':"kg",'model_id':"default_1.yaml"},
                {'symbol':"s_a"  ,'description':"soil carbon stock",'unit':"kg",'model_id':"default_1.yaml"},
                {'symbol':"s_b"  ,'description':"soil carbon stock",'unit':"kg",'model_id':"default_1.yaml"},
                {'symbol':"s_c"  ,'description':"soil carbon stock",'unit':"kg",'model_id':"default_1.yaml"},
                {'symbol':"u_org",'description':"some variable describing the comulativ vegetation input"  ,'unit':"kg",'model_id':"default_1.yaml"},
                {'symbol':"b_a",'description':"fraction of cumulative vegetation input received by pool v_a"  ,'unit':"kg",'model_id':"default_1.yaml"},
                {'symbol':"b_b",'description':"fraction of cumulative vegetation input received by pool v_b"  ,'unit':"kg",'model_id':"default_1.yaml"},
                {'symbol':"k_r",'description':"root decomprate"  ,'unit':"kg",'model_id':"default_1.yaml"}
        	]
        )
        conn.execute(
        	StateVectorPositions.insert(),
        	[
                {'pos_id':0,'symbol':"v_a",'model_id':"default_1.yaml"},
                {'pos_id':1,'symbol':"v_b",'model_id':"default_1.yaml"},
                {'pos_id':2,'symbol':"s_a",'model_id':"default_1.yaml"},
                {'pos_id':3,'symbol':"s_b",'model_id':"default_1.yaml"},
                {'pos_id':4,'symbol':"s_c",'model_id':"default_1.yaml"}
        	]
        )
        conn.execute(
        	InFluxes.insert(),
        	[
                {'expression':'u_org*u_a','description':'','target_symbol':"v_a",'model_id':"default_1.yaml"},
        	]
        )
        conn.execute(
        	OutFluxes.insert(),
        	[
                {'expression':'x','description':'','source_symbol':"x",'model_id':"default_1.yaml"},
        	]
        )
        conn.execute(
        	InternalFluxes.insert(),
        	[
                {'expression':'x','description':'','source_symbol':"x",'target_symbol':"y",'model_id':"default_1.yaml"},
        	]
        )
        self.conn                   =  conn
        self.metadata               =  metadata
        self.engine                 =  engine
        self.StateVectorPositions   =  StateVectorPositions
        self.Variables              =  Variables
        self.Models                 =  Models
        self.InFluxes               =  InFluxes
        self.OutFluxes              =  OutFluxes
        self.InternalFluxes         =  InternalFluxes

    def test_StateVector(self):
        conn                        =  self.conn
        StateVectorPositions        =  self.StateVectorPositions
        Variables                   =  self.Variables
        Models                      =  self.Models
        InFluxes                    =  self.InFluxes
        OutFluxes                   =  self.OutFluxes
        InternalFluxes              =  self.InternalFluxes
        # now query
        # we use the c collection for the columns
        s = select([StateVectorPositions.c.symbol]).where(StateVectorPositions.c.model_id== 'default_1.yaml').order_by(StateVectorPositions.c.pos_id)
        sym_list=[Symbol(str(row[0])) for row in conn.execute(s)]
        pe('sym_list',locals())
        stateVector=Matrix(sym_list)

        v_a, v_b, s_a, s_b, s_c = symbols('v_a,v_b,s_a,s_b,s_c')

        ref=Matrix([v_a, v_b, s_a, s_b, s_c])
        self.assertEqual(stateVector,ref)

    @unittest.skip
    def test_b_vector(self):
        # ecosystem models would have a vegetation and soil part
        #         .
        #       ⎡v_a⎤   ⎡⎡_,_⎤⎡_,_,_⎤⎤   ⎡v_a⎤  ⎡I_a⎤
        #       ⎢v_b⎥   ⎢⎣_,_⎦⎣_,_,_⎦⎥   ⎢v_b⎥  ⎢I_b⎥
        #       ⎢s_a⎥ = ⎢⎡_,_⎤⎡_,_,_⎤⎥ * ⎢s_a⎥ +⎢I_a⎥
        #       ⎢s_b⎥   ⎢⎢_,_⎦⎢_,_,_⎦⎥   ⎢s_b⎥  ⎢I_b⎥
        #       ⎣s_c⎦   ⎣⎣_,_⎦⎣_,_,_⎦⎦   ⎣s_c⎦  ⎣I_c⎦
        # 
        #  The input to the vegetation is often written like this 
        #
        #   ⎡I_a⎤   ⎡b_a⎤
        #   ⎢   ⎥ = ⎢   ⎥* u 
        #   ⎣I_b⎦   ⎣b_b⎦


        # The test demonstrates how 
        #    ⎡b_a⎤
        #    ⎢   ⎥ and u 
        #    ⎣b_b⎦
        # can be retrieved from the database
        # although it is not stored directly in the database
        conn                        =  self.conn
        engine                      =  self.engine
        StateVectorPositions        =  self.StateVectorPositions
        Variables                   =  self.Variables
        Models                      =  self.Models
        InFluxes                    =  self.InFluxes
        OutFluxes                   =  self.OutFluxes
        InternalFluxes              =  self.InternalFluxes
        # we create an extra stateVecotorPositions table to reflect our special ordering of variables 
        # could be the same but does not have to
        metadata = MetaData()
        MyStateVectorPositions= Table('MyStateVectorPositions', metadata,
        	Column('pos_id', Integer ),
        	Column('symbol',None),
        	Column('model_id',None),
        	ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        )
        metadata.create_all(engine)
        conn.execute(
        	MyStateVectorPositions.insert(),
        	[
                {'pos_id':0,'symbol':"v_a",'model_id':"default_1.yaml"},
                {'pos_id':1,'symbol':"v_b",'model_id':"default_1.yaml"},
                {'pos_id':2,'symbol':"s_a",'model_id':"default_1.yaml"},
                {'pos_id':3,'symbol':"s_b",'model_id':"default_1.yaml"},
                {'pos_id':4,'symbol':"s_c",'model_id':"default_1.yaml"}
        	]
        )
        # the first way to establish the connection is to refer to variables defined in the original database entry for the model
        #b=






