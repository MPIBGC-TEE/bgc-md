from sqlalchemy import Table 
from helpers import addModel
def addOnePoolModel(metadata,engine,model_id,name):
    base_variables = [ 
        { 'symbol':"kO_vl"  ,'description':"decomposition rate",'dimension':"1/time"   } 
        ,{ 'symbol':"kIvl"  ,'description':"photasynthesis rate",'dimension':"1/time"   } 
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
            ,'expression':"vl*kIvl"
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
         { 'symbol':"ka"  ,'description':"decomprate"                              ,'dimension':"1/time"   }
        ,{ 'symbol':"kO_vl" ,'description':"leaf respiration rate"                   ,'dimension':"1/time"   }
        ,{ 'symbol':"ki_vw" ,'description':"wood respiration rate"                   ,'dimension':"1/time"   }
    ]
    derived_variables = [
         { 'symbol':"u_org"     ,'description':"some variable describing the comulativ vegetation input"    ,'expression':"Ivl+Ivw"}
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
            'symbol':"Ivw" 
            ,'description':"External influx into compartment vw"    
            ,'expression':"vw*ki_vw"
            ,'target_symbol':"vw"
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
            'symbol':"INTvlvw"
            ,'description':"root leaf transfer"                                         
            ,'expression':"ka*vl"  
            ,'source_symbol':"vl"
            ,'target_symbol':"vw"
        }
    ]
    
    state_variables= [ 
         { 'symbol':"vl" ,'description':"leaf pool" }
        ,{ 'symbol':"vw" ,'description':"wood pool" }
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
         { 'symbol':"klw"  ,'description':"decomprate"                              ,'dimension':"1/time"   }
        ,{ 'symbol':"kvl"   ,'description':"leaf respiration rate"                   ,'dimension':"1/time"   }
        ,{ 'symbol':"ksf"   ,'description':"fast soil respiration rate"              ,'dimension':"1/time"   }
        ,{ 'symbol':"kIvw" ,'description':"leaf respiration rate"                   ,'dimension':"1/time"   }
    ]
    derived_variables = [
         { 'symbol':"u_org"     ,'description':"some variable describing the comulativ vegetation input"    ,'expression':"Ivl+Ivw"}
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
            'symbol':"Ivw" 
            ,'description':"External influx into compartment vw"    
            ,'expression':"vw*kIvw"
            ,'target_symbol':"vw"
        }
    ]
    derived_out_fluxes=[
        {
            'symbol':"Ovl" 
            ,'description':"External Outflux out of compartment vl =leaf respiration"    
            ,'expression':"kvl*vl"
            ,'source_symbol':"vl"
        }
        ,{
            'symbol':"Osf" 
            ,'description':"External Outflux out of compartment sf =soil respiration"    
            ,'expression':"kvl*vl"
            ,'source_symbol':"vl"
        }
    ]
    derived_internalfluxes=[
        { 
            'symbol':"INTvlvw"
            ,'description':"root leaf transfer"                                         
            ,'expression':"klw*vl"  
            ,'source_symbol':"vl"
            ,'target_symbol':"vw"
        }
    ]
    
    state_variables= [ 
         { 'symbol':"vl" ,'description':"leaf pool" }
        ,{ 'symbol':"vw" ,'description':"wood pool" }
        ,{ 'symbol':"sf" ,'description':"soil pool fast" }
        ,{ 'symbol':"ss" ,'description':"soil pool slow" }
        ,{ 'symbol':"sb" ,'description':"soil pool bacteria" }
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
