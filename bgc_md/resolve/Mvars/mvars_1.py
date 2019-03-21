from ..Classes import MVar
from ..Computers.srm_1 import srm_bu_tens
from ..Computers.smr_1 import smr
smooth_reservoir_model=MVar(
         name='smooth_reservoir_model'
        ,computers=[srm_bu_tens]
        ,description='A smooth reservroir Model'
)

smooth_model_run_dictionary=MVar(
        'smooth_model_run_dictionary'
        ,computers=[]
        ,description= """The dictionary values are SmoothModelRun objects. The keys can be used
        in user code to refer to special simulations. """
)
        
smooth_model_run=MVar(
        'smooth_model_run_dictionary'
        ,computers=[smr]
        ,description= """A single simulation"""
)
        
