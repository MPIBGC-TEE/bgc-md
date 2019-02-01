from source import special_vars
from interpolationFunctions import cable_sols_by_name

smr=special_vars['smooth_model_run']
srm=special_vars['smooth_reservoir_model']
times=smr.times
##solutions=smr.solve()
#sol_funcs=smr.sol_funcs()
state_vector=srm.state_vector
n=len(state_vector)
#sol_dict_by_smybol={state_vector[i]:sol_funcs[i] for i in range(n)}
#sol_dict_by_name={k.name:v for k,v in sol_dict_by_smybol.items()}
sol_dict_by_name=smr.sol_funcs_dict_by_name()
################################################################
import matplotlib.pyplot  as plt
fig=plt.figure(figsize=(7,n*7))
#smr.plot_solutions(fig, fontsize=10)
for i in range(n):
    sym=state_vector[i]
    name=sym.name
    ax1=fig.add_subplot(n,1,i+1)
    ax1.plot(times,cable_sols_by_name[name](times),'*',color='red',label="cable")
    ax1.plot(times,sol_dict_by_name[name](times),'-',color='blue',label="bgc_md")
    ax1.legend()
fig.savefig("pool_contents.pdf")


#fig=plt.figure(figsize=(7,7))
#test_expr_num=numerical_function_from_expression(test_expr,tup=(t,),parameter_set=par_dict,func_set=func_dict)
#
#leaf_num=sol_funcs[0]
#fine_root_num=sol_funcs[1]
#wood_num=sol_funcs[2]
#func_dict.update(
#    {
#          leaf:leaf_num
#         ,wood:wood_num
#         ,fine_root:fine_root_num
#    }
#)
#expr=srm.F
#sv_syms=[leaf,wood,fine_root,metabolic_lit,fast_soil,structural_lit]
#symToFunc={var:Function(var.name)(t) for var in sv_syms} 
#expr_symFunc=expr.subs(symToFunc)
#num_func=numerical_function_from_expression(expr_symFunc,tup=(t,),parameter_set=par_dict,func_set=func_dict)
##        ,tup=(t,),parameter_set=par_dict,func_set=func_dict)
#
#ax1=fig.add_subplot(2,1,1)
#ax1.plot(times,test_expr_num(times),color='blue')
#fig.savefig('diagnostics.pdf')
