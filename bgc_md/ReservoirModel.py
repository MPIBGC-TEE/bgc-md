# vim: set expandtab ts=4

from sympy import zeros, lambdify, Matrix, simplify, diag, eye, gcd, latex, DiracDelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

from .SmoothReservoirModel import SmoothReservoirModel
from .helpers import py2tex_silent 
from .helpers_reservoir import factor_out_from_matrix, has_pw, parse_input_function

class ReservoirModel:
    def __init__(self, state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes, units=None, time_unit=None):

        self.state_vector = state_vector
        self.state_variables = [sv.name for sv in state_vector]
        self.time_symbol = time_symbol
        #self.output_fluxes = output_fluxes
        #self.internal_fluxes = internal_fluxes
        self.units = units
        self.time_unit = time_unit
 
        #self.input_fluxes = input_fluxes
        
        clean_input_fluxes = {}
        impulsive_input_fluxes = {}
        jump_times = []

        impulsive_fluxes = {}

        for (input_pool, flux) in input_fluxes.items():
            impulses, jumps = parse_input_function(flux, time_symbol)
            jump_times += jumps

            clean_flux = flux
            for impulse in impulses:
                impulse_time = impulse['time']
                intensity = impulse['intensity']
                clean_flux -= intensity * DiracDelta(-time_symbol+impulse_time)

                if not impulse_time in impulsive_fluxes.keys():
                    impulsive_fluxes[impulse_time] = {}

                impulsive_fluxes[impulse_time][input_pool] = intensity

            clean_input_fluxes[input_pool] = clean_flux

        self.clean_model = SmoothReservoirModel(state_vector, time_symbol, clean_input_fluxes, output_fluxes,
                            internal_fluxes, units, time_unit)
        self.jump_times = sorted(set(jump_times))
        self.impulsive_fluxes = impulsive_fluxes


        

        # if piecewise, otherwise just one interval
        # initialize list of smooth reservoir models


    # alternative constructor based on the formulation x = U + integral(Ax)
#    @classmethod
#    def from_A_U(cls,x,time_symbol,A,U=None,units=None,time_unit=None):
#        if not(U):
#           # fixme mm:
#           # make sure that ReservoirModels standard constructor can handle an 
#           # empty dict and produce the empty matrix only if necessary later
#           u=zeros(x.rows,1)
#        
#        # convert inputs
#        inputs = dict()
#        for pool in range(u.rows):
#            inp = U[pool]
#            if inp:
#                inputs[pool] = inp
#    
#        outputs = dict()
#        internal_fluxes = dict()
#        # calculate outputs
#        for pool in range(x.rows):
#            outp = -sum(A[:, pool]) * x[pool]
#            outp = simplify(outp)
#            if outp:
#                outputs[pool] = outp
#        
#        # calculate internal fluxes
#        pipes = [(i,j) for i in range(x.rows) for j in range(x.rows) if i != j]
#        for pool_from, pool_to in pipes:
#            flux = A[pool_to, pool_from] * x[pool_from]
#            flux = simplify(flux)
#            if flux:
#                internal_fluxes[(pool_from, pool_to)] = flux
#        # call the standard constructor 
#        o=cls(list(x),time_symbol,inputs, outputs, internal_fluxes,units,time_unit)
#        return(o)

#    @property
#    def F(self):
#        v = self.u+self.u_int-self.o_int-self.o
#        for i in range(len(v)):
#            v[i] = simplify(v[i])
#        return v
#    
#
    @property
    def external_inputs(self):
        '''return the vector of external inputs'''
        u=zeros(self.nr_pools,1)
        for k,val in self.input_fluxes.items():
            u[k]=val
        return(u)
    

