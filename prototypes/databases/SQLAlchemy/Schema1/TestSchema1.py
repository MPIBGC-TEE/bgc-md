# This prototype uses the SQL Expression Language of SQLAlchemy
# we could have done the same much simpler using the ORM
# to do:
# 1.) in the tests retrieve the tables from the database instead of attaching them to the TestInstance
#     since this reflects
# 2.) There are datbase constraints that are not reflected yet 
#     1.) A variable can be either BaseVariable or DerivedVariable not both
#         so the BaseVariables table needs a constraint that blocks the addition of a Symbol already present
#         in DerivedVariables and vice versa
import unittest
import exampleModels
from sqlalchemy import Table, Column, Integer, String, MetaData,ForeignKey,ForeignKeyConstraint
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sympy import Matrix,sympify,symbols,Symbol
from testinfrastructure.helpers import pe
from createTables import createTables
from helpers import addModel,resolve

class TestSchema1(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the structure of the different ways to structure the 
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
        StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
        # now query
        # we use the c collection for the columns
        s = select([StateVectorPositions.c.symbol]).where(StateVectorPositions.c.model_id== model_id).order_by(StateVectorPositions.c.pos_id)
        sym_list=[Symbol(str(row[0])) for row in conn.execute(s)]
        pe('sym_list',locals())
        stateVector=Matrix(sym_list)

        vl, vw = symbols('vl,vw')

        ref=Matrix([vl, vw])
        self.assertEqual(stateVector,ref)

    #@unittest.skip
    def test_resolve_derived_variable(self):
        metadata=self.metadata
        engine=self.engine
        model_id='default_2'
        exampleModels.addOnePoolModel(metadata,engine,model_id,'test')

        res=resolve(metadata,engine,Symbol("NetFlux"),model_id)
        ref=sympify('kIvl*vl-kOvl*vl')

    @unittest.skip
    def test_matrix_variables(self):
        metadata=self.metadata
        engine=self.engine
        exampleModels.addFivePoolModel(metadata,engine,'default_3','matrix test')
        conn=engine.connect()
    #    #         .
    #    #       ⎡vl⎤   ⎡⎡_,_⎤⎡_,_,_⎤⎤   ⎡vl⎤  ⎡I_a⎤
    #    #       ⎢v_b⎥   ⎢⎣_,_⎦⎣_,_,_⎦⎥   ⎢v_b⎥  ⎢I_b⎥
    #    #       ⎢s_a⎥ = ⎢⎡_,_⎤⎡_,_,_⎤⎥ * ⎢s_a⎥ +⎢I_a⎥
    #    #       ⎢s_b⎥   ⎢⎢_,_⎦⎢_,_,_⎦⎥   ⎢s_b⎥  ⎢I_b⎥
    #    #       ⎣s_c⎦   ⎣⎣_,_⎦⎣_,_,_⎦⎦   ⎣s_c⎦  ⎣I_c⎦
    #    # 
    #    #  The input to the vegetation is often written like this 
    #    #
    #    #   ⎡I_a⎤   ⎡b_a⎤
    #    #   ⎢   ⎥ = ⎢   ⎥* u 
    #    #   ⎣I_b⎦   ⎣b_b⎦


    #    # The test demonstrates how 
    #    #    ⎡b_a⎤
    #    #    ⎢   ⎥ and u 
    #    #    ⎣b_b⎦
    #    # can be retrieved from the database
    #    # although it is not stored directly in it.
    #    conn                        =  self.conn
    #    engine                      =  self.engine
    #    StateVectorPositions        =  self.StateVectorPositions
    #    BaseVariables               =  self.BaseVariables
    #    Models                      =  self.Models
    #    #InFluxes                    =  self.InFluxes
    #    #OutFluxes                   =  self.OutFluxes
    #    #InternalFluxes              =  self.InternalFluxes
    #    # if we can express b dirctly by variables defined in the original database entry for the model
    #    # we can do this
    #    #s = select([Expressions.c.symbol]).where(Expressions.c.symbol== 'default_1.yaml' and )
    #    #b=Matrix([b_a,b_b])
    #    
    #    
    #    
    #   # # we create an extra stateVecotorPositions table to reflect our special ordering of variables 
    #   # # could be the same but does not have to
    #   # metadata = MetaData()
    #   # MyStateVectorPositions= Table('MyStateVectorPositions', metadata,
    #   # 	Column('pos_id', Integer ),
    #   # 	Column('symbol',None),
    #   # 	Column('model_id',None),
    #   # 	ForeignKeyConstraint(['symbol', 'model_id'], ['BaseVariables.symbol', 'BaseVariables.model_id'])
    #   # )
    #   # metadata.create_all(engine)
    #   # conn.execute(
    #   # 	MyStateVectorPositions.insert(),
    #   # 	[
    #   #         {'pos_id':0,'symbol':"vl",'model_id':"default_1.yaml"},
    #   #         {'pos_id':1,'symbol':"v_b",'model_id':"default_1.yaml"},
    #   #         {'pos_id':2,'symbol':"s_a",'model_id':"default_1.yaml"},
    #   #         {'pos_id':3,'symbol':"s_b",'model_id':"default_1.yaml"},
    #   #         {'pos_id':4,'symbol':"s_c",'model_id':"default_1.yaml"}
    #   # 	]
    #   # )






