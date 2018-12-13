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
from helpers import defaultOrderingName,addModel,resolve

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
        # also base variables should be resolved (just to Symbols) 
        res=resolve(metadata,engine,Symbol("Ivl"),model_id)
        ref=sympify('Ivl')

    #@unittest.skip
    def test_matrix_variables(self):
        metadata=self.metadata
        engine=self.engine
        model_id='default_2'
        exampleModels.addFivePoolModel(metadata,engine,model_id,'matrix test')
        conn=engine.connect()
        # We invent a minimal ecosystem model with 2 vegetation and 3 soil pools
        #        .
        #       ⎡vl⎤   ⎡⎡_,_⎤⎡_,_,_⎤⎤   ⎡vl⎤  ⎡Il⎤
        #       ⎢vw⎥   ⎢⎣_,_⎦⎣_,_,_⎦⎥   ⎢vw⎥  ⎢Iw⎥
        #       ⎢sf⎥ = ⎢⎡_,_⎤⎡_,_,_⎤⎥ * ⎢sf⎥ +⎢If⎥
        #       ⎢ss⎥   ⎢⎢_,_⎦⎢_,_,_⎦⎥   ⎢ss⎥  ⎢Is⎥
        #       ⎣sb⎦   ⎣⎣_,_⎦⎣_,_,_⎦⎦   ⎣sb⎦  ⎣Ib⎦
        # 
        #  The input to the vegetation is often written as a product of distribution vector b and a scalar u
        #
        #   ⎡Il⎤   ⎡bl⎤
        #   ⎢  ⎥ = ⎢  ⎥* u 
        #   ⎣Iw⎦   ⎣bw⎦


        # The test demonstrates how 
        #    ⎡bl⎤
        #    ⎢  ⎥ and u 
        #    ⎣bw⎦
        # can be retrieved from the database although it should not be stored directly in it.
        
        # The reason for not storing this information directly in the database is 
        # that matrix and vector valued variables depend on the ordering of the pools, 
        # which is actually not relevant for the solution. 
        # Thurthermore different orderings are usefull for different purposes (clustering different soil levels or all microbial pools, or ..)

        # Therefore if  we define vector/or matrix valued variables we always define them along with an ordering 
        my_ordering_name='veg_2'
        StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
        conn.execute(
        	StateVectorPositions.insert(),
        	[
                 {'pos_id':0,'symbol':"vl",'model_id':model_id,'ordering_id':my_ordering_name}
                ,{'pos_id':1,'symbol':"vw",'model_id':model_id,'ordering_id':my_ordering_name}
                ,{'pos_id':2,'symbol':"sf",'model_id':model_id,'ordering_id':my_ordering_name}
                ,{'pos_id':3,'symbol':"ss",'model_id':model_id,'ordering_id':my_ordering_name}
                ,{'pos_id':4,'symbol':"sb",'model_id':model_id,'ordering_id':my_ordering_name}
        	]
        )
        #
        # If we can express b by scalar variables defined in the original database entry for the model
        # in case we can do this
        Variables=Table("Variables",metadata,autoload=True,autoload_with=engine)
        s = select([Variables.c.symbol]).where(Variables.c.model_id== model_id )
        Ivl=resolve(metadata,engine,Symbol('Ivl'),model_id)
        Ivw=resolve(metadata,engine,Symbol('Ivw'),model_id)
        NetVegIn=Ivl+Ivw
        bl=Ivl/NetVegIn
        bw=Ivw/NetVegIn
        b=Matrix([bl,bw])
        pe('b',locals())
        
        
        






