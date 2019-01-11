# This prototype uses the SQL Expression Language of SQLAlchemy
# possibly we could have done the it simpler using the ORM
# The purpose is however to identify the relational model

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
        #,geometric_resolve
        #,symbolic_resolve
        #,resolveMatrix
        #,resolveVector
        ,addStateVariableOrdering
        ,getStateVector
        ,addDerivedVariable
        #,get_name_spaces
        ,getHighestExecutionOrder
)


class TestIndexedVariables(unittest.TestCase):
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
    # depend on the ordering of the pools (the coordinate system), 
    # although this is not relevant for the solution. 
    
    # Furthermore different orderings are usefull for different purposes (clustering different soil levels or all microbial pools, or ..)
    # Therefore if we define tuple/or matrix valued variables we implicitly always define them along with an ordering of the state variables 
    
    # The block-matrix-decomposition is NOT preserved under general permutations 
    # of the order of state variables.(Only for those permutations inside blocks)
    # On the other hand sums and products of matrices ARE preserved under coordinate transformations. 
    # In order to be able to retrieve the vegetation part after a variable transformation 
    # (e.g. a permutation)
    # We could therefore write the above equation with full sized matrices and vectors as
    #         .       .       .
    #       ⎡v_l⎤   ⎡v_l⎤   ⎡ 0 ⎤ 
    #       ⎢v_w⎥   ⎢v_w⎥   ⎢ 0 ⎥ 
    #       ⎢   ⎥ = ⎢   ⎥ + ⎢   ⎥ 
    #       ⎢s_f⎥   ⎢ 0 ⎥   ⎢s_f⎥ 
    #       ⎢s_s⎥   ⎢ 0 ⎥   ⎢s_s⎥ 
    #       ⎣s_b⎦   ⎣ 0 ⎦   ⎣s_b⎦ 
    
    #                 ⎡ ⎡ V_11,  V_12  0  ,  0  ,   0  ⎤
    #                 ⎢ ⎢ V_21,  V_22  0  ,  0  ,   0  ⎥
    #               = ⎢ ⎢  0  ,   0    0  ,  0  ,   0  ⎥
    #                 ⎢ ⎢  0  ,   0    0  ,  0  ,   0  ⎥
    #                 ⎣ ⎣  0  ,   0    0  ,  0  ,   0  ⎦
    #
    #                   ⎡  0  ,   0  VS_11,VS_12, VS_13⎤ 
    #                   ⎢  0  ,   0  VS_21,VS_22, VS_23⎥        
    #               +   ⎢  0  ,   0    0  ,  0  ,   0  ⎥ 
    #                   ⎢  0  ,   0    0  ,  0  ,   0  ⎥ 
    #                   ⎣  0  ,   0    0  ,  0  ,   0  ⎦ 
    #                   
    #                   ⎡  0  ,   0    0  ,  0  ,   0  ⎤ 
    #                   ⎢  0  ,   0    0  ,  0  ,   0  ⎥ 
    #               +   ⎢SV_11, SV_12  0  ,  0  ,   0  ⎥ 
    #                   ⎢SV_21, SV_22  0  ,  0  ,   0  ⎥ 
    #                   ⎣SV_31, SV_32  0  ,  0  ,   0  ⎦ 
    #                   
    #                   ⎡  0  ,   0    0  ,  0  ,   0  ⎤ ⎤   ⎡ ⎡v l⎤   ⎡ 0 ⎤ ⎤  
    #                   ⎢  0  ,   0    0  ,  0  ,   0  ⎥ ⎥   ⎢ ⎢v w⎥   ⎢ 0 ⎥ ⎥  
    #               +   ⎢  0  ,   0   S_11, S_12,  S_13⎥ ⎥ * ⎢ ⎢ 0 ⎥ + ⎢s f⎥ ⎥  
    #                   ⎢  0  ,   0   S_21, S_22,  S_23⎥ ⎥   ⎢ ⎢ 0 ⎥   ⎢s s⎥ ⎥  
    #                   ⎣  0  ,   0   S_31, S_32,  S_33⎦ ⎦   ⎣ ⎣ 0 ⎦   ⎣s b⎦ ⎦  
    #
    #                   ⎡I_l⎤   ⎡ 0 ⎤
    #                   ⎢I_w⎥   ⎢ 0 ⎥
    #               +   ⎢ 0 ⎥ + ⎢I_f⎥
    #                   ⎢ 0 ⎥   ⎢I_s⎥
    #                   ⎣ 0 ⎦   ⎣I_b⎦
    #
    # These buildig blocks can be transformed in the usual way, e.g. 
    # 
    #  in the default statevariable ordering we have
    #
    #                  ⎡ V_11,  V_12,  0  ,  0  ,   0  ⎤
    #                  ⎢ V_21,  V_22,  0  ,  0  ,   0  ⎥
    #              V = ⎢  0  ,   0  ,  0  ,  0  ,   0  ⎥
    #                  ⎢  0  ,   0  ,  0  ,  0  ,   0  ⎥
    #                  ⎣  0  ,   0  ,  0  ,  0  ,   0  ⎦
    #                                
    # after the permutaion we have: V'= P * V * P^-1, for instance (for a permutation P that
    # exchanges row 2 and 5 in the original statevector)
    #                                
    #                  ⎡ V_11,   0  ,  0  ,  0  , V_12 ⎤
    #                  ⎢  0  ,   0  ,  0  ,  0  ,  0   ⎥
    #              V'= ⎢  0  ,   0  ,  0  ,  0  ,  0   ⎥
    #                  ⎢  0  ,   0  ,  0  ,  0  ,  0   ⎥
    #                  ⎣ V_21,   0  ,  0  ,  0  , V_22 ⎦
    #
    # which still contains only vegetation related entries although it is not a block matrix anymore.
    
    # The purpose of these tests is to infer what kind of information we can retrieve depending 
    # on the storage scheme we choose.
    def setUp(self):
        #engine = create_engine('sqlite:///:memory:', echo=True)
        #metadata = MetaData()

        metadata,engine=createTables()
        self.metadata=metadata
        self.engine=engine


    def test_scalar_invariants(self):
        # Take a coordinate independent scalar like the complete influx to the vegetation pools
        # 
        # NetVegIn=I_l+I_w
        # 
        # Since we store expressions as strings a user could by means of some indexed variables
        # 
        # I =Matrix([I_l,I_w,I_f,I_s,I_b])                        
        # 
        # NetVegIn=I[0]+I[1]
        #
        # The indices 0 and 1 are only correct for coordinate systems where I_l and I_w are the first
        # two components. This has the following implications
        # 1.)   We have to store the coordinate system along with the variables
        # 2.)   All expressions that depend on  an indexed expression are only valid in the original coordinate 
        #       system and must therefore be executed there to get the value

        metadata=self.metadata
        engine=self.engine
        model_id='default_2'
        exampleModels.addFivePoolModel(metadata,engine,model_id,'matrix test')
        
        addDerivedVariable(
             metadata
            ,engine
            ,model_id
            ,symbol='I'
            ,description='net influx to vegetation pools'
            ,expression='Matrix([Ivl,Ivw,0,0,0])'                        
            ,execution_order=22
            ,coord_system_id=defaultOrderingName
            
        )
        addDerivedVariable(
             metadata
            ,engine
            ,model_id=model_id
            ,symbol='NetVegIn'
            ,description='Input tuple'
            ,expression='sum(I[0:2])'
            ,execution_order=23
            ,coord_system_id=defaultOrderingName
            
        )

        res_0 = resolve(metadata,engine,"NetVegIn",model_id,coord_system_id=defaultOrderingName)

        my_ordering_name='veg_2'

        addStateVariableOrdering(metadata,engine,model_id,state_variable_symbols=[ "sb", "vl","sf", "ss","vw"],coord_system_id=my_ordering_name)
        res_1 = resolve(metadata,engine,"NetVegIn",model_id,coord_system_id=my_ordering_name)
        self.assertEqual(res_0,res_1)

        # now assume that the target variable has NOT been defined with respect to the same coordinate system as the variables it depends on

        # we have to make sure that we get an exception if we try

        
        addDerivedVariable(
             metadata
            ,engine
            ,model_id=model_id
            ,symbol='NetVegIn2'
            ,description='cummulative Input to all vegetation pools'
            ,expression='sum(I[1]+I[4])'
            ,execution_order=23
            ,coord_system_id=my_ordering_name
            
        )
        with self.assertRaises(Exception) as e:
            res_1 = resolve(metadata,engine,"NetVegIn2",model_id,coord_system_id=my_ordering_namea)

    
    def test_vector_component_transformation(self):
        # Take a vectr like the influx to the model 
        # 
        # The components may be given by a matrix
        # 
        # I =Matrix([I_l,I_w,I_f,I_s,I_b])                        
        # 

        metadata=self.metadata
        engine=self.engine
        model_id='default_2'
        exampleModels.addFivePoolModel(metadata,engine,model_id,'matrix test')
        
        addDerivedVariable(
             metadata
            ,engine
            ,model_id
            ,symbol='I'
            ,description='influx vector components'
            ,expression='Matrix([Ivl,Ivw,0,0,0])'                        
            ,execution_order=22
            ,coord_system_id=defaultOrderingName
            
        )
        # We can resolve it in any coordinate system if we know the transformation of the base vectors
        # (which in our case will be a permutation)
        res_0 = resolve(metadata,engine,"I",model_id,coord_system_id=defaultOrderingName)
        self.assertEqual(res_0,sympify('Matrix([Ivl,kIvw*vw,0,0,0])'))                      

        # we add a permutation 
        my_ordering_name='veg_2'
        addStateVariableOrdering(metadata,engine,model_id,state_variable_symbols=[ "sb", "vl","sf", "ss","vw"],coord_system_id=my_ordering_name)
        res_1 = resolve(metadata,engine,"I",model_id,coord_system_id=my_ordering_name)
        self.assertEqual(res_1,sympify('Matrix([0,Ivl,0,0,kIvw*vw])'))

        # now assume that the target variable is not a columnvector of size n 
        # or a matrix of size nxn

        # we have to make sure that we get an exception if we try to transform 
        # something of this kind
        addDerivedVariable(
             metadata
            ,engine
            ,model_id
            ,symbol='Iveg'
            ,description='net influx to vegetation pools'
            ,expression='Matrix([Ivl,Ivw])'                        
            ,execution_order=23
            ,coord_system_id=defaultOrderingName
            
        )
        with self.assertRaises(Exception) as e:
            res_1 = resolve(metadata,engine,"Iveg",model_id,coord_system_id=my_ordering_namea)


        


    
