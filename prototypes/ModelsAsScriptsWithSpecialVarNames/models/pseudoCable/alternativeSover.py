from CompartmentalSystems.helpers_reservoir import  numsol_symbolic_system
from source import special_vars
srm=special_vars['smooth_reservoir_model']
smr=special_vars['smooth_model_run']
print(srm)
#rhs=numerical_rhs2(srm.state_vector,srm.time_symbol,srm.F,smr.parameter_set,smr.func_set)
# alternative solution method:
sol2=numsol_symbolic_system(
    srm.state_vector,
    srm.time_symbol,
    srm.F,
    smr.parameter_set,
    smr.func_set,
    smr.start_values, 
    smr.times
)