#    @property
#    def external_outputs(self):
#        '''return the vector of external outputs '''
#        o=zeros(self.nr_pools,1)
#        for k,val in self.output_fluxes.items():
#            o[k]=val
#        return(o)
#        
#
#    @property
#    def internal_inputs(self):
#        '''return the vector of internal inputs'''
#        n=self.nr_pools
#        u_int=zeros(n,1)
#        for ln in range(n):     
#            # find all entries in the fluxes dict that have the target key==ln
#            expr=0
#            for k,val in self.internal_fluxes.items():
#                if k[1]==ln: #the second part of the tupel is the recipient
#                    expr+=val
#            u_int[ln]=expr
#        return(u_int)
#    
#
#    @property
#    def internal_outputs(self):
#        '''return the vector of internal outputs'''
#        n=self.nr_pools
#        o_int=zeros(n,1)
#        for ln in range(n):     
#            # find all entries in the fluxes dict that have the target key==ln
#            expr=0
#            for k,val in self.internal_fluxes.items():
#                if k[0]==ln:# the first part of the tupel is the donator
#                    expr+=val
#            o_int[ln]=expr
#        return(o_int)
#
#
    @property
    def nr_pools(self):
        return(len(self.state_variables))
#
#
#    def internal_flux_type(self, pool_from, pool_to):
#        # return 'linear', 'nonlinear', 'no substrate dependence'
#
#        sv = self.state_vector[pool_from]
#        flux = self.internal_fluxes[(pool_from, pool_to)]
#
#        if has_pw(flux):
#            print("Piecewise")    
#            print(latex(flux))
#            return "nonlinear"
#            
#        if gcd(sv, flux) == 1:
#            return 'no substrate dependence'
#
#        # now test for dependence on further state variables, which would lead to nonlinearity
#        if (gcd(sv, flux) == sv) or gcd(sv, flux) == 1.0*sv:
#            flux /= sv
#            free_symbols = flux.free_symbols
#
#            for sv in list(self.state_vector):
#                if sv in free_symbols:
#                    return 'nonlinear'
#
#            return 'linear'
#        else:
#            # probably this can never happen
#            raise(Exception('Unknown internal flux type'))
#
#
#    def output_flux_type(self, pool_from):
#        # return 'linear', 'nonlinear', 'no substrate dependence'
#
#        sv = self.state_vector[pool_from]
#        flux = self.output_fluxes[pool_from]
#        if gcd(sv, flux) == 1:
#            return 'no substrate dependence'
#
#        # now test for dependence on further state variables, which would lead to nonlinearity
#        if (gcd(sv, flux) == sv) or gcd(sv, flux) == 1.0*sv:
#            flux /= sv
#            free_symbols = flux.free_symbols
#
#            for sv in list(self.state_vector):
#                if sv in free_symbols:
#                    return 'nonlinear'
#
#            return 'linear'
#        else:
#            # probably this can never happen
#            raise(Exception('Unknown internal flux type'))
#
#
#
#    @property
#    def xi_T_N_u_representation(self):
#        nr_pools = self.nr_pools
#        inputs = self.input_fluxes
#        outputs = self.output_fluxes
#        internal_fluxes = self.internal_fluxes
#
#        # create state_vector
#        C = Matrix(self.state_variables)
#
#        # convert inputs
#        u = self.u
#
#        # calculate decomposition operators
#        decomp_rates = []
#        for pool in range(nr_pools):
#            if pool in outputs.keys():
#                decomp_flux = outputs[pool]
#            else:
#                decomp_flux = 0
#
#            decomp_flux += sum([flux for (i,j), flux in internal_fluxes.items() if i == pool])
#            decomp_rates.append(simplify(decomp_flux/C[pool]))
#
#        N = diag(*decomp_rates)
#
#        # calculate transition operator
#        T = -eye(nr_pools)
#        
#        for (i,j), flux in internal_fluxes.items():
#            T[j,i] = flux/C[i]/N[i,i]
#
#        # try to extract xi from N and T
#        xi_N = factor_out_from_matrix(N)
#        N = N/xi_N
#
#        xi_T = factor_out_from_matrix(T)
#        T = T/xi_T
#
#        xi = xi_N * xi_T
#
#        return (u, xi, T, N, C)
#
#    @property
#    def compartmental_matrix(self):
#        # could be computed directly from Jaques
#        # but since we need the xi*T*N decomposition anyway
#        # we can use it
#        xi,T,N,C,u=self.xi_T_N_u_representation
#        return(xi*T*N)
#    
#    @property
#    def mean_age_system(self):
#        # we construct the nonlinear system for the combined solution
#        # of the contents and the mean ages according to Rasmussen2016
#        u=self.u
#        S = u #nomenclature of Rasmussen paper
#        X=Matrix(self.state_variables)
#        B=self.compartmental_matrix
#
#        n=len(X)
#        ab=Matrix([var(str(x)+"_meanage") for x in X]) 
#        pretty_print(ab)
#        #g=Matrix([
#        i=1
#        g=[1+(sum([(ab[j]-ab[i])*B[i,j]*X[j] for j in range(n)])-ab[i]*S[i])/X[i] for i in range(n)]
#        #build the new statevector
#        extendet_state=Matrix(list(X)+list(ab))
#        extendet_rhs=Matrix(list(self.F)+g)
#        return(extendet_state,extendet_rhs)
#
#    def figure(self, figure_size = (7,7), logo = False, thumbnail = False):
#        inputs = self.input_fluxes
#        outputs =  self.output_fluxes
#        internal_fluxes = self.internal_fluxes
#
#
#        pool_alpha = 0.3
#        pool_color = 'blue'
#        pipe_colors = {'linear': 'blue', 'nonlinear': 'green', 'no substrate dependence': 'red'}
#        pipe_alpha=0.5
#
#        mutation_scale = 50
#        #mutation_scale=20
#        arrowstyle = "simple"
#        fontsize = 24
#        legend = True
#        if thumbnail:
#            mutation_scale = 10
#            legend = False
#            arrowstyle = "-"
#            figure_size = (0.7,0.7)    
#
#        if logo:
#            mutation_scale = 15
#            legend = False
#            fontsize = 16
#            figure_size = (3,3)     
#       
#        fig = plt.figure(figsize=figure_size,dpi=300)
#        if legend:
#            ax = fig.add_axes([0,0,1,0.9])
#        else:
#            #ax = fig.add_axes([0,0,1,1])
#            ax = fig.add_subplot(1,1,1)
#        
#        ax.set_axis_off()
#         
#        class PlotPool():
#            def __init__(self, x, y, size, name, inputs, outputs, nr, reservoir_model):
#                self.x = x
#                self.y = y
#                self.size = size
#                self.name = name
#                self.inputs = inputs
#                self.outputs = outputs
#                self.nr = nr
#                # fixme:
#                # circular dependency
#                # actually a reservoir model can have pools and 
#                # pipelines (and should initialize them)
#                # the pipelines are not properties of a pool
#                # but of the model
#                # suggestion:
#                # new class for Pipe (or PlotPipe) that can plot itself
#                # with a color property set on initialization by the 
#                # model depending on the linearity
#                self.reservoir_model = reservoir_model
#
#            def plot(self, ax):
#                # plot the pool itself
#                ax.add_patch(mpatches.Circle((self.x, self.y), self.size, alpha=pool_alpha, color=pool_color))
#                if not thumbnail:
#                    ax.text(self.x, self.y, "$"+latex(self.name)+"$", fontsize = fontsize, horizontalalignment='center', verticalalignment='center')
#                
#                # plot input flux if there is one
#                if self.inputs:
#                    x1 = self.x
#                    y1 = self.y
#                    z1 = self.x-0.5 + (self.y-0.5)*1j
#                    arg1 = np.angle(z1) - np.pi/6
#    
#                    z1 = z1 + np.exp(1j*arg1) * self.size
#                    x1 = 0.5+z1.real
#                    y1 = 0.5+z1.imag
#                    
#                    z2 = z1 + np.exp(1j * arg1) * self.size * 1.0
#                    
#                    x2 = 0.5+z2.real
#                    y2 = 0.5+z2.imag
#        
#                    col = pipe_colors['linear']
#                    ax.add_patch(mpatches.FancyArrowPatch((x2,y2), (x1,y1), connectionstyle='arc3, rad=0.1', arrowstyle=arrowstyle, mutation_scale=mutation_scale, alpha=pipe_alpha, color=col))
#
#                if self.outputs:
#                    x1 = self.x
#                    y1 = self.y
#                    z1 = self.x-0.5 + (self.y-0.5)*1j
#                    arg1 = np.angle(z1) + np.pi/6
#    
#                    z1 = z1 + np.exp(1j*arg1) * self.size
#                    x1 = 0.5+z1.real
#                    y1 = 0.5+z1.imag
#                    
#                    z2 = z1 + np.exp(1j * arg1) * self.size *1.0
#                    
#                    x2 = 0.5+z2.real
#                    y2 = 0.5+z2.imag
#    
#                    col = pipe_colors[self.reservoir_model.output_flux_type(self.nr)]
#                    ax.add_patch(mpatches.FancyArrowPatch((x1,y1), (x2,y2), arrowstyle=arrowstyle, connectionstyle='arc3, rad=0.1', mutation_scale=mutation_scale, alpha=pipe_alpha, color=col))
#
#        nr_pools = self.nr_pools
#
#        base_r = 0.1 + (0.5-0.1)/10*nr_pools
#        if nr_pools > 1:
#            r = base_r * (1-np.exp(1j*2*np.pi/nr_pools))
#            r = abs(r) / 2 * 0.6
#            r = min(r, (0.5-base_r)*0.5)
#        else:
#            r = base_r * 0.5
#        
#        r = abs(r)
#
#        if thumbnail:
#            r = r * 0.7
#    
#        #patches.append(mpatches.Circle((0.5, 0.5), base_r))
#        pools = []
#        for i in range(nr_pools):
#            z = base_r * np.exp(i*2*np.pi/nr_pools*1j)
#            x = 0.5 - z.real
#            y = 0.5 + z.imag
#            if i in inputs.keys():
#                inp = inputs[i]
#            else:
#                inp = None
#            if i in outputs.keys():
#                outp = outputs[i]
#            else:
#                outp = None
#            pools.append(PlotPool(x, y, r, self.state_vector[i], inp, outp, i, self))
#
#        for pool in pools:
#            pool.plot(ax)
#        pipe_alpha=0.5
#
#        for (i,j) in internal_fluxes.keys():
#            z1 = (pools[i].x-0.5) + (pools[i].y-0.5) * 1j
#            z2 = (pools[j].x-0.5) + (pools[j].y-0.5) * 1j
#
#            arg1 = np.angle(z2-z1) - np.pi/20
#            z1 = z1+np.exp(1j*arg1)*r
#           
#            arg2 = np.angle(z1-z2)  + np.pi/20
#            z2 = z2+np.exp(1j*arg2)*r
#
#            x1 = 0.5+z1.real
#            y1 = 0.5+z1.imag
#
#            x2 = 0.5+z2.real
#            y2 = 0.5+z2.imag
#
#            col = pipe_colors[self.internal_flux_type(i,j)]
#
#            ax.add_patch(mpatches.FancyArrowPatch((x1,y1),(x2,y2), connectionstyle='arc3, rad=0.1', arrowstyle=arrowstyle, mutation_scale=mutation_scale, alpha=pipe_alpha, color=col))
#
#       
#        if legend:
#            legend_descs = []
#            legend_colors = []
#            for desc, col in pipe_colors.items():
#                legend_descs.append(desc)
#                legend_colors.append(mpatches.FancyArrowPatch((0,0),(1,1), connectionstyle='arc3, rad=0.1', arrowstyle=arrowstyle, mutation_scale=mutation_scale, alpha=pipe_alpha, color=col))
#            
#            ax.legend(legend_colors, legend_descs, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol = 3)
#        
#        return fig
#    
#
#
