from sympy import Symbol,Number
from sympy.vector import CoordSysND,express,Vector,Dyadic
from typing import List,Dict
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun
#from CompartmentalSystems import smooth_reservoir_model 
from testinfrastructure.helpers import pe
from ..Classes import MVar,Computer

# first define some functions
def make_model_run_dict(
    srm:SmoothReservoirModel
    ,par_dict_dict
    ,start_vec_dict
    ,time_vec_dict
    ,func_dict_dict)->Dict:
    return {"fake":"fake"}


smr=Computer(
     func=SmoothModelRun
    ,args=[
         MVar(name='smooth_reservoir_model') 
        ,MVar(name='parameter_dictionary') 
        ,MVar(name='start_vector') 
        ,MVar(name='time_vector') 
        ,MVar(name='function_dictionary') 
     ]
    ,description="""Creates a single instance of a SmoothModelRun"""
)
