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
from sympy import Matrix,sympify,symbols,Symbol,IndexedBase
from testinfrastructure.helpers import pe
from createTables import createTables
from helpers import defaultOrderingName,addModel,resolve,symbolic_resolve,resolveMatrix,resolveVector,addIndexedVariable,addStateVariableOrdering,getStateVector,addDerivedVariable,get_name_spaces

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

        res=resolve(metadata,engine,Symbol("NetFlux"),model_id)
        ref=sympify('kIvl*vl-kOvl*vl')
        # also base variables should be resolved (just to Symbols) 
        res=resolve(metadata,engine,Symbol("Ivl"),model_id)
        ref=sympify('Ivl')
        
        #addIndexedVariable(
        #    metadata
        #    ,engine
        #    ,model_id=model_id
        #    ,symbol='Iv'
        #    ,description='carbon distribution'
        #    ,expr_str='Matrix([Ivl,Ivw,0,0,0])'
        #    ,coord_system_id=defaultOrderingName
        #)
        #addDerivedVariable(
        #     metadata
        #    ,engine
        #    ,model_id=model_id
        #    ,symbol='u'
        #    ,description='net influx to vegetation pools'
        #    ,expression='sum(Iv[0:2])'
        #    ,coord_system_id=defaultOrderingName
        #    
        #)
        #res_0=resolve(metadata,engine,Symbol('u'),model_id,defaultOrderingName)
        #pe('u',locals())

    def test_resolve_indexed_expression(self):
        # suppose v is a vector (in the physical coordinate independent sense)
        # in coord system 1 it has components [a,b,c,d]
        sl=["a","b","c","d"]
        el=['v=Matrix([a,b,c,d])']
        gns,lns = get_name_spaces(sl,el)
        # and the
        res_exp=sympify('v[1]+v[2]',locals=lns) # unfortunately sympyfy does not recognize 'sum(v[1:3])' which evaluates to the same result
        ## We confine ourselves here to what sympify can do at the moment
        #res=geometric_resolve(res_exp,sl,ed) 
        #pe('res',locals())
        ## now suppose res is coordinate invariant
        ## and we want to compute it for a representation of v in different
        ## and vp is related to v by
        #vp=Matrix([
        #    [0,0,0,1]
        #   ,[0,1,0,0]
        #   ,[0,0,1,0]
        #   ,[1,0,0,0]
        #])

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

        #
        # If we wanted to store (AND TRANSFORM) block matrices we would be 
        # compelled to store their positions inside the matrices assembled from them 
        # As mentioned before, it would be impossible to transform the constituents 
        # of the assembly to a new ordering without this information.
        # As transformable objects we therefore presently store full sized matrices only.

        # The next test demonstrates how to extract \vec{b} u and \tens{V}
        # refering to the original ordering in the database 
        #          ⎡ bl⎤
        #          ⎢ bv⎥ 
        # \vec{b} =⎢ 0 ⎥ 
        #          ⎢ 0 ⎥ 
        #          ⎣ 0 ⎦
        
        addIndexedVariable(
            metadata
            ,engine
            ,symbol='b'
            ,description='carbon distribution'
            ,model_id=model_id
            ,expression='Matrix([Ivl/NetVegIn,Ivw/NetVegIn,0,0,0])'
            ,execution_order=20
            ,coord_system_id=defaultOrderingName
        )
        res=resolve(metadata,engine,Symbol('b'),model_id)
        ref = sympify("Matrix([Ivl/(Ivl + kIvw*vw), kIvw*vw/(Ivl + kIvw*vw),0,0,0])")
        self.assertEqual(res,ref)

        # we could now retrieve the vector b resulting from another ordering of the statevariables
        my_ordering_name='veg_2'
        addStateVariableOrdering(metadata,engine,model_id,state_variable_symbols=["vw", "vl", "sf", "ss", "sb"],coord_system_id=my_ordering_name)
        res=resolveVector(metadata,engine,Symbol('b'),model_id,my_ordering_name)
        ref = sympify("Matrix([kIvw*vw/(Ivl + kIvw*vw),Ivl/(Ivl + kIvw*vw),0,0,0])")
        self.assertEqual(res,ref)
        
        # The next test demonstrates how to extract the matrix V
        # refering to the original ordering in the database 
        #                  ⎡ V_11,  V_12, 0  ,  0  ,  0  ⎤   ⎡ V_11,   0  ,  0  ,  0  ,  0  ⎤
        #                  ⎢ V_21,  V_22, 0  ,  0  ,  0  ⎥   ⎢  0  ,  V_22,  0  ,  0  ,  0  ⎥
        #              V = ⎢  0  ,   0  , 0  ,  0  ,  0  ⎥ = ⎢  0  ,   0  ,  0  ,  0  ,  0  ⎥
        #                  ⎢  0  ,   0  , 0  ,  0  ,  0  ⎥   ⎢  0  ,   0  ,  0  ,  0  ,  0  ⎥
        #                  ⎣  0  ,   0  , 0  ,  0  ,  0  ⎦   ⎣  0  ,   0  ,  0  ,  0  ,  0  ⎦
        
        addIndexedVariable(
            metadata
            ,engine
            ,symbol='V'
            ,description='an incomplete vegetation matrix'
            ,model_id=model_id
            ,expression='SparseMatrix(5,5,{(0,0):kvl})'
            ,execution_order=getHighestExecutionOrder(metadata,engine,model_id)+1
            ,coord_system_id=defaultOrderingName
        )
        res=resolve(metadata,engine,Symbol('V'),model_id)

        ref=sympify("Matrix([[kvl, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])")
        #pe("res",locals())
        self.assertEqual(res,ref)


        # Since we store derived variables as expression strings it is still possible to (maybe accidentally) use 
        # matrix and vector variables without being able to transform them to other coordinates, 
        # So we have to make sure that they are not used without the context of the ordering:
        #
        # Assume for example that "NetVegIn" had not been defined by  " NetVegIn = Ivl+Ivw "
        # but by " u= NetVegIn = sum(Iv[0:2]) " with "Iv=Matrix([Ivl,Ivw,Isf,Iss,Isb])"
        # After the above Permutation of the second and fifth line the correct way to compute u would be
        # "u = Iv[0]+Iv[5]" and the original "u = sum(Iv[0:2]) " would be wrong.
        # Although" sum(Iv[0:2]) "itself is a scalar we can not compute it for a different ordering because it DEPENDS on a vector (and so on the ordering).
        # lets test that it is reproduced accurately under a change of orderings.
        # firt define the compelet Inputvector
        addIndexedVariable(
            metadata
            ,engine
            ,model_id=model_id
            ,symbol='Iv'
            ,description='carbon distribution'
            ,expression='Matrix([Ivl,Ivw,0,0,0])'
            ,execution_order=22
            ,coord_system_id=defaultOrderingName
        )
        addDerivedVariable(
             metadata
            ,engine
            ,model_id=model_id
            ,symbol='u'
            ,description='net influx to vegetation pools'
            ,expression='sum(Iv[0:2])'
            ,execution_order=22
            ,coord_system_id=defaultOrderingName
            
        )
        addDerivedVariable(
             metadata
            ,engine
            ,model_id
            ,symbol='u_2'
            ,description='net influx to vegetation pools'
            ,expression='Iv[0]+Iv[4])'
            ,execution_order=23
            ,coord_system_id=defaultOrderingName
            
        )
        res_0=resolve(metadata,engine,Symbol('u'),model_id,defaultOrderingName)
        res_1=resolve(metadata,engine,Symbol('u_2'),model_id,my_ordering_name)
        # since u is coordinate (permutation invariant) it has to be the same in both orderings
        self.assertEqual(res_0,res_1)






