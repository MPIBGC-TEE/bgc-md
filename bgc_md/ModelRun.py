# vim:set ff=unix expandtab ts=4 sw=4:
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from sympy import diff, exp, lambdify, flatten, latex, Symbol
from scipy.integrate import odeint, quad 
from scipy.interpolate import interp1d
import numpy as np

from .SmoothModelRun import SmoothModelRun
from .helpers_reservoir import has_pw, numsol_symbolic_system

class ModelRun:
    def __init__(self, rm, parameter_set={}, start_values=None, times = None):
        self.model = rm
        self.parameter_set = parameter_set
        self.times = times
        self.start_values = start_values

        times = set(list(times) + rm.jump_times)
        times = sorted(times)

        split_data = []
        start_time = times[0]
        for end_time in rm.jump_times + [times[-1]]:
            ts = times[times.index(start_time):times.index(end_time)+1]
            
            intensity = [0]*self.nr_pools
            if start_time in rm.impulsive_fluxes.keys():
                for pool, intens in rm.impulsive_fluxes[start_time].items():
                    intensity[pool] = intens
            
            split_data.append({'times': ts, 'intensity': intensity})
            start_time = ts[-1]
            
        self.split_data = split_data
                

    @property
    def nr_pools(self):
        return(self.model.nr_pools)

    def solve(self):
        #return cached result if possible
        if hasattr(self,"_previously_computed__sol"):
            return(self._previously_computed__sol)
    
        old_values = np.array(self.start_values)
        solution = np.array([[0]*self.nr_pools])
        for data in self.split_data:
            start_values = old_values + np.array(data['intensity'], dtype='float64')
            times = data['times']

            smr = SmoothModelRun(self.model.clean_model, self.parameter_set, start_values, times)
            sol = smr.solve()
            solution = np.append(solution[:-1], sol, axis=0)
            old_values = sol[-1]
            
        self._previously_computed__sol = solution
        return solution
        
#    @property
#    def mean_transit_time(self):
#        times=self.times
#        n=self.nr_pools
#        m=self.model
#        soln=self.solve_mean_age_system()
#        sol_x=soln[:,0:n]
#        sol_funcs=self.sol_funcs()
#        tup=tuple(m.state_variables)+(m.time_symbol,)
#        l=len(times)
#        outputs=dict()
#        for key,expr in m.output_fluxes.items():
#            expr_par=expr.subs(self.parameter_set)
#            ol=lambdify(tup,expr_par,modules="numpy")
#            result=np.ndarray((l,))
#            for i in range(l):
#                args=[sol_x[i,j] for j in range(n)]+[times[i]]
#                res=ol(*args)
#                result[i]=res
#            outputs[key]=result
#        
#        transit_times=np.zeros((l,))
#        overall_output=np.zeros((l,))
#        for key,vector in outputs.items():
#            agevec=soln[:,n+key]
#            pool_age=agevec*vector
#            overall_output+=vector
#            transit_times+=pool_age
#        return(transit_times/overall_output)    
#
    def sol_funcs(self):
        sol=self.solve()
        sol_funcs=[]
        for i in range(self.nr_pools):
            sol_inter=interp1d(self.times, sol[:,i])
            sol_funcs.append(sol_inter)
        return(sol_funcs)
        
