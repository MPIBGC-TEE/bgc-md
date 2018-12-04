from sqlalchemy import Table
def addVariable(metadata,engine,model_id,symbol,description):
    Variables=Table("Variables",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	Variables.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'description':description, } ]
    )
def addBaseVariable(metadata,engine,model_id,symbol,description,dimension):
    # base variables are variables
    addVariable(metadata,engine,model_id,symbol,description)
    
    BaseVariables=Table("BaseVariables",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	BaseVariables.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'dimension':dimension, } ]
    )
def addDerivedVariable(metadata,engine,model_id,symbol,description,expression):
    # derived variables are variables
    addVariable(metadata,engine,model_id,symbol,description)
    
    DerivedVariables=Table("DerivedVariables",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	DerivedVariables.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'expression':expression, } ]
    )
    
def addBaseInFlux(metadata,engine,model_id,symbol,target_symbol,description,dimension):
    addBaseVariable(metadata,engine,model_id,symbol,description,dimension)
    InFluxes=Table("InFluxes",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	InFluxes.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'target_symbol':target_symbol} ]
    )

def addDerivedInFlux(metadata,engine,model_id,symbol,target_symbol,description,expression):
    addDerivedVariable(metadata,engine,model_id,symbol,description,expression)

    InFluxes=Table("InFluxes",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	InFluxes.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'target_symbol':target_symbol} ]
    )

def addDerivedOutFlux(metadata,engine,model_id,symbol,source_symbol,description,expression):
    addDerivedVariable(metadata,engine,model_id,symbol,description,expression)

    OutFluxes=Table("OutFluxes",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	OutFluxes.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'source_symbol':source_symbol} ]
    )

def addDerivedInternalFlux(metadata,engine,model_id,symbol,source_symbol,target_symbol,description,expression):
    # a flux is a variable
    addDerivedVariable(metadata,engine,model_id,symbol,description,expression)
    # with additional information
    InternalFluxes=Table("InternalFluxes",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	InternalFluxes.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'source_symbol':source_symbol, 'target_symbol':target_symbol} ]
    )

def addStateVariables(metadata,engine,model_id,state_variables):
    StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
    for index,v in enumerate(state_variables):
        addVariable(metadata,engine,model_id,v['symbol'],v['description'])
        conn=engine.connect()
        conn.execute(
    	    StateVectorPositions.insert(), [ {'pos_id':index,'symbol':v['symbol'],'model_id':model_id} ]
        )



def addModel(
        metadata
        ,engine
        ,model_id
        ,model_name
        ,state_variables
        ,base_variables
        ,derived_variables
        ,base_in_fluxes
        ,derived_in_fluxes
        ,derived_out_fluxes
        ,derived_internal_fluxes
    ):
    Models=Table("Models",metadata,autoload=True,autoload_with=engine)
    addStateVariables(metadata,engine,model_id,state_variables) 
    conn=engine.connect()
    conn.execute(
    	Models.insert(),
    	[
    		{'folder_name':model_id,'name':model_name},
    	]
    )
     	
    for v in base_variables:
        addBaseVariable(metadata,engine,model_id,v['symbol'],v['description'],v['dimension'])
    
    for v in base_in_fluxes:
        addBaseInFlux(metadata,engine,model_id,v['symbol'],v['target_symbol'],v['description'],v['dimension'])

    for v in derived_variables:
        addDerivedVariable(metadata,engine,model_id,v['symbol'],v['description'],v['expression'])

    for v in derived_in_fluxes:
        addDerivedInFlux(metadata,engine,model_id,v['symbol'],v['target_symbol'],v['description'],v['expression'])

    for v in derived_out_fluxes:
        addDerivedOutFlux(metadata,engine,model_id,v['symbol'],v['source_symbol'],v['description'],v['expression'])

    for v in derived_internal_fluxes:
        addDerivedInternalFlux(metadata,engine,model_id,v['symbol'],v['source_symbol'],v['target_symbol'],v['description'],v['expression'])

