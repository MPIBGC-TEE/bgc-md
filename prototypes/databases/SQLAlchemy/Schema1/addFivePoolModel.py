from sqlalchemy import Table 
def addFivePoolModel(metadata,engine):
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
