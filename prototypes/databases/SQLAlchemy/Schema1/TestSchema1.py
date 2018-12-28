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
from helpers import defaultOrderingName,addModel,resolve,resolveMatrix,resolveVector,addMatrix,addStateVariableOrdering,getStateVector

class TestSchema1(unittest.TestCase):
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
        # try to add an ordering with more state variables
        with self.assertRaises(Exception) as cm:
            addStateVariableOrdering(metadata,engine,model_id,state_variable_symbols=["vw", "vl", "sf", "ss", "sb"],ordering_id=my_ordering_name)
        #pe('cm.exception',locals())

        # add a new ordering with positions reversed
        addStateVariableOrdering(metadata,engine,model_id,state_variable_symbols=["vw", "vl"],ordering_id=my_ordering_name)

        stateVector=getStateVector(metadata,engine,model_id,my_ordering_name)
        vl, vw = symbols('vw,vl')
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
        # We invent a minimal ecosystem model with 2 vegetation and 3 soil pools and write it 
        # in block-matrix-form
        #          .
        #       ⎡⎡v_l⎤⎤   ⎡⎡ V_11,  V_12⎤⎡VS_11,VS_12, VS_13⎤⎤   ⎡⎡v l⎤⎤  ⎡⎡I_l⎤⎤
        #       ⎢⎣v_w⎦⎥   ⎢⎣ V_21,  V_22⎦⎣VS_21,VS_22, VS_23⎦⎥   ⎢⎣v w⎦⎥  ⎢⎣I_w⎦⎥
        #       ⎢     ⎥   ⎢                                  ⎥   ⎢     ⎥  ⎢     ⎥
        #       ⎢⎡s_f⎤⎥ = ⎢⎡SV_11, SV_12⎤⎡ S_11, S_12,  S_13⎤⎥ * ⎢⎡s f⎤⎥ +⎢⎡I_f⎤⎥
        #       ⎢⎢s_s⎥⎥   ⎢⎢SV_21, SV_22⎥⎢ S_21, S_22,  S_23⎥⎥   ⎢⎢s s⎥⎥  ⎢⎢I_s⎥⎥
        #       ⎣⎣s_b⎦⎦   ⎣⎣SV_31, SV_32⎦⎣ S_31, S_32,  S_33⎦⎦   ⎣⎣s b⎦⎦  ⎣⎣I_b⎦⎦
        # 
        # The input to the vegetation is often written as a product of distribution vector b and a scalar u
        #
        #   ⎡Il⎤   ⎡bl⎤
        #   ⎢  ⎥ = ⎢  ⎥* u 
        #   ⎣Iw⎦   ⎣bw⎦
        #
        # and models are compared with respect to \vec{b} or \tens{V} 
        # It is therefore desirable to be able to extract this information from the database.

        # On the other hand storing this information in the database 
        # has to account for the fact that matrix and vector valued variables 
        # depend on the ordering of the pools, 
        # although this is not relevant for the solution. 

        # Furthermore different orderings are usefull for different purposes (clustering different soil levels or all microbial pools, or ..)
        # Therefore if we define vector/or matrix valued variables we implicitly always define them along with an ordering of the state variables 

        # The block-matrix-decomposition is NOT preserved under general permutations 
        # of the order of state variables.(Only for those permutations inside blocks)
        # On the other hand sums and products of matrices ARE preserved under coordinate transformations. 
        # In order to be able to retrieve the vegetation part after a variable transformation 
        # (e.g. a permutation)
        # We could therefore write the above equation as
        #          .         .         .
        #       ⎡⎡v_l⎤⎤   ⎡⎡v_l⎤⎤   ⎡⎡ 0 ⎤⎤ 
        #       ⎢⎣v_w⎦⎥   ⎢⎣v_w⎦⎥   ⎢⎣ 0 ⎦⎥ 
        #       ⎢     ⎥ = ⎢     ⎥ + ⎢     ⎥ 
        #       ⎢⎡s_f⎤⎥   ⎢⎡ 0 ⎤⎥   ⎢⎡s_f⎤⎥ 
        #       ⎢⎢s_s⎥⎥   ⎢⎢ 0 ⎥⎥   ⎢⎢s_s⎥⎥ 
        #       ⎣⎣s_b⎦⎦   ⎣⎣ 0 ⎦⎦   ⎣⎣s_b⎦⎦ 

        #                 ⎡ ⎡⎡ V_11,  V_12⎤⎡  0  ,  0  ,   0  ⎤⎤
        #                 ⎢ ⎢⎣ V_21,  V_22⎦⎣  0  ,  0  ,   0  ⎦⎥
        #                 ⎢ ⎢                                  ⎥
        #               = ⎢ ⎢⎡  0  ,   0  ⎤⎡  0  ,  0  ,   0  ⎤⎥
        #                 ⎢ ⎢⎢  0  ,   0  ⎥⎢  0  ,  0  ,   0  ⎥⎥
        #                 ⎣ ⎣⎣  0  ,   0  ⎦⎣  0  ,  0  ,   0  ⎦⎦
        #
        #                   ⎡⎡  0  ,   0  ⎤⎡VS_11,VS_12, VS_13⎤⎤ 
        #                   ⎢⎣  0  ,   0  ⎦⎣VS_21,VS_22, VS_23⎦⎥        
        #                 + ⎢                                  ⎥ 
        #                   ⎢⎡  0  ,   0  ⎤⎡  0  ,  0  ,   0  ⎤⎥ 
        #                   ⎢⎢  0  ,   0  ⎥⎢  0  ,  0  ,   0  ⎥⎥ 
        #                   ⎣⎣  0  ,   0  ⎦⎣  0  ,  0  ,   0  ⎦⎦ 
        #                   
        #                   ⎡⎡  0  ,   0  ⎤⎡  0  ,  0  ,   0  ⎤⎤ 
        #                   ⎢⎣  0  ,   0  ⎦⎣  0  ,  0  ,   0  ⎦⎥ 
        #                 + ⎢                                  ⎥ 
        #                   ⎢⎡SV_11, SV_12⎤⎡  0  ,  0  ,   0  ⎤⎥ 
        #                   ⎢⎢SV_21, SV_22⎥⎢  0  ,  0  ,   0  ⎥⎥ 
        #                   ⎣⎣SV_31, SV_32⎦⎣  0  ,  0  ,   0  ⎦⎦ 
        #                   
        #                   ⎡⎡  0  ,   0  ⎤⎡  0  ,  0  ,   0  ⎤⎤ ⎤   ⎡ ⎡⎡v l⎤⎤   ⎡⎡ 0 ⎤⎤ ⎤  
        #                   ⎢⎣  0  ,   0  ⎦⎣  0  ,  0  ,   0  ⎦⎥ ⎥   ⎢ ⎢⎣v w⎦⎥   ⎢⎣ 0 ⎦⎥ ⎥  
        #                 + ⎢                                  ⎥ ⎥ * ⎢ ⎢     ⎥ + ⎢     ⎥ ⎥  
        #                   ⎢⎡  0  ,   0  ⎤⎡ S_11, S_12,  S_13⎤⎥ ⎥   ⎢ ⎢⎡ 0 ⎤⎥   ⎢⎡s f⎤⎥ ⎥  
        #                   ⎢⎢  0  ,   0  ⎥⎢ S_21, S_22,  S_23⎥⎥ ⎥   ⎢ ⎢⎢ 0 ⎥⎥   ⎢⎢s s⎥⎥ ⎥  
        #                   ⎣⎣  0  ,   0  ⎦⎣ S_31, S_32,  S_33⎦⎦ ⎦   ⎣ ⎣⎣ 0 ⎦⎦   ⎣⎣s b⎦⎦ ⎦  
        #
        #                   ⎡⎡I_l⎤⎤   ⎡⎡ 0 ⎤⎤
        #                   ⎢⎣I_w⎦⎥   ⎢⎣ 0 ⎦⎥
        #                   ⎢     ⎥ + ⎢     ⎥
        #                   ⎢⎡ 0 ⎤⎥   ⎢⎡I_f⎤⎥
        #                   ⎢⎢ 0 ⎥⎥   ⎢⎢I_s⎥⎥
        #                   ⎣⎣ 0 ⎦⎦   ⎣⎣I_b⎦⎦

        # Although we can input sparse matrices matrices and vectors that we store should have full size.
        # If we wanted to store block matrices we would be compelled to store their positions and would
        # also be tempted to assemble bigger matrices from them by composition. As mentioned before, it 
        # would be difficult to transform this assembly to a new ordering.
        # We therefore store only full sized matrices presently.


        # The test demonstrates how to extract \vec{b} u and \tens{V}
        # refering to the original ordering in the database 
        #          ⎡ bl⎤
        #          ⎢ bv⎥ 
        # \vec{b} =⎢ 0 ⎥ 
        #          ⎢ 0 ⎥ 
        #          ⎣ 0 ⎦
        
        addMatrix(
            metadata
            ,engine
            ,symbol='b'
            ,description='carbon distribution '
            ,model_id=model_id
            ,ordering_id=defaultOrderingName
            ,expr_str='Matrix([Ivl/NetVegIn,Ivw/NetVegIn,0,0,0])'
        )
        res=resolve(metadata,engine,Symbol('b'),model_id)
        ref = sympify("Matrix([Ivl/(Ivl + kIvw*vw), kIvw*vw/(Ivl + kIvw*vw),0,0,0])")
        self.assertEqual(res,ref)
        pe("res",locals())

        # we could now retrieve the matrices resulting from another ordering of the statevariables
        # (and the time derivatives)
        my_ordering_name='veg_2'
        addStateVariableOrdering(metadata,engine,model_id,state_variable_symbols=["vw", "vl", "sf", "ss", "sb"],ordering_id=my_ordering_name)
        res=resolveVector(metadata,engine,Symbol('b'),model_id,my_ordering_name)
        ref = sympify("Matrix([kIvw*vw/(Ivl + kIvw*vw),Ivl/(Ivl + kIvw*vw),0,0,0])")
        self.assertEqual(res,ref)
        pe("res",locals())
