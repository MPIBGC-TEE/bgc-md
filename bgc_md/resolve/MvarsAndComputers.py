from sympy import Symbol,Number
from typing import List
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun
#from CompartmentalSystems import smooth_reservoir_model 
from testinfrastructure.helpers import pe
from .Classes import MVar,Computer
from .functions import srm_from_B_u_tens

########## README ###################
# This module defines MVar and Computer instances simultaniously since they 
# refer to each other recursively.
# In this way it (implicitly) defines a kind of convex hull or a closure 
# which has the consequence that 
# the smallest possible consistent change might NOT be a single 'Computer' or a 
# single 'MVar'.
# In particular you can NOT add a new Computer to a Mvar's computers set
# before defining the Computer instance. 
# This in turn might require you to define new
# Mvars (since they appear as the computers arguments). 
# For these you can first rely on the empty Computers list so that there is no
# infinite regress.  

# fixme?:
# Since this module is regular python code even the order in which variables
# are defined is not arbitrary. This might become troublesome. Maybe we need
# a more 'lazy' approach than a module containing variables that have to be
# defined in order.
#   a)  One possibility is to define the Mvars first and then 
#       'register' the computers later. One consequence is that the Mvars 
#       can not be immutable in this approach 
#       which does not allow caching by functools
# 
#   b)  Another possibility is to define both the 'args; of the 
#       Computer instance and the 'computers' in a MVar instance
#       not as objects but as strings interpreted with respect to a
#       dictionary of Mvars or Computers respectively and resolve
#       the relationship at runtime. This allows any kind of cross 
#       referencing even if the variables or computers do not 
#       exist yet or not at all. The latter possibility must be excluded
#       by a consistence check



# fixme?:
# possible convention:
# for Mvars that have a very specific class (like SmoothModelRun ) we could 
# call the MVar like the class? The computers act then like constructors of 
# this class.
# This raises the question if we make subclasses for all
# MVars (and find the appropriate Computers by their signature) 

coord_sys           = MVar(name='coord_sys') 
state_vector        = MVar(name='state_vector') 
time_symbol         = MVar(name='time_symbol') 
compartmental_dyad  = MVar(name='compartmental_dyad') 
input_vector        = MVar(name='input_vector') 
parameter_dictionary= MVar(name='parameter_dictionary') 
start_vector        = MVar(name='start_vector') 
time_vector         = MVar(name='time_vector') 
function_dictionary = MVar(name='function_dictionary')



srm_bu_tens=Computer(
    func=srm_from_B_u_tens
    ,args=[
         coord_sys 
        ,state_vector 
        ,time_symbol 
        ,compartmental_dyad 
        ,input_vector 
     ]
    ,description="""Produces a smoth reservoir model"""

)
smooth_reservoir_model=MVar(
         name='smooth_reservoir_model'
        ,computers=[srm_bu_tens]
        ,description='A smooth reservroir Model'
)
smr=Computer(
     func=SmoothModelRun
    ,args=[
         smooth_reservoir_model
        ,parameter_dictionary
        ,start_vector
        ,time_vector
        ,function_dictionary
     ]
    ,description="""Creates a single instance of a SmoothModelRun"""
)


smooth_model_run_dictionary=MVar(
        'smooth_model_run_dictionary'
        ,computers=[] # at the moment empty list, consequently 
        # only available when explicitly defined. 
        # Although automatic computation would be simple 
        # the keys make most sense if defined by the user

        ,description= """
        The dictionary values are SmoothModelRun objects. 
        The keys can be used in user code to refer to special 
        simulations. """
)
        
smooth_model_run=MVar(
        'smooth_model_run'
        ,computers=[smr]
        ,description= """A single simulation"""
)



