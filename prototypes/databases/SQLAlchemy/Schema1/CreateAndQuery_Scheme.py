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
from sqlalchemy import Table, Column, Integer, String, MetaData,ForeignKey,ForeignKeyConstraint
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sympy import Matrix,sympify,symbols,Symbol
from testinfrastructure.helpers import pe
from createTables import createTables
from addFivePoolModel import addFivePoolModel
from helpers import addModel
class TestStructureOfCompartmentalMatrix(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the structure of the different ways to structure the 
    # compartmental Matrix
    # Conceptually we want to separate this information from the database, which should only hold
    # the Variables and the statevectorpositions which together already determine the matrices
    def setUp(self):
        #engine = create_engine('sqlite:///:memory:', echo=True)
        #metadata = MetaData()

        self.metadata,self.engine=createTables()


    def test_StateVector(self):
        metadata=self.metadata
        engine=self.engine
        conn=engine.connect()
        addFivePoolModel(metadata,engine)
        StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
        # now query
        # we use the c collection for the columns
        s = select([StateVectorPositions.c.symbol]).where(StateVectorPositions.c.model_id== 'default_1.yaml').order_by(StateVectorPositions.c.pos_id)
        sym_list=[Symbol(str(row[0])) for row in conn.execute(s)]
        pe('sym_list',locals())
        stateVector=Matrix(sym_list)

        v_a, v_b, s_a, s_b, s_c = symbols('v_a,v_b,s_a,s_b,s_c')

        ref=Matrix([v_a, v_b, s_a, s_b, s_c])
        self.assertEqual(stateVector,ref)

    def test_resolve_derived_Variable(self):
        metadata=self.metadata
        engine=self.engine
        conn=engine.connect()
        base_variables = [
             { 'symbol':"k_a"  ,'description':"decomprate"                              ,'dimension':"1/time"   }
            ,{ 'symbol':"kv_a" ,'description':"leaf respiration rate"                   ,'dimension':"1/time"   }
            ,{ 'symbol':"ki_v_b" ,'description':"leaf respiration rate"                   ,'dimension':"1/time"   }
    	]
        derived_variables = [
             { 'symbol':"u_org"     ,'description':"some variable describing the comulativ vegetation input"    ,'expression':"Iv_a+Iv_b"}
    	]
        base_in_fluxes=[
            {
                'symbol':"Iv_a" 
                ,'description':"External influx into compartment v_a"    
                ,'dimension':"mass/time"# fixme: this should be derived from the target_symbol which must be a state variable
                ,'target_symbol':"v_a"
            }
        ]
        derived_in_fluxes=[
            {
                'symbol':"Iv_b" 
                ,'description':"External influx into compartment v_b"    
                ,'expression':"v_b*ki_v_b"
                ,'target_symbol':"v_b"
            }
        ]
        derived_out_fluxes=[
            {
                'symbol':"Ov_a" 
                ,'description':"External Outflux out of compartment v_a =leaf respiration"    
                ,'expression':"kv_a*v_a"
                ,'source_symbol':"v_a"
            }
        ]
        derived_internal_fluxes=[
            { 
                'symbol':"INTv_a_v_b"
                ,'description':"root leaf transfer"                                         
                ,'expression':"k_a*v_a"  
                ,'source_symbol':"v_a"
                ,'target_symbol':"v_b"
            }
        ]

        state_variables= [ 
             { 'symbol':"v_a" ,'description':"leaf pool" }
            ,{ 'symbol':"v_b" ,'description':"wood pool" }
        ]
        
        addModel(
            metadata
            ,engine
            ,'default_2'
            ,'MarkusMadeUpVegModel'
            ,state_variables
            ,base_variables
            ,derived_variables
            ,base_in_fluxes
            ,derived_in_fluxes
            ,derived_out_fluxes
            ,derived_internal_fluxes
        )
        #StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
        # prove that we can reconstruct the fluxes as functions of the BaseVariables
    #@unittest.skip
    #def test_b_vector(self):
    #    # ecosystem models would have a vegetation and soil part
    #    #         .
    #    #       ⎡v_a⎤   ⎡⎡_,_⎤⎡_,_,_⎤⎤   ⎡v_a⎤  ⎡I_a⎤
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
    #   #         {'pos_id':0,'symbol':"v_a",'model_id':"default_1.yaml"},
    #   #         {'pos_id':1,'symbol':"v_b",'model_id':"default_1.yaml"},
    #   #         {'pos_id':2,'symbol':"s_a",'model_id':"default_1.yaml"},
    #   #         {'pos_id':3,'symbol':"s_b",'model_id':"default_1.yaml"},
    #   #         {'pos_id':4,'symbol':"s_c",'model_id':"default_1.yaml"}
    #   # 	]
    #   # )






