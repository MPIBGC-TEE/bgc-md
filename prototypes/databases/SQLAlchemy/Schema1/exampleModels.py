from sqlalchemy import Table 
from helpers import addModel
def addOnePoolModel(metadata,engine,model_id,name):
    base_variables = [ 
        { 'symbol':"kO_vl"  ,'description':"decomposition rate",'dimension':"1/time"   } 
        ,{ 'symbol':"kI_vl"  ,'description':"photasynthesis rate",'dimension':"1/time"   } 
    ]
    derived_variables = [
         { 'symbol':"NetFlux"     ,'description':"input - output"    ,'expression':"Ivl-Ovl"}
    ]
    state_variables= [ 
         { 'symbol':"vl" ,'description':"leaf pool" }
    ]
    derived_in_fluxes=[
        {
            'symbol':"Ivl" 
            ,'description':"External influx into leaf compartment"    
            ,'expression':"vl*kI_vl"
            ,'target_symbol':"vl"
        }
    ]
    derived_out_fluxes=[
        {
            'symbol':"Ovl" 
            ,'description':"External Outflux out of compartment vl =leaf respiration"    
            ,'expression':"kO_vl*vl"
            ,'source_symbol':"vl"
        }
    ]
    addModel(
        metadata
        ,engine
        ,model_id
        ,name
        ,state_variables
        ,base_variables
        ,derived_variables
        ,[] #base_in_fluxes
        ,derived_in_fluxes
        ,derived_out_fluxes
        ,[] #derived internal fluxes
    )
def addTwoPoolModel(metadata,engine,model_id,name):
    base_variables = [
         { 'symbol':"k_a"  ,'description':"decomprate"                              ,'dimension':"1/time"   }
        ,{ 'symbol':"kO_vl" ,'description':"leaf respiration rate"                   ,'dimension':"1/time"   }
        ,{ 'symbol':"ki_v_b" ,'description':"leaf respiration rate"                   ,'dimension':"1/time"   }
    ]
    derived_variables = [
         { 'symbol':"u_org"     ,'description':"some variable describing the comulativ vegetation input"    ,'expression':"Ivl+Iv_b"}
    ]
    base_in_fluxes=[
        {
            'symbol':"Ivl" 
            ,'description':"External influx into compartment vl"    
            ,'dimension':"mass/time"# fixme: this should be derived from the target_symbol which must be a state variable
            ,'target_symbol':"vl"
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
            'symbol':"Ovl" 
            ,'description':"External Outflux out of compartment vl =leaf respiration"    
            ,'expression':"kO_vl*vl"
            ,'source_symbol':"vl"
        }
    ]
    derived_internal_fluxes=[
        { 
            'symbol':"INTvl_v_b"
            ,'description':"root leaf transfer"                                         
            ,'expression':"k_a*vl"  
            ,'source_symbol':"vl"
            ,'target_symbol':"v_b"
        }
    ]
    
    state_variables= [ 
         { 'symbol':"vl" ,'description':"leaf pool" }
        ,{ 'symbol':"v_b" ,'description':"wood pool" }
    ]
    
    addModel(
        metadata
        ,engine
        ,model_id
        ,name
        ,state_variables
        ,base_variables
        ,derived_variables
        ,base_in_fluxes
        ,derived_in_fluxes
        ,derived_out_fluxes
        ,derived_internal_fluxes
    )
    
def addFivePoolModel(metadata,engine,model_id,name):
    base_variables = [
         { 'symbol':"k_l_w"  ,'description':"decomprate"                              ,'dimension':"1/time"   }
        ,{ 'symbol':"kv_l"   ,'description':"leaf respiration rate"                   ,'dimension':"1/time"   }
        ,{ 'symbol':"ks_f"   ,'description':"fast soil respiration rate"              ,'dimension':"1/time"   }
        ,{ 'symbol':"kI_v_w" ,'description':"leaf respiration rate"                   ,'dimension':"1/time"   }
    ]
    derived_variables = [
         { 'symbol':"u_org"     ,'description':"some variable describing the comulativ vegetation input"    ,'expression':"Iv_l+Iv_w"}
    ]
    base_in_fluxes=[
        {
            'symbol':"Iv_l" 
            ,'description':"External influx into compartment v_l"    
            ,'dimension':"mass/time"# fixme: this should be derived from the target_symbol which must be a state variable
            ,'target_symbol':"v_l"
        }
    ]
    derived_in_fluxes=[
        {
            'symbol':"Iv_w" 
            ,'description':"External influx into compartment v_w"    
            ,'expression':"v_w*kI_v_w"
            ,'target_symbol':"v_w"
        }
    ]
    derived_out_fluxes=[
        {
            'symbol':"Ov_l" 
            ,'description':"External Outflux out of compartment v_l =leaf respiration"    
            ,'expression':"kv_l*v_l"
            ,'source_symbol':"v_l"
        }
        ,{
            'symbol':"Os_f" 
            ,'description':"External Outflux out of compartment s_f =soil respiration"    
            ,'expression':"kv_l*v_l"
            ,'source_symbol':"v_l"
        }
    ]
    derived_internal_fluxes=[
        { 
            'symbol':"INTv_l_v_w"
            ,'description':"root leaf transfer"                                         
            ,'expression':"k_l_w*v_l"  
            ,'source_symbol':"v_l"
            ,'target_symbol':"v_w"
        }
    ]
    
    state_variables= [ 
         { 'symbol':"v_l" ,'description':"leaf pool" }
        ,{ 'symbol':"v_w" ,'description':"wood pool" }
        ,{ 'symbol':"s_f" ,'description':"soil pool fast" }
        ,{ 'symbol':"s_s" ,'description':"soil pool slow" }
        ,{ 'symbol':"s_b" ,'description':"soil pool bacteria" }
    ]
    
    addModel(
        metadata
        ,engine
        ,model_id
        ,name
        ,state_variables
        ,base_variables
        ,derived_variables
        ,base_in_fluxes
        ,derived_in_fluxes
        ,derived_out_fluxes
        ,derived_internal_fluxes
    )
