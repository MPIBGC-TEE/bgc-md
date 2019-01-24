from sqlalchemy import Table, Column, Integer, String, MetaData,ForeignKey,ForeignKeyConstraint
from sqlalchemy import create_engine
def createTables():
    #engine = create_engine('sqlite:///:memory:', echo=True)
    engine = create_engine('sqlite:///:memory:')
    metadata = MetaData()
    
    # build the tables
    Models=Table('Models', metadata,
    	Column('folder_name', String(50), primary_key=True),
    	Column('name', String(100))
    )
    
    # For vector/matrix/tensor valued arguments the 
    Orderings= Table('Orderings', metadata,
         Column('model_id'   , primary_key=True)
        ,Column('id'         , String(100), primary_key=True)
    	,ForeignKeyConstraint(['model_id'], ['Models.folder_name'])
    )

    Variables= Table('Variables', metadata,
        Column('symbol', String(100), primary_key=True),
        Column('model_id', None, ForeignKey('Models.folder_name') , primary_key=True),
        Column('description', String)
    )
    
    # 1.) Derived Variables are Variables 
    #     that depend on other variables (derived or base)
    # 
    # 2.) They are branches of the expression tree
    #     (If we want to include dimensions the framework
    #     the dimensions  of these variables should 
    #     be computed not stored in the database
    #
    # 3.) Since the expressions could contain indeces like u=I[0] 
    #     even scalar variables refer to an ordering of 
    #     statevariables (other coordinates in general)
    #     so a reference to this ordering has to be stored 
    #     alongside the expression since an expression
    #     containing an indexed variable is in general only valid
    #     in the coordinate system it was defined in.
    #     The aboxe example u=I[0] for instance would have to change
    #     to u=I[4] if the position of the first (0) and fith (4)
    #     statevariables would be exchanged

    DerivedVariables= Table(
        'DerivedVariables'
        ,metadata
        ,Column('symbol')
        ,Column('model_id')
        ,Column('expression', String)
        ,Column('ordering_id', String)
    	,ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
    	,ForeignKeyConstraint(['ordering_id','model_id'], ['Orderings.id', 'Orderings.model_id'])
        # here shoulb be another constraint ensuring that a symbol that has been added to the 
        # BaseVariables can not be added here
    )
    
    # BaseVariables are Variables which could be replaced by parameters or external functions
    # They are the leafes of the expression tree 
    # We could add a dimension column that contains names like mass or length ( 
    # https://docs.sympy.org/latest/modules/physics/units/dimensions.html
    BaseVariables= Table('BaseVariables', metadata,
        Column('symbol'     )
        ,Column('model_id'   )
        ,Column('dimension', String(1000))# should be constrained to a table with valid dimensions that could be created by the sympy package
    	,ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
        # here shoulb be another constraint ensuring that a symbol that has been added to the 
        # DerivedVariables can not be added here
    )
    IndexedComponents= Table('IndexedComponents', metadata,
        Column('symbol'     ,               primary_key=True) #refers to the whole matrix
        ,Column('model_id'  ,                primary_key=True )
        ,Column('ordering_id', String(1000), primary_key=True)
    	,ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
    	,ForeignKeyConstraint(['model_id','ordering_id'], ['Orderings.model_id', 'Orderings.id'])
        # here should be another constraint ensuring that there are indeed rows in the StateVectorPositions Table
        # for the specified id and every state variable (a complete permuation) 
    )
    
    StateVectorPositions= Table('StateVectorPositions', metadata,
    	Column('pos_id'         , Integer )
    	,Column('symbol'        , primary_key=True)
    	,Column('model_id'      , primary_key=True)
    	,Column('ordering_id'   , primary_key=True)
    	,ForeignKeyConstraint(['symbol', 'model_id'], ['Variables.symbol', 'Variables.model_id'])
    	,ForeignKeyConstraint([ 'model_id','ordering_id'], ['Orderings.model_id', 'Orderings.id'])
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
