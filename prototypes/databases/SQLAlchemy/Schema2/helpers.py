from sqlalchemy import Table
from sqlalchemy.sql import select,and_
from sympy import Matrix,SparseMatrix,sympify,symbols,Symbol
from sympy.core.sympify import kernS
import sympy
from testinfrastructure.helpers import pe
from typing import List

#define some module wide Variables
defaultOrderingName='default_ordering' # might become a classVariable if we decide to encapsulate the database access

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
def addDerivedVariable(metadata,engine,model_id,symbol,description,expression,execution_order,coord_system_id=defaultOrderingName):
    # derived variables are variables
    addVariable(metadata,engine,model_id,symbol,description)
    
    DerivedVariables=Table("DerivedVariables",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	DerivedVariables.insert(), [ 
            { 
                'symbol':symbol
                ,'model_id':model_id
                ,'expression':expression
                ,'execution_order':execution_order
                # Derived variables potentially contain indexed expressions 
                # (even if the result is scalar). They therefore need a reference to 
                # the coordinate frame they are defined in.
                ,'coord_system_id':coord_system_id 
            } 
        ]
    )
    
def addBaseInFlux(metadata,engine,model_id,symbol,target_symbol,description,dimension):
    addBaseVariable(metadata,engine,model_id,symbol,description,dimension)
    InFluxes=Table("InFluxes",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	InFluxes.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'target_symbol':target_symbol} ]
    )

def addDerivedInFlux(metadata,engine,model_id,symbol,target_symbol,description,expression,execution_order,coord_system_id):
    addDerivedVariable(metadata,engine,model_id,symbol,description,expression,execution_order,coord_system_id)

    InFluxes=Table("InFluxes",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	InFluxes.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'target_symbol':target_symbol} ]
    )

def addDerivedOutFlux(metadata,engine,model_id,symbol,source_symbol,description,expression,execution_order,coord_system_id):
    addDerivedVariable(metadata,engine,model_id,symbol,description,expression,execution_order,coord_system_id)

    OutFluxes=Table("OutFluxes",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	OutFluxes.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'source_symbol':source_symbol} ]
    )

