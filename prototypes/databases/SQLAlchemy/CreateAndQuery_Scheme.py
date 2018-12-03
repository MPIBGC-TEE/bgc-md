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
def createTables():
    engine = create_engine('sqlite:///:memory:', echo=True)
    metadata = MetaData()
    
    # build the tables
    Models=Table('Models', metadata,
    	Column('folder_name', String(50), primary_key=True),
    	Column('name', String(100))
    )
    
    Variables= Table('Variables', metadata,
        Column('symbol', String(100), primary_key=True),
        Column('model_id', None, ForeignKey('Models.folder_name') , primary_key=True),
        Column('description', String)
    )
    
    # Derived Variables are Variables that depend on other variables (derived or base)
    # They are branches of the expression tree
    # (If we want to include dimensions the framework
    # the dimensions  of these variables should be computed not stored in the database
    DerivedVariables= Table('DerivedVariables', metadata,
        Column('symbol'     ),
        Column('model_id'   ),
        Column('expression', String),
    	ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        # here shoulb be another constraint ensuring that a symbol that has been added to the 
        # BaseVariables can not be added here
    )
    
    # BaseVariables are Variables which could be replaced by parameters or external functions
    # They are the leafes of the expression tree 
    # We could add a dimension column that contains names like mass or length ( 
    # https://docs.sympy.org/latest/modules/physics/units/dimensions.html
    BaseVariables= Table('BaseVariables', metadata,
        Column('symbol'     ),
        Column('model_id'   ),
        #Column('dimension', String(1000)),# should be constrained to a table with valid dimensions that could be created by the sympy package
    	ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        # here shoulb be another constraint ensuring that a symbol that has been added to the 
        # DerivedVariables can not be added here
    )
    
    StateVectorPositions= Table('StateVectorPositions', metadata,
    	Column('pos_id', Integer ),
    	Column('symbol'          ),
    	Column('model_id'        ),
    	ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
    )
    
    #Fluxes are just variables 
    #InFluxes are variables connected to a target pool
    InFluxes= Table('InFluxes', metadata,
        Column('symbol'        )
        ,Column('model_id'     )
    	,Column('target_symbol')
    	,ForeignKeyConstraint(['target_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
    	,ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
    )
    
    #InFluxes are variables connected to a source pool
    OutFluxes= Table('OutFluxes', metadata,
         Column('symbol'       )
        ,Column('model_id'     )
    	,Column('source_symbol')
    	,ForeignKeyConstraint(['source_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
    	,ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
    )
    #InternalFluxes are variables( identified by (symbol,model_id) ) connected to a combination of source and target pool
    InternalFluxes= Table('InternalFluxes', metadata,
         Column('symbol'       )
        ,Column('model_id'     )
    	,Column('source_symbol')
    	,Column('target_symbol')
    	,ForeignKeyConstraint(['source_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
    	,ForeignKeyConstraint(['target_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
    	,ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
    )
    
    metadata.create_all(engine)
    return metadata,engine
def add_fivePoolModel(metadata,engine):
    #metadata,engine=createTables()
    Models=Table("Models",metadata,autoload=True,autoload_with=engine)
    Variables=Table("Variables",metadata,autoload=True,autoload_with=engine)
    StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
    BaseVariables=Table("BaseVariables",metadata,autoload=True,autoload_with=engine)
    DerivedVariables=Table("DerivedVariables",metadata,autoload=True,autoload_with=engine)
    InFluxes=Table("InFluxes",metadata,autoload=True,autoload_with=engine)
    OutFluxes=Table("OutFluxes",metadata,autoload=True,autoload_with=engine)
    InternalFluxes=Table("InternalFluxes",metadata,autoload=True,autoload_with=engine)
    ## insert data
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
            {'symbol':"v_a",    'model_id':"default_1.yaml",    'description':"vegetation carbon stock a" }
            ,{'symbol':"v_b",    'model_id':"default_1.yaml",    'description':"vegetation carbon stock b" }
            ,{'symbol':"s_a",    'model_id':"default_1.yaml",    'description':"soil carbon stock a"       }
            ,{'symbol':"s_b",    'model_id':"default_1.yaml",    'description':"soil carbon stock b"       }
            ,{'symbol':"s_c",    'model_id':"default_1.yaml",    'description':"soil carbon stock c"       }
                                                            
            ,{'symbol':"k_a" ,    'model_id':"default_1.yaml",    'description':"decomprate"                    }
            ,{'symbol':"kv_a",    'model_id':"default_1.yaml",    'description':"respiration rate"              }
            ,{'symbol':"ks_a",    'model_id':"default_1.yaml",    'description':"s_a decomprate "               }
            ,{'symbol':"Ov_a",    'model_id':"default_1.yaml",    'description':"respiration Flux from pool v_a"}
            ,{'symbol':"Os_a",    'model_id':"default_1.yaml",    'description':"respiration Flux from poos s_a"}
            ,{
                'symbol':"u_org",
                'model_id':"default_1.yaml",
                'description':"some variable describing the comulativ vegetation input"  ,
            }
            ,{
                'symbol':"Is_a",
                'model_id':"default_1.yaml",
                'description':"External influx into soil compartment a"  ,
            }
            ,{
                'symbol':"INTv_a_v_b",
                'model_id':"default_1.yaml",
                'description':"Something different from 'Internal Flux from vegetation pool v_a to v_b' because this information is allready available"  ,
            }
    	]
    )
    conn.execute(
    	DerivedVariables.insert(),
    	[
            {
                'symbol':"u_org",
                'model_id':"default_1.yaml",
                'expression':"Iv_a+Iv_b",
            }
            ,{
                'symbol':"Is_a",
                'model_id':"default_1.yaml",
                'expression':"ks_a*s_a",
            }
            ,{
                'symbol':"Os_a",
                'model_id':"default_1.yaml",
                'expression':"ks_a*s_a",
            }
            ,{
                'symbol':"Ov_a",
                'model_id':"default_1.yaml",
                'expression':"kv_a*v_a",
            }
            ,{
                'symbol':"INTv_a_v_b",
                'model_id':"default_1.yaml",
                'expression':"k_a*v_a",
            }
    	]
    )
    conn.execute(
    	BaseVariables.insert(),
    	[
            {
                'symbol':"k_a" ,'model_id':"default_1.yaml"    #,'dimension':"1/time"           
            }
            ,{
                'symbol':"Iv_a" ,'model_id':"default_1.yaml"   #,'dimension':"mass/time"           
            }
            ,{
                'symbol':"Iv_b" ,'model_id':"default_1.yaml"   #,'dimension':"mass/time"           
            }
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
            {'symbol':"Iv_a" ,'model_id':"default_1.yaml",'target_symbol':"v_a"},
            {'symbol':"Iv_b" ,'model_id':"default_1.yaml",'target_symbol':"v_b"},
            {'symbol':"Is_a" ,'model_id':"default_1.yaml",'target_symbol':"v_b"},
    	]
    )
    conn.execute(
    	OutFluxes.insert(),
    	[
             {'symbol':"Ov_a" ,'model_id':"default_1.yaml",'source_symbol':"v_a"}
            ,{'symbol':"Os_a" ,'model_id':"default_1.yaml",'source_symbol':"s_a"}
    	]
    )
    conn.execute(
    	InternalFluxes.insert(),
    	[
            { 'symbol':"INTv_a_v_b", 'model_id':"default_1.yaml",'source_symbol':"v_a",'target_symbol':"v_b"},
    	]
    )

class TestStructureOfCompartmentalMatrix(unittest.TestCase):
    # The aim is a proof of concept implementation for the retrieval of the structure of the different ways to structure the 
    # compartmental Matrix
    # Conceptually we want to separate this information from the database, which should only hold
    # the Variables and the statevectorpositions which together already determine the matrices
    def setUp(self):
        #engine = create_engine('sqlite:///:memory:', echo=True)
        #metadata = MetaData()

        self.metadata,self.engine=createTables()

        ## build the tables
        #Models=Table('Models', metadata,
        #	Column('folder_name', String(50), primary_key=True),
        #	Column('name', String(100))
        #)

        #Variables= Table('Variables', metadata,
        #    Column('symbol', String(100), primary_key=True),
        #    Column('model_id', None, ForeignKey('Models.folder_name') , primary_key=True),
        #    Column('description', String)
        #)
        #
        ## Derived Variables are Variables that depend on other variables (derived or base)
        ## They are branches of the expression tree
        ## (If we want to include dimensions the framework
        ## the dimensions  of these variables should be computed not stored in the database
        #DerivedVariables= Table('DerivedVariables', metadata,
        #    Column('symbol'     ),
        #    Column('model_id'   ),
        #    Column('expression', String),
        #	ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        #    # here shoulb be another constraint ensuring that a symbol that has been added to the 
        #    # BaseVariables can not be added here
        #)
        #
        ## BaseVariables are Variables which could be replaced by parameters or external functions
        ## They are the leafes of the expression tree 
        ## We could add a dimension column that contains names like mass or length ( 
        ## https://docs.sympy.org/latest/modules/physics/units/dimensions.html
        #BaseVariables= Table('BaseVariables', metadata,
        #    Column('symbol'     ),
        #    Column('model_id'   ),
        #    #Column('dimension', String(1000)),# should be constrained to a table with valid dimensions that could be created by the sympy package
        #	ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        #    # here shoulb be another constraint ensuring that a symbol that has been added to the 
        #    # DerivedVariables can not be added here
        #)

        #StateVectorPositions= Table('StateVectorPositions', metadata,
        #	Column('pos_id', Integer ),
        #	Column('symbol'          ),
        #	Column('model_id'        ),
        #	ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        #)
        #
        ##Fluxes are just variables 
        ##InFluxes are variables connected to a target pool
        #InFluxes= Table('InFluxes', metadata,
        #    Column('symbol'        )
        #    ,Column('model_id'     )
        #	,Column('target_symbol')
        #	,ForeignKeyConstraint(['target_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
        #	,ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        #)

        ##InFluxes are variables connected to a source pool
        #OutFluxes= Table('OutFluxes', metadata,
        #     Column('symbol'       )
        #    ,Column('model_id'     )
        #	,Column('source_symbol')
        #	,ForeignKeyConstraint(['source_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
        #	,ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        #)
        ##InternalFluxes are variables( identified by (symbol,model_id) ) connected to a combination of source and target pool
        #InternalFluxes= Table('InternalFluxes', metadata,
        #     Column('symbol'       )
        #    ,Column('model_id'     )
        #	,Column('source_symbol')
        #	,Column('target_symbol')
        #	,ForeignKeyConstraint(['source_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
        #	,ForeignKeyConstraint(['target_symbol', 'model_id'], ['StateVectorPositions.symbol', 'StateVectorPositions.model_id'])
        #	,ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        #)
        #
        #metadata.create_all(engine)
        #
        ### insert data
        #conn=engine.connect()
        #
        #conn.execute(
        #	Models.insert(),
        #	[
        #		{'folder_name':"default_1.yaml",'name':"Ceballos_eco"},
        #		{'folder_name':"default_2.yaml",'name':"Ceballos"},
        #	]
        #)
        #	
        #conn.execute(
        #	Variables.insert(),
        #	[
        #        {'symbol':"v_a",    'model_id':"default_1.yaml",    'description':"vegetation carbon stock a" }
        #        ,{'symbol':"v_b",    'model_id':"default_1.yaml",    'description':"vegetation carbon stock b" }
        #        ,{'symbol':"s_a",    'model_id':"default_1.yaml",    'description':"soil carbon stock a"       }
        #        ,{'symbol':"s_b",    'model_id':"default_1.yaml",    'description':"soil carbon stock b"       }
        #        ,{'symbol':"s_c",    'model_id':"default_1.yaml",    'description':"soil carbon stock c"       }
        #                                                        
        #        ,{'symbol':"k_a" ,    'model_id':"default_1.yaml",    'description':"decomprate"                    }
        #        ,{'symbol':"kv_a",    'model_id':"default_1.yaml",    'description':"respiration rate"              }
        #        ,{'symbol':"ks_a",    'model_id':"default_1.yaml",    'description':"s_a decomprate "               }
        #        ,{'symbol':"Ov_a",    'model_id':"default_1.yaml",    'description':"respiration Flux from pool v_a"}
        #        ,{'symbol':"Os_a",    'model_id':"default_1.yaml",    'description':"respiration Flux from poos s_a"}
        #        ,{
        #            'symbol':"u_org",
        #            'model_id':"default_1.yaml",
        #            'description':"some variable describing the comulativ vegetation input"  ,
        #        }
        #        ,{
        #            'symbol':"Is_a",
        #            'model_id':"default_1.yaml",
        #            'description':"External influx into soil compartment a"  ,
        #        }
        #        ,{
        #            'symbol':"INTv_a_v_b",
        #            'model_id':"default_1.yaml",
        #            'description':"Something different from 'Internal Flux from vegetation pool v_a to v_b' because this information is allready available"  ,
        #        }
        #	]
        #)
        #conn.execute(
        #	DerivedVariables.insert(),
        #	[
        #        {
        #            'symbol':"u_org",
        #            'model_id':"default_1.yaml",
        #            'expression':"Iv_a+Iv_b",
        #        }
        #        ,{
        #            'symbol':"Is_a",
        #            'model_id':"default_1.yaml",
        #            'expression':"ks_a*s_a",
        #        }
        #        ,{
        #            'symbol':"Os_a",
        #            'model_id':"default_1.yaml",
        #            'expression':"ks_a*s_a",
        #        }
        #        ,{
        #            'symbol':"Ov_a",
        #            'model_id':"default_1.yaml",
        #            'expression':"kv_a*v_a",
        #        }
        #        ,{
        #            'symbol':"INTv_a_v_b",
        #            'model_id':"default_1.yaml",
        #            'expression':"k_a*v_a",
        #        }
        #	]
        #)
        #conn.execute(
        #	BaseVariables.insert(),
        #	[
        #        {
        #            'symbol':"k_a" ,'model_id':"default_1.yaml"    #,'dimension':"1/time"           
        #        }
        #        ,{
        #            'symbol':"Iv_a" ,'model_id':"default_1.yaml"   #,'dimension':"mass/time"           
        #        }
        #        ,{
        #            'symbol':"Iv_b" ,'model_id':"default_1.yaml"   #,'dimension':"mass/time"           
        #        }
        #	]
        #)
        #conn.execute(
        #	StateVectorPositions.insert(),
        #	[
        #        {'pos_id':0,'symbol':"v_a",'model_id':"default_1.yaml"},
        #        {'pos_id':1,'symbol':"v_b",'model_id':"default_1.yaml"},
        #        {'pos_id':2,'symbol':"s_a",'model_id':"default_1.yaml"},
        #        {'pos_id':3,'symbol':"s_b",'model_id':"default_1.yaml"},
        #        {'pos_id':4,'symbol':"s_c",'model_id':"default_1.yaml"}
        #	]
        #)
        #conn.execute(
        #	InFluxes.insert(),
        #	[
        #        {'symbol':"Iv_a" ,'model_id':"default_1.yaml",'target_symbol':"v_a"},
        #        {'symbol':"Iv_b" ,'model_id':"default_1.yaml",'target_symbol':"v_b"},
        #        {'symbol':"Is_a" ,'model_id':"default_1.yaml",'target_symbol':"v_b"},
        #	]
        #)
        #conn.execute(
        #	OutFluxes.insert(),
        #	[
        #         {'symbol':"Ov_a" ,'model_id':"default_1.yaml",'source_symbol':"v_a"}
        #        ,{'symbol':"Os_a" ,'model_id':"default_1.yaml",'source_symbol':"s_a"}
        #	]
        #)
        #conn.execute(
        #	InternalFluxes.insert(),
        #	[
        #        { 'symbol':"INTv_a_v_b", 'model_id':"default_1.yaml",'source_symbol':"v_a",'target_symbol':"v_b"},
        #	]
        #)
        #self.conn                   =  conn
        #self.metadata               =  metadata
        #self.engine                 =  engine
        #self.StateVectorPositions   =  StateVectorPositions
        #self.BaseVariables          =  BaseVariables
        #self.Models                 =  Models
        #self.InFluxes               =  InFluxes
        #self.OutFluxes              =  OutFluxes
        #self.InternalFluxes         =  InternalFluxes

    def test_StateVector(self):
        # now query
        # we use the c collection for the columns
        metadata=self.metadata
        engine=self.engine
        conn=engine.connect()
        add_fivePoolModel(metadata,engine)
        Models=Table("Models",metadata,autoload=True,autoload_with=engine)
        Variables=Table("Variables",metadata,autoload=True,autoload_with=engine)
        StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
        BaseVariables=Table("BaseVariables",metadata,autoload=True,autoload_with=engine)
        DerivedVariables=Table("DerivedVariables",metadata,autoload=True,autoload_with=engine)
        InFluxes=Table("InFluxes",metadata,autoload=True,autoload_with=engine)
        OutFluxes=Table("OutFluxes",metadata,autoload=True,autoload_with=engine)
        InternalFluxes=Table("InternalFluxes",metadata,autoload=True,autoload_with=engine)
        s = select([StateVectorPositions.c.symbol]).where(StateVectorPositions.c.model_id== 'default_1.yaml').order_by(StateVectorPositions.c.pos_id)
        sym_list=[Symbol(str(row[0])) for row in conn.execute(s)]
        pe('sym_list',locals())
        stateVector=Matrix(sym_list)

        v_a, v_b, s_a, s_b, s_c = symbols('v_a,v_b,s_a,s_b,s_c')

        ref=Matrix([v_a, v_b, s_a, s_b, s_c])
        self.assertEqual(stateVector,ref)

    def test_Fluxes(self):
        # prove that we can reconstruct the fluxes as functions of the BaseVariables
        pass
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