#    def f_of_t_maker(self,sol_funcs,ol):
#        def ot(t):
#            sv=[sol_funcs[i](t) for i in range(self.nr_pools)]
#            tup=tuple(sv)+(t,)
#            res=ol(*tup)
#            return(res)
#        return(ot)
#
#    def flux_funcs(self,expr_dict):
#        m=self.model
#        sol_funcs=self.sol_funcs()
#        flux_funcs={}
#        tup=tuple(m.state_variables)+(m.time_symbol,)
#        for key,value in expr_dict.items():
#            o_par=value.subs(self.parameter_set)
#            ol=lambdify(tup,o_par,modules="numpy")
#            flux_funcs[key]=self.f_of_t_maker(sol_funcs,ol)
#
#        return(flux_funcs)
#
#    
#    def external_input_flux_funcs(self):
#        return(self.flux_funcs(self.model.input_fluxes))
#
#    def internal_flux_funcs(self):
#        return(self.flux_funcs(self.model.internal_fluxes))
#
#
#    def output_flux_funcs(self):
#        return(self.flux_funcs(self.model.output_fluxes))
#    
#
    def plot_sols(self, fig, fontsize = 20):
    #fixme:
    # since time units and units are related to those
    # of the other fluxes it would be more consistent
    # to make them a property of SmoothModelRun and use
    # them in the other plots as well

        tf = self.times
        sol_funcs = self.sol_funcs()
        n=self.nr_pools
        for i in range(n):
            ax = fig.add_subplot(n,1,i+1)
            ax.plot(tf,sol_funcs[i](tf))
            
            ax.set_xlim(tf[0], tf[-1])
            ax.set_ylim(ax.get_ylim()[0]*0.9, ax.get_ylim()[1]*1.1)
        
            time_unit = self.model.time_unit
            xlabel = latex(self.model.time_symbol)
            if time_unit:
                xlabel += "\quad(" + latex(time_unit) + ")"
            ax.set_xlabel("$" + xlabel + "$", fontsize = fontsize)
            
            units = self.model.units
            ylabel = latex(self.model.state_vector[i])
            if units and units[i]:
                ylabel += "\quad(" + latex(units[i]) + ")"
            ax.set_ylabel("$" + ylabel + "$", fontsize=fontsize)

    def plot_phase_plane(self, ax, i, j, fontsize = 24):
        #fixme: exact the same code as in SmoothModelRun
        tf = self.times
        sol_funcs = self.sol_funcs()
        ax.plot(sol_funcs[i](tf), sol_funcs[j](tf))

        x0 = sol_funcs[i](tf[0])
        y0 = sol_funcs[j](tf[0])
        ax.scatter([x0],[y0], s=60)

        x1 = sol_funcs[i](tf[len(tf)//2-1])
        y1 = sol_funcs[j](tf[len(tf)//2-1])
        x2 = sol_funcs[i](tf[len(tf)//2+1])
        y2 = sol_funcs[j](tf[len(tf)//2+1])
        ax.add_patch(mpatches.FancyArrowPatch((x1,y1), (x2,y2), arrowstyle='simple', mutation_scale=20, alpha=1))

        ax.set_xlim(ax.get_xlim()[0]*0.9, ax.get_xlim()[1]*1.1)
        ax.set_ylim(ax.get_ylim()[0]*0.9, ax.get_ylim()[1]*1.1)

        units = self.model.units

        xlabel = latex(self.model.state_vector[i])
        if units and units[i]:
            xlabel += "\quad(" + units[i] + ")"
        ax.set_xlabel("$" + xlabel + "$", fontsize=fontsize)
        
        ylabel = latex(self.model.state_vector[j])
        if units and units[j]:
            ylabel += "\quad(" + units[j] + ")"
        ax.set_ylabel("$" + ylabel + "$", fontsize=fontsize)

    def plot_phase_planes(self, fig, fontsize = 20):
        #fixme: exact the same code as in SmoothModelRun
        n = len(self.model.state_vector)
        planes = [(i,j) for i in range(n) for j in range(i)]
        n = len(planes)

        if n <=3:
            rows = 1
            cols = n
        if n == 4 :
            rows = 2
            cols = 2
        if n >= 5:
            rows = n // 3
            if n % 3 != 0:
                rows += 1
            cols = 3         

        for k, (i, j) in enumerate(planes):
            ax = fig.add_subplot(rows, cols, k+1)
            self.plot_phase_plane(ax, i, j, fontsize=fontsize)
    
#    def plot_internal_fluxes(self,fig):
#        internal_flux_funcs=self.internal_flux_funcs()
#        n=len(internal_flux_funcs.keys())
#        tf=self.times
#        sol_funcs=self.sol_funcs()
#        n=self.nr_pools
#        i=1
#        for key,value in internal_flux_funcs.items():
#            p=fig.add_subplot(n,1,i)
#            p.plot(tf,internal_flux_funcs[key](tf))
#            i+=1
#
#    def plot_output_fluxes(self,fig):
#        tf=self.times
#        output_flux_funcs=self.output_flux_funcs()
#        n=len(output_flux_funcs.keys())
#        i=1
#        for key,value in output_flux_funcs.items():
#            p=fig.add_subplot(n,1,i)
#            p.plot(tf,output_flux_funcs[key](tf))
#            i+=1
#                
#    def plot_mean_ages_rasmussen(self,fig):
#        tf=self.times
#        n=self.nr_pools
#        states,rhs=self.model.mean_age_system
#        time_symbol=self.model.time_symbol
#        tf=self.times
#        soln=self.solve_mean_age_system()
#        for i in range(n):
#            ax_a = plt.subplot2grid((n,1),(i,0))
#            ax_a.plot(tf,soln[:,i+n])
#            ax_a.set_xlabel("$"+latex(time_symbol)+ "$" )
#            ax_a.set_ylabel("$"+latex(states[i+n])+ "$" )
#                
#    def plot_mean_transit_time_rasmussen(self,fig):
#        tr_val=self.mean_transit_time
#        fig=plt.figure()
#        ax_a = plt.subplot2grid((1,1),(0,0))
#        ax_a.plot(tf,tr_val[:])
#        ax_a.set_xlabel("$"+latex(time_symbol)+ "$" )
#        ax_a.set_ylabel("mean transit time " )
#
#    def plot_external_input_fluxes(self,fig):
#        tf=self.times
#        input_flux_funcs=self.external_input_flux_funcs()
#        n=len(input_flux_funcs.keys())
#        i=1
#        for key,value in input_flux_funcs.items():
#            p=fig.add_subplot(n,1,i)
#            p.plot(tf,input_flux_funcs[key](tf))
#            i+=1
                



 
 
 
 