def addDerivedInternalFlux(metadata,engine,model_id,symbol,source_symbol,target_symbol,description,expression,execution_order,coord_system_id):
    # a flux is a variable
    addDerivedVariable(metadata,engine,model_id,symbol,description,expression,execution_order,coord_system_id)
    # with additional information
    InternalFluxes=Table("InternalFluxes",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    conn.execute(
    	InternalFluxes.insert(), [ { 'symbol':symbol, 'model_id':model_id, 'source_symbol':source_symbol, 'target_symbol':target_symbol} ]
    )

def addStateVariableOrdering(metadata,engine,model_id,state_variable_symbols,coord_system_id):
    CoordSystems=Table("CoordSystems",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    # check if ordering already exists
    s = select([CoordSystems.c.id]).where(
            and_(CoordSystems.c.model_id== model_id
                ,CoordSystems.c.id == coord_system_id))
    res=[row[0] for row in conn.execute(s)]
    #pe('len(res)',locals())
    if len(res)==0:
        conn.execute(
        	CoordSystems.insert(),
        	[
        		{'model_id':model_id,'id':coord_system_id},
        	]
        )

    # now check if statevariables already defined in default ordering
    # and if so if the new ordering defines the same set of state variables
    dsv=getStateVector(metadata,engine,model_id,coord_system_id=defaultOrderingName)
    #pe('dsv',locals())
    dsvs=set(dsv)
    if len(dsvs)!=0:
        svss=set([Symbol(s) for s in state_variable_symbols])
        if dsvs!=svss:
            raise Exception("the set of statevariables defined by the new ordering {0} differs from the set of statevariables defined by the default ordering {1}".format(dsvs,svss))
    StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
    # If an ordering of the same name has been present
    # we have to remove the entried in the StateVectorPositions table
    StateVectorPositions.delete().where(StateVectorPositions.c.model_id== model_id and StateVectorPositions.c.coord_system_id==coord_system_id)
    # and add the new entries
    for index,s in enumerate(state_variable_symbols):
        conn=engine.connect()
        conn.execute(
    	    StateVectorPositions.insert(), [
                {
                    'pos_id':index
                    ,'symbol':s
                    ,'model_id':model_id
                    ,'coord_system_id':coord_system_id
                } 
            ]
        )
    #s=select([StateVectorPositions.c.symbol,StateVectorPositions.c.coord_system_id,StateVectorPositions.c.pos_id]).where(StateVectorPositions.c.model_id==model_id)
    #for r in conn.execute(s):
    #    print(r)

def addStateVariables(metadata,engine,model_id,state_variables,coord_system_id=defaultOrderingName):
    CoordSystems=Table("CoordSystems",metadata,autoload=True,autoload_with=engine)
    conn=engine.connect()
    # check if ordering already exists
    s = select([CoordSystems.c.id]).where(CoordSystems.c.model_id== model_id)
    res=[row[0] for row in conn.execute(s)]
    #pe('len(res)',locals())
    if len(res)==0:
        conn.execute(
        	CoordSystems.insert(),
        	[
        		{'model_id':model_id,'id':coord_system_id},
        	]
        )
    StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
    for index,v in enumerate(state_variables):
        addVariable(metadata,engine,model_id,v['symbol'],v['description'])
        conn=engine.connect()
        conn.execute(
    	    StateVectorPositions.insert(), [
                {
                    'pos_id':index
                    ,'symbol':v['symbol']
                    ,'model_id':model_id
                    ,'coord_system_id':coord_system_id
                } 
            ]
        )



def addIndexedVariable(
        metadata
        ,engine
        ,symbol:str
        ,description:str
        ,model_id:str
        ,expression:str
        ,execution_order:int
        ,coord_system_id:str
    ):
    CoordSystems=Table("CoordSystems",metadata,autoload=True,autoload_with=engine)
    IndexedComponents=Table("IndexedComponents",metadata,autoload=True,autoload_with=engine)
    #Dimensions=Table("Dimensions",metadata,autoload=True,autoload_with=engine)
    
    addDerivedVariable(
            metadata
            ,engine,model_id
            ,symbol,description
            ,expression=expression
            ,execution_order=execution_order
            ,coord_system_id=coord_system_id
    )
    conn=engine.connect()
    # check if ordering already exists
    s = select([CoordSystems.c.id]).where(CoordSystems.c.model_id== model_id)
    res=[row[0] for row in conn.execute(s)]
    #pe('len(res)',locals())
    if len(res)==0:
        raise Exception("The ordering with id: {0} does not exist yet.".format(coord_system_id))
    #    conn.execute(
    #    	CoordSystems.insert(),
    #    	[
    #    		{'model_id':model_id,'id':coord_system_id},
    #    	]
    #    )
    #mat=resolve(
    #    metadata
    #    ,engine
    #    ,expr=sympify(expr_str)
    #    ,model_id=model_id
    #) 
    conn.execute(
    	IndexedComponents.insert(),
    	[
            {'symbol':symbol,'model_id':model_id,'coord_system_id':coord_system_id}
    	]
    )

def getStateVariableList(metadata ,engine ,model_id:str,coord_system_id:str=defaultOrderingName)->List[str]:
    StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
    # now query
    # we use the c collection for the columns
    s = select([StateVectorPositions.c.symbol]).where(
            and_(StateVectorPositions.c.model_id==model_id,
            StateVectorPositions.c.coord_system_id == coord_system_id)).order_by(
                    StateVectorPositions.c.pos_id)
    conn=engine.connect()
    
    #sa=select([StateVectorPositions.c.symbol,StateVectorPositions.c.coord_system_id,StateVectorPositions.c.pos_id]).where(
    #        and_(StateVectorPositions.c.model_id==model_id,
    #        StateVectorPositions.c.coord_system_id==coord_system_id)
    #        )
    #for r in conn.execute(sa):
    #    print(r)

    # remark:
    # we do not have to make sure that the list is unique because this is implied by the database scheme
    sym_list=[str(row[0]) for row in conn.execute(s)]
    return sym_list

def getStateVector( metadata ,engine ,model_id:str,coord_system_id:str=defaultOrderingName)->Matrix:
    str_list=getStateVariableList( metadata ,engine ,model_id,coord_system_id=coord_system_id)
    sym_list=[Symbol(s) for s in str_list]
    stateVector=Matrix(sym_list)
    return stateVector

def getHighestExecutionOrder(metadata ,engine ,model_id:str)->int:
    DerivedVariables= Table( 'DerivedVariables' ,metadata,autoload=True,autoload_with=engine)

    s = select([DerivedVariables.c.execution_order]).where( DerivedVariables.c.model_id==model_id)
    conn=engine.connect()
    return max([row[0] for row in conn.execute(s)])


def addModel(
        metadata
        ,engine
        ,model_id
        ,model_name
        ,state_variables
        ,base_variables=[]
        ,derived_variables=[]
        ,vector_components=[]
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
     	
    for i,v in enumerate(base_variables):
        ks=v.keys()
        if 'target_symbol' in ks and 'source_symbol' in ks:
            addBaseInternalFlux(metadata,engine,model_id,v['symbol'],v['target_symbol'],v['description'],v['dimension'])
        elif 'target_symbol' in ks and not('source_symbol' in ks):
            addBaseInFlux(metadata,engine,model_id,v['symbol'],v['target_symbol'],v['description'],v['dimension'])
        elif not('target_symbol' in ks) and 'source_symbol' in ks:
            addBaseOutFlux(metadata,engine,model_id,v['symbol'],v['target_symbol'],v['description'],v['dimension'])
        else:
            addBaseVariable(metadata,engine,model_id,v['symbol'],v['description'],v['dimension'])
    
    for i,v in enumerate(derived_variables):
        ks=v.keys()
        if 'target_symbol' in ks and 'source_symbol' in ks:
            addDerivedInternalFlux(metadata,engine,model_id,v['symbol'],v['source_symbol'],v['target_symbol'],v['description'],v['expression'],i,v['coord_system_id'])

        elif 'target_symbol' in ks and not('source_symbol' in ks):
            addDerivedInFlux(metadata,engine,model_id,v['symbol'],v['target_symbol'],v['description'],v['expression'],i,v['coord_system_id'])
        elif not('target_symbol' in ks) and 'source_symbol' in ks:
            addDerivedOutFlux(metadata,engine,model_id,v['symbol'],v['source_symbol'],v['description'],v['expression'],i,v['coord_system_id'])
        else:
            addDerivedVariable(metadata,engine,model_id,v['symbol'],v['description'],v['expression'],i,v['coord_system_id'])

def getDimension(metadata,engine,model_id:str)->int:
    svl=getStateVariableList(metadata ,engine ,model_id,defaultOrderingName)
    return(len(svl))

def getPermutation(metadata,engine,model_id:str,coord_system_id:str)->Matrix:
    orig=getStateVariableList(metadata,engine,model_id,defaultOrderingName)
    new=getStateVariableList(metadata,engine,model_id,coord_system_id)
    n=len(orig)
    perm=[orig.index(s) for s in new]
    P=SparseMatrix(n,n,{(i,v):1 for i,v in enumerate(perm)})
    return P

def resolveVector(metadata,engine,expr:sympy.Expr,model_id:str,coord_system_id:str)->Matrix:
    im=resolve(metadata,engine,expr,model_id)
    # now retrieve the original ordering and the target ordering and 
    # compute the permutation
    s=im.shape
    assert(len(s)==2) 
    assert(s[1]==1)# row vector
    P=getPermutation(metadata,engine,model_id,coord_system_id)
    return  P*im

def resolveMatrix(metadata,engine,expr:sympy.Expr,model_id:str,coord_system_id:str):
    im=resolve(metadata,engine,expr,model_id)
    #make sure that we realy deal with an n x n matrix 
    s=im.shape
    assert(len(s)==2) #matrix
    assert(s[0]==s[1])#quadratic
    
    P=getPermutation(metadata,engine,model_id,coord_system_id)
    P_inv=P.inverse_LU()
    return  P*im*P_inv

def resolve(metadata,engine,expr:sympy.Expr,model_id:str,coord_system_id:str=defaultOrderingName)->sympy.Expr:
    conn=engine.connect()
    #Variables=Table("Variables",metadata,autoload=True,autoload_with=engine)
    BaseVariables=Table("BaseVariables",metadata,autoload=True,autoload_with=engine)
    StateVectorPositions=Table("StateVectorPositions",metadata,autoload=True,autoload_with=engine)
    DerivedVariables=Table("DerivedVariables",metadata,autoload=True,autoload_with=engine)
    
    sb=select([BaseVariables.c.symbol]).where(BaseVariables.c.model_id==model_id)
    bss=[str(row[0])  for row in conn.execute(sb)]
    
    ss=select([StateVectorPositions.c.symbol]).where(StateVectorPositions.c.model_id==model_id)
    sss=[str(row[0])  for row in conn.execute(ss)]
    
    #sym_strs=['kI_vl','kO_vl']+['vl']
    ss=bss+sss
    sl=[Symbol(s) for s in ss]

    expressions={str(row[0]):str(row[1])  for row in 
            conn.execute(
                select([DerivedVariables.c.symbol,DerivedVariables.c.expression]).where(DerivedVariables.c.model_id==model_id))
    }

    #expressions={
    #        'NetFlux':'Ivl-Ovl'
    #        ,'Ivl':'kI_vl*vl'
    #        ,'Ovl':'kO_vl*vl'
    #}
            
    ed={Symbol(k):sympify(v) for k,v in expressions.items()}
    #ed={Symbol(k):kernS(v) for k,v in expressions.items()}

    res=symbolic_resolve(expr,sl,ed)
    return res
        
def symbolic_resolve(expr,sl,ed):
    # actual resolver that works with sympy Symbols and expressions 
    if isinstance(expr,Symbol):
        targetSym=expr
        if targetSym in sl:
            return targetSym 
        else:
            e=ed[targetSym]
            #pe('e.free_symbols',locals())
            return e.subs({s:symbolic_resolve(s,sl,ed) for s in e.free_symbols}) 
    else:
        e=expr
        return e.subs({s:symbolic_resolve(s,sl,ed) for s in e.free_symbols}) 


