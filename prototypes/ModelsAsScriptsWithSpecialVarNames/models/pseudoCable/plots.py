from source import special_vars
smr=special_vars['smooth_model_run']
srm=special_vars['smooth_reservoir_model']
times=smr.times
solutions=smr.solve()
#sol_funcs=smr.sol_funcs()
################################################################
import matplotlib.pyplot  as plt
fig=plt.figure(figsize=(7,50))
#smr.plot_solutions(fig, fontsize=10)
ax1=fig.add_subplot(9,1,1)
ax1.plot(times,cable_leaf(times),'*',color='red')
ax1.plot(times,solutions[:,0],'-',color='blue')
ax1.set_title("leaf")

ax2=fig.add_subplot(9,1,2)
ax2.plot(times,cable_fine_root(times),'*',color='red')
ax2.plot(times,solutions[:,1],'-',color='blue')
ax2.set_title("fine_root")

ax3=fig.add_subplot(9,1,3)
ax3.plot(times,cable_wood(times),'*',color='red')
ax3.plot(times,solutions[:,2],'-',color='blue')
#ax3.plot(times,solutions[:,2],'-',color='blue')
ax3.set_title("wood")

ax4=fig.add_subplot(9,1,4)
ax4.plot(times,cable_metabolic_lit(times),'*',color='red')
ax4.plot(times,solutions[:,3],'-',color='blue')
ax4.set_title("metabolic_lit")

ax5=fig.add_subplot(9,1,5)
ax5.plot(times,cable_structural_lit(times),'*',color='red')
ax5.plot(times,solutions[:,4],'-',color='blue')
ax5.set_title("structural_lit")

ax6=fig.add_subplot(9,1,6)
ax6.plot(times,cable_cwd(times),'*',color='red')
ax6.plot(times,solutions[:,5],'-',color='blue')
ax6.set_title("cwd")

ax7=fig.add_subplot(9,1,7)
ax7.plot(times,cable_fast_soil(times),'*',color='red')
ax7.plot(times,solutions[:,6],'-',color='blue')
ax7.set_title("fast_soil")

ax8=fig.add_subplot(9,1,8)
ax8.plot(times,cable_slow_soil(times),'*',color='red')
ax8.plot(times,solutions[:,7],'-',color='blue')
ax8.set_title("slow_soil")

ax9=fig.add_subplot(9,1,9)
ax9.plot(times,cable_passive_soil(times),'*',color='red')
ax9.plot(times,solutions[:,8],'-',color='blue')
ax9.set_title("passive_soil")
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
