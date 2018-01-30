# vim:set ff=unix expandtab ts=4 sw=4:
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

#import plotly.plotly as py
import plotly.graph_objs as go

from sympy import lambdify, flatten, latex, Function, sympify, sstr
from sympy.abc import _clash

from scipy.integrate import odeint, quad 
from scipy.interpolate import interp1d, UnivariateSpline
from scipy.optimize import newton, brentq

from tqdm import tqdm
import numpy as np
import pickle

from .SmoothReservoirModel import SmoothReservoirModel
from .helpers_reservoir import has_pw, numsol_symbolic_system, arrange_subplots, melt, generalized_inverse_CDF, draw_rv, stochastic_collocation_transform, numerical_rhs, MH_sampling, save_csv, load_csv, stride


#class SmoothModelRun:
class SmoothModelRun(ModelRun):
    def __init__(self, smooth_reservoir_model, parameter_set = None, start_values = None, times = None, func_set = {}):
        # we cannot use dict() as default because the test suite makes weird things with it!
        if parameter_set is None: parameter_set = dict()
        if func_set is None: func_set = dict()
        #fixme:
        # check for completeness and so on and so forth
        self.model = smooth_reservoir_model
        self.parameter_set = parameter_set
        self.times = times
        self.start_values = start_values
        if not(isinstance(start_values,np.ndarray)):
            raise(Exception("start_values should be a numpy array"))
        func_set = {str(key): val for key, val in func_set.items()}
        self.func_set = func_set
        self._state_transition_operator_values = None


    # create self.A(t)

    # in a linear model, A(t) is independent of the state_variables,
    # consequently, we can call _A with X = 0,
    # in a nonlinear model we would need to compute X(t) by solving the ODE first,
    # then plug it in --> much slower --> influences quantiles and forward transit time computation time

    # --> this should be respected by the class to which the model belongs
    def A(self, t):
        if not hasattr(self, '_A'):
            #fixme: what about a piecewise in the matrix?
            # is this here the right place to do it??
            cm_par = self.model.compartmental_matrix.subs(self.parameter_set)
            tup = tuple(self.model.state_vector) + (self.model.time_symbol.name,)
            cut_func_set = {key[:key.index('(')]: val for key, val in self.func_set.items()}
            A_func = lambdify(tup, cm_par, [cut_func_set, 'numpy'])
        
            def _A(t):
                #print('A', t)
                #fixme: another times cut off!
                t = min(t, self.times[-1])
                #print(t)
                #X = self.solve_single_value()(t) # nonlinear model needs that

                X = np.ones((self.nr_pools,)) # for a linear model this is OK (and faster)
                Xt = tuple(X) + (t,)
                return  A_func(*Xt)

            self._A = _A
            
        return self._A(t)     
   

    def linearize(self):
        sol_funcs = self.sol_funcs()
        
        srm = self.model
        xi, T, N, C, u = srm.xi_T_N_u_representation
        svec = srm.state_vector

        symbolic_sol_funcs = {sv: Function(sv.name + '_sol')(srm.time_symbol) for sv in svec}

        # need to define a function_factory to create the function we need to avoid late binding
        # with late binding pool will always be nr_pools and always the last function will be used!
        def func_maker(pool):
            def func(t):
                return sol_funcs[pool](t)

            return(func)

        sol_dict = {}
        for pool in range(self.nr_pools):
            key = sstr(symbolic_sol_funcs[svec[pool]])
            sol_dict[key] = func_maker(pool)


        linearized_A = (xi*T*N).subs(symbolic_sol_funcs)
        linearized_u = u.subs(symbolic_sol_funcs)

        func_set = self.func_set
        func_set.update(sol_dict)

        cl=srm.__class__
        linearized_srm = cl.from_A_u(
            srm.state_vector, 
            srm.time_symbol, 
            linearized_A, 
            linearized_u, 
            srm.content_unit, 
            srm.time_unit
        )      

        linearized_smr = self.__class__(
            linearized_srm, 
            self.parameter_set,
            self.start_values, 
            self.times, 
            func_set=func_set
        )
 
        return linearized_smr


    # return an ndarray (moments x pools) 
    @staticmethod
    def moments_from_densities(max_order, densities):
        n = densities(0).shape[0]

        def kth_moment(k):
            def kth_moment_pool(k, pool):
                norm = quad(lambda a: densities(a)[pool], 0, np.infty)[0]
                if norm == 0: return np.nan
                return quad(lambda a: a**k * densities(a)[pool], 0, np.infty)[0] / norm

            return np.array([kth_moment_pool(k,pool) for pool in range(n)])

        return np.array([kth_moment(k) for k in range(1, max_order+1)])

    
    ########## public methods and properties ########## 

    
    @property
    def nr_pools(self):
        return(self.model.nr_pools)

    def solve_single_value(self, alternative_start_values = None):
        return self._solve_age_moment_system_single_value(0, None, alternative_start_values)


    def solve(self, alternative_times = None, alternative_start_values = None):
        return self._solve_age_moment_system(0, None, alternative_times, alternative_start_values)


    ##### fluxes as functions #####
    

    #fixme: test
    def sol_funcs(self):
        times = self.times

        sol = self.solve(times)
        sol_funcs = []
        for i in range(self.nr_pools):
            sol_inter = interp1d(times, sol[:,i])
            sol_funcs.append(sol_inter)

        return(sol_funcs)
        

    #fixme: test and move
    def f_of_t_maker(self,sol_funcs,ol):
        def ot(t):
            sv = [sol_funcs[i](t) for i in range(self.nr_pools)]
            tup = tuple(sv)+(t,)
            res = ol(*tup)
            return(res)
        return(ot)


    def flux_funcs(self, expr_dict):
        m = self.model
        sol_funcs = self.sol_funcs()
        flux_funcs = {}
        tup = tuple(m.state_variables) + (m.time_symbol,)
        for key, value in expr_dict.items():
            o_par = sympify(value, locals=_clash).subs(self.parameter_set)
            cut_func_set = {key[:key.index('(')]: val for key, val in self.func_set.items()}
            ol = lambdify(tup, o_par, modules = [cut_func_set, 'numpy'])
            flux_funcs[key] = self.f_of_t_maker(sol_funcs, ol)

        return(flux_funcs)


    def external_input_flux_funcs(self):
        return(self.flux_funcs(self.model.input_fluxes))


    def internal_flux_funcs(self):
        return(self.flux_funcs(self.model.internal_fluxes))


    def output_flux_funcs(self):
        return(self.flux_funcs(self.model.output_fluxes))
    

    def output_vector_func(self, t):
        res = np.zeros((self.nr_pools,))
        for key, value in self.output_flux_funcs().items():
            res[key] = value(t)

        return res


    ##### fluxes as vector-valued functions #####
    

    #fixme: returns a function
    def external_input_vector_func(self):
        t0 = self.times[0]
        # cut off inputs until t0
        t_valid = lambda t: True if (t0<t) and (t<=self.times[-1]) else False

        input_fluxes = []
        for i in range(self.nr_pools):
            if i in self.external_input_flux_funcs().keys():
                input_fluxes.append(self.external_input_flux_funcs()[i])
            else:
                input_fluxes.append(lambda t: 0)
        
        u = lambda t: np.array([f(t) for f in input_fluxes], dtype=np.float) if t_valid(t) else np.zeros((self.nr_pools,))
        return u

    # fixme: returns a vector
    def output_rate_vector_at_t(self, t):
        n = self.nr_pools

        sol_funcs = self.sol_funcs()
        output_vec_at_t = self.output_vector_func(t)

        rate_vec = np.zeros((n,))
        for pool in range(n):
            x = sol_funcs[pool](t)
            if x != 0:
                rate_vec[pool] = output_vec_at_t[pool] / x

        return rate_vec


    ##### fluxes as vector over self.times #####

    @property
    def external_input_vector(self):
        res = self._flux_vector(self.model.external_inputs)
        # no inputs at t0 (only >t0)
        res[0,:] = np.zeros((self.nr_pools,))
        
        return res

    @property
    def external_output_vector(self):
        return(self._flux_vector(self.model.external_outputs))


    @property    
    def output_rate_vector(self):
        n = self.nr_pools
        times = self.times
        soln = self.solve()
        output_vec = self.external_output_vector

        # take care of possible division by zero
        output_vec[soln==0] = 0
        soln[soln==0] = 0

        return output_vec/soln



    ##### age density methods #####
    

    def pool_age_densities_single_value(self, start_age_densities = None):
        p1_sv = self._age_densities_1_single_value(start_age_densities)
        p2_sv = self._age_densities_2_single_value()

        p_sv = lambda a, t: p1_sv(a,t) + p2_sv(a,t)
        
        return p_sv

    
    # returns a function p that takes an age array "ages" as argument
    # and gives back a three-dimensional ndarray (ages x times x pools)
    # start_age_densities is a array-valued function of age
    def pool_age_densities_func(self, start_age_densities = None):
        p1 = self._age_densities_1(start_age_densities)
        p2 = self._age_densities_2()
        
        def p(ages):
            if hasattr(self, '_computed_age_density_fields'):
                if (start_age_densities, tuple(ages)) in self._computed_age_density_fields.keys():
                    #print('using cached result')
                    return self._computed_age_density_fields[(start_age_densities, tuple(ages))]
            else:
                self._computed_age_density_fields = {}
        
            field_list = []
            for a in tqdm(ages):
                field_list.append(p1(np.array([a])) + p2(np.array([a])))

            field = np.array(field_list)[:,0,:,:]
            
            self._computed_age_density_fields[(start_age_densities, tuple(ages))] = field
            return field
                
        return p

    
    def system_age_density_single_value(self, start_age_densities = None):
        p_sv = self.pool_age_densities_single_value(start_age_densities)
        sys_p_sv = lambda a, t: sum(p_sv(a,t))

        return sys_p_sv


    # return array ages x times with ages based on pool_age_densities
    def system_age_density(self, pool_age_densities):
        return pool_age_densities.sum(2)


    def age_densities(self, pool_age_densities, system_age_density):
        # combine pool and system age densities to one numpy array
        n = self.nr_pools
        nr_ages = pool_age_densities.shape[0]
        nr_times = pool_age_densities.shape[1]

        _age_densities = np.zeros(nr_ages, nr_times, n+1)
        _age_densities[:,:,:n] = pool_age_densities
        _age_densities[:,:,n] = system_age_density

        return _age_densities


    ##### age moment methods #####


    # really slow, just here to show that everything works
    def age_moment_vector_from_densities(self, order, start_age_densities):
        p_sv = self.pool_age_densities_single_value(start_age_densities)
        times = self.times
        x = self.solve()
        n = self.nr_pools
        k = order

        def am_at_time_index_for_pool(ti, pool):
            def integrand(a):
                return (a**k) * p_sv(a, times[ti])[pool]
            
            return x[ti, pool]**(-1) * quad(integrand, 0, np.inf)[0]        

        def age_moment_at_time_index(ti):
            return np.array([am_at_time_index_for_pool(ti, pool) for pool in range(n)])

        am_arr = np.array([age_moment_at_time_index(ti) for ti in range(len(times))]) 
        am = np.ndarray((len(times), n), np.float, am_arr)

        return am


    def age_moment_vector_semi_explicit(self, order, start_age_moments = None, times = None):
        if times is None: times = self.times
        t0 = times[0]
        n = self.nr_pools
        k = order
        
        if start_age_moments is None:
            start_age_moments = np.zeros((order, n))

        start_age_moments[np.isnan(start_age_moments)] = 0

        p2_sv = self._age_densities_2_single_value()

        def binomial(n, k):
            return 1 if k==0 else (0 if n==0 else binomial(n-1, k) + binomial(n-1, k-1))

        Phi = lambda t, t0, x: self._state_transition_operator(t, t0, x)

        def x0_a0_bar(j):
            if j == 0: 
                return self.start_values
                
            return np.array(self.start_values) * start_age_moments[j-1,:]

        def both_parts_at_time(t):
            def part2_time(t):
                def part2_time_index_pool(ti, pool):
                    return quad(lambda a: a**k * p2_sv(a, t)[pool], 0, t-t0)[0]

                return np.array([part2_time_index_pool(t, pool) for pool in range(n)])

            def part1_time(t):
                def summand(j):
                    return binomial(k, j)*(t-t0)**(k-j)*Phi(t, t0, x0_a0_bar(j))

                return sum([summand(j) for j in range(k+1)])

            return part1_time(t) + part2_time(t)

        soln = self.solve()

        def both_parts_normalized_at_time_index(ti):
            t = times[ti]
            bp = both_parts_at_time(t)
            diag_values = np.array([x if x>0 else np.nan for x in soln[ti,:]])
            X_inv = np.diag(diag_values**(-1))

            return (np.mat(X_inv) * np.mat(bp).transpose()).A1

        return np.array([both_parts_normalized_at_time_index(ti) for ti in range(len(times))])
        

    def age_moment_vector(self, order, start_age_moments = None):
        n = self.nr_pools
        times = self.times
        
        if start_age_moments is None:
            start_age_moments = np.zeros((order, n))

        if not (0 in self.start_values):
            ams = self._solve_age_moment_system(order, start_age_moments)
            return ams[:,n*order:]
        else:
            # try to start adapted mean_age_system once no pool as np.nan as mean_age (empty pool)

            # find last time index that contains an empty pool --> ti
            soln = self.solve()
            ti = len(times)-1
            content = soln[ti,:]
            while not (0 in content) and (ti>0): 
                ti = ti-1
                content = soln[ti,:]

            # not forever an empty pool there?
            if ti+1 < len(times):
                # compute moment with semi-explicit formula as long as there is an empty pool
                amv1_list = []
                amv1 = np.zeros((ti+2, order*n))
                for k in range(1, order+1):
                    amv1_k = self.age_moment_vector_semi_explicit(k, start_age_moments, times[:ti+2])
                    amv1[:,(k-1)*n:k*n] = amv1_k

                # use last values as start values for moment system with nonzero start values
                new_start_age_moments = amv1[-1,:].reshape((n, order))
                start_values = soln[ti+1]
                ams = self._solve_age_moment_system(order, new_start_age_moments, times[ti+1:], start_values)
                amv2 = ams[:,n*order:]

                # put the two parts together
                part1 = amv1[:,(order-1)*n:order*n][:-1]
                amv = np.ndarray((len(times), n))
                amv[:part1.shape[0], :part1.shape[1]] = part1
                amv[part1.shape[0]:, :amv2.shape[1]] = amv2
                return amv
            else:
                # always an empty pool there
                return self.age_moment_vector_semi_explicit(order, start_age_moments)


    # requires start moments <= order
    def system_age_moment(self, order, start_age_moments = None):
        n = self.nr_pools
        age_moment_vector = self.age_moment_vector(order, start_age_moments)
        age_moment_vector[np.isnan(age_moment_vector)] = 0
        soln = self.solve()
         
        total_mass = soln.sum(1) # row sum
        total_mass[total_mass==0] = np.nan

        system_age_moment = (age_moment_vector*soln).sum(1)/total_mass

        return system_age_moment
        

    ##### transit time density methods #####


    def backward_transit_time_density_single_value(self, start_age_densities):
        n = self.nr_pools
        p_age_sv = self.pool_age_densities_single_value(start_age_densities)

        def p_sv(a, t):
            p = p_age_sv(a, t)
            r = self.output_rate_vector_at_t(t)
            return (r*p).sum() 
            
        return p_sv


    # return an array ages x times with ages based on pool_age_densities
    def backward_transit_time_density(self, pool_age_densities):
        r = self.output_rate_vector
        return (pool_age_densities*r).sum(2)

    
    def forward_transit_time_density_single_value(self, cut_off = True):
        n = self.nr_pools
        times = self.times
        Phi = self._state_transition_operator
        input_func = self.external_input_vector_func()
        t0 = times[0]   
        t_max = times[-1] 
        def p_ftt_sv(a, t):
            #print(a,t)
            # nothing leaves before t0
            if (t+a < t0): return 0

            #fixme: for MH we might need the density ver far away...
            # we cannot compute the density if t+a is out of bounds
            if cut_off and (t+a > t_max): return np.nan

            u = input_func(t)
            if sum(u) == 0: return np.nan
            if (a < 0): return 0.0
            
            return -self.A(t+a).dot(Phi(t+a, t, u)).sum()

        return p_ftt_sv


    #fixme: return value not consistent with backward_transit_time_density
    # not that easy to resolve, since here we do not use age_densities,
    # instead ages is really needed to be able to make the shift or call the state_transition_operator
    def forward_transit_time_density_func(self, cut_off = True):
        p_sv = self.forward_transit_time_density_single_value(cut_off)
        pp = lambda a: np.array([p_sv(a,t) for t in self.times], np.float)
        #p = lambda ages: np.array([pp(a) for a in ages], np.float)
        def p(ages):
            field_list = []
            for a in tqdm(ages):
                field_list.append(pp(a))

            field = np.array(field_list)

            return field

        return p


    ##### transit time moment methods #####

    
    # really slow, just here to show that everything works
    def backward_transit_time_moment_from_density(self, order, start_age_densities):
        p_sv = self.backward_transit_time_density_single_value(start_age_densities)
        times = self.times
        k = order

        ext_outp_vec = self.external_output_vector
        ext_outp = ext_outp_vec.sum(1)
     
        def btt_moment_at_time_index(ti):
            def integrand(a):
                return (a**k) * p_sv(a, times[ti])
            
            return ext_outp[ti]**(-1) * quad(integrand, 0, np.inf)[0]        

        bttm = np.array([btt_moment_at_time_index(ti) for ti in range(len(times))]) 
        return bttm


    def backward_transit_time_moment(self, order, start_age_moments):
        times = self.times

        age_moment_vector = self.age_moment_vector(order, start_age_moments)
        r = self.external_output_vector
        
        return (r*age_moment_vector).sum(1)/r.sum(1)


    def forward_transit_time_moment_from_density(self, order, start_age_densities):
        # we cannot compute it using the backward transit time density, 
        # because solutions and fluxes are given only on a finite time interval
        # we can make it work for symbolically given systems if we really need to,
        # but it will be pretty slow
        pass


    def forward_transit_time_moment(self, order):
        k = order
        times = self.times
        Phi = self._state_transition_operator
        input_vector = self.external_input_vector

        #import warnings
        #from scipy.integrate import IntegrationWarning
        #warnings.simplefilter("error", IntegrationWarning)
        def moment_at_ti(ti):
            u = input_vector[ti] 
            
            # if we have no inputs, there cannot be a transit(time)
            if u.sum() == 0:    
                return np.nan

            def integrand(a):
                res = (k*a**(k-1) * Phi(times[ti]+a, times[ti], u).sum())/u.sum()
                #res = (k*a**(k-1) * Phi(54+a, 54, u).sum())/u.sum()
                #res = (Phi(54+a, 54, u).sum())/u.sum()
                #print(a, Phi(times[ti]+a, times[ti], u), res)
                return res

            # fixme:
            # it is possible that quad can be replaced by something
            # that is better suited for the infinite integration domain
            # that is always required for forward transit times.
            #print(times[ti], '\n')
            return quad(integrand, 0, np.infty)[0]

        res = np.array([moment_at_ti(ti) for ti in range(len(times))])
        return res

    #fixme: split into two functions for SCCS and MH
    def apply_to_forward_transit_time_simulation(self, f_dict = {'mean': np.mean}, N = 10000, M = 2, k = 5, MH = False):
        # f is a Python function, for the mean, take f = np.mean
        # N is the number of simulations per each time step
        # M is the number of collocation points for stochastic collocation sampling
        # allowed values for M are 2, 3, 4, ..., 11
        # other values lead to inverse transform sampling (slow)
        # k is the order of the smoothing and interpolating spline
        # 'smoothin_spline' is best used for inverse transform sampling, because of additional smoothing for low
        # number of random variates
        # for SCMCS (M in [2,...,11]), 'interpolation' is better, because the higher number of random variates 
        # (because of faster sampling) makes their mean already quite precise (in the framework of what is possible with SCMCS)
  
        times = self.times
        Phi = self._state_transition_operator
        input_func = self.external_input_vector_func()

        if not MH:
            self.n = 0
            def F_FTT(a, t):
                u = input_func(t)
                if u.sum() == 0: 
                    return np.nan
                
                if (a <= 0): return 0.0

                self.n += 1
                return 1 - Phi(t+a, t, u).sum()/u.sum()
    
            
            def simulate(n, CDF):
                # compute lagrange polynomial p if M is in [2, ..., 11]
                g = stochastic_collocation_transform(M, CDF)
                if g is None: 
                    # inverse transform sampling
                    print('inverse transform sampling')
                    rvs = np.array([draw_rv(CDF) for _ in range(n)])
                else:
                    norms = np.random.normal(size = n)
                    rvs = g(norms)
        
                return rvs

        else:
            self.m = 0
            p_sv = self.forward_transit_time_density_single_value(cut_off = False)
            def f_FTT(a, t):
                self.m += 1
                return p_sv(a, t)


        res = {f_name: {'values': [], 'smoothing_spline': None, 'interpolation': None} for f_name in f_dict.keys()}
        for t in times:
            print('time', t)
            # no iput means no forward transit time
            u = input_func(t)
            if u.sum() == 0: 
                rvs = np.nan
            else:
                if not MH:
                    rvs = simulate(N, lambda a: F_FTT(a, t))
                    print(self.n, 'calls of state transition operator')
                else:
                    rvs = MH_sampling(N, lambda a: f_FTT(a, t))
                    print(self.m, 'calls of forward transit time density')

            for f_name, f in f_dict.items():
                value = f(rvs)
                res[f_name]['values'].append(value)
                print(f_name, value)
                
        for f_name in res.keys():
            y = np.array(res[f_name]['values'])
            z = y.copy()
            res[f_name]['values'] = y.copy()

            # give weight zero to nan values fo compting the spline
            w = np.isnan(y)
            y[w] = 0.
            res[f_name]['smoothing_spline'] = UnivariateSpline(times, y, w=~w, k=k, check_finite=True)
            res[f_name]['interpolation'] = interp1d(times[~w], z[~w], kind=k)

        return res

    # use inverse transform sampling
    def apply_to_forward_transit_time_simulation_its(self, f_dict, times, N = 1000, k = 5):
        # f is a Python function, for the mean, take f = np.mean
        # N is the number of simulations per each time step
        # times is an np.array of interpolation points
        # k is the order of the smoothing and interpolating spline
        # 'smoothin_spline' is best used for inverse transform sampling, because of additional smoothing for low
        # number of random variates
  
        Phi = self._state_transition_operator
        input_func = self.external_input_vector_func()

        def F_FTT(a, t):
            u = input_func(t)
            if u.sum() == 0: 
                return np.nan
            
            if (a <= 0): return 0.0

            return 1 - Phi(t+a, t, u).sum()/u.sum()

        res = {f_name: {'values': [], 'smoothing_spline': None, 'interpolation': None} for f_name in f_dict.keys()}
        for t in times:
            print('time', t)
            # no iput means no forward transit time
            u = input_func(t)
            if u.sum() == 0: 
                rvs = np.nan
            else:
                CDF = lambda a: F_FTT(a, t)
                rvs = np.array([draw_rv(CDF) for _ in range(N)])

            for f_name, f in f_dict.items():
                value = f(rvs)
                res[f_name]['values'].append(value)
                print(f_name, value)
                
        def compute_splines(res, times):
            for f_name in res.keys():
                y = np.array(res[f_name]['values'])
                z = y.copy()
                res[f_name]['values'] = y.copy()

                # give weight zero to nan values fo compting the spline
                w = np.isnan(y)
                y[w] = 0.
                res[f_name]['smoothing_spline'] = UnivariateSpline(times, y, w=~w, k=k, check_finite=True)
                res[f_name]['interpolation'] = interp1d(times[~w], z[~w], kind=k)

            return res

        return compute_splines(res, times)


    ##### comma separated values output methods #####


    ## age ##


    def save_pools_and_system_density_csv(self, filename, pool_age_densities, system_age_density, ages):
        n = self.nr_pools
        times = self.times
    
        ndarr = np.zeros((system_age_density.shape[0], len(times), n+1))
        ndarr[:,:,:n] = pool_age_densities
        ndarr[:,:,n] = system_age_density

        pool_entries = [i for i in range(n)] + [-1]
        melted = melt(ndarr, [ages, times, pool_entries])
        header = '"age", "time", "pool", "value"'
        save_csv(filename, melted, header)


    def save_pools_and_system_value_csv(self, filename, pools_ndarr, system_arr):
        n = self.nr_pools
        times = self.times
    
        ndarr = np.concatenate((pools_ndarr, system_arr.reshape((len(times), 1))), axis=1)

        pool_entries = [i for i in range(n)] + [-1]
        melted = melt(ndarr, [times, pool_entries])
        header = '"time", "pool", "value"'
        save_csv(filename, melted, header)


    def density_values_for_pools(self, pool_densities_sv, pool_age_values):
        n = self.nr_pools
        times = self.times
    
        # for each pool we have a different age value 
        z = []
        for pool in range(n):
            val = pool_age_values[:,pool]
            #z.append(np.array([pool_densities_sv(val[i], times[i])[pool] for i in range(len(times))]))
            new_z_list = []
            for i in tqdm(range(len(times))):
                new_z_list.append(pool_densities_sv(val[i], times[i])[pool])

            z.append(np.array(new_z_list))

            z = np.array(z).T

        return z

    # return density values for mean, median, etc.
    #fixme: test
    def density_values(self, density_sv, values):
        times = self.times
        def f(i):
            if np.isnan(values[i]): return np.nan
            return density_sv(values[i], times[i])

        #dv_list = [f(i) for i in range(len(times))]

        dv_list = []
        for i in tqdm(range(len(times))):
            dv_list.append(f(i))

        return np.array(dv_list)


    ## transit time ##


    def save_value_csv(self, filename, ndarr):
        melted = melt(ndarr, [self.times])
        header = '"time", "value"'
        save_csv(filename, melted, header)


    def save_density_csv(self, filename, density, ages, times = None):
        if times is None: times = self.times
        melted = melt(density, [ages, times])
        header = '"age", "time", "value"'
        save_csv(filename, melted, header)
        

    ##### comma separated values input methods #####


    ## combining pool and system structures ##


    def combine_pools_and_system_values(self, pools_values, system_values):
        n = self.nr_pools
        times = self.times
        values = np.zeros((len(times), n+1))
        values[:,:n] = pools_values
        values[:, n] = system_values
    
        return values


    ## age ##

    
    #attention: assumes that density was saved with the exact same ages and times and pools
    def load_pools_and_system_densities_csv(self, filename, ages):
        melted = load_csv(filename)
        n = self.nr_pools
        
        return np.ndarray((len(ages), len(self.times), n+1), buffer=(melted[:,3]).copy())


    #attention: assumes that density was saved with the exact same ages and times
    def load_density_csv(self, filename, ages):
        melted = load_csv(filename)
        
        return np.ndarray((len(ages), len(self.times)), buffer=(melted[:,2]).copy())


    #attention: assumes that values were saved with the exact same times and pools
    def load_pools_and_system_value_csv(self, filename):
        melted = load_csv(filename)

        n = self.nr_pools
        values_lst = []
        for pool in range(n):
            indices = melted[:,1] == pool
            values_lst.append(melted[np.ix_(indices),2][0])
        pool_values = np.array(values_lst).transpose()

        indices = melted[:,1] == -1
        system_values = melted[np.ix_(indices),2][0]

        return (pool_values, system_values)


    ##### plotting methods #####

    
    ## solutions ##


    def plot_solutions(self, fig, fontsize = 10):
    #fixme:
    # since time units and units are related to those
    # of the other fluxes it would be more consistent
    # to make them a property of SmoothModelRun and use
    # them in the other plots as well

        times = self.times
        n = self.nr_pools
        soln = self.solve()


        def make_ax_nice(ax, title):
            ax.set_title(title, fontsize = fontsize)
            ax.set_xlabel(self._add_time_unit(latex(self.model.time_symbol)), fontsize=fontsize)
            ax.set_ylabel(self._add_content_unit('content'), fontsize=fontsize)
            ax.set_xlim(times[0], times[-1])
            ax.set_ylim(ax.get_ylim()[0]*0.9, ax.get_ylim()[1]*1.1)
        

        ax = fig.add_subplot(n+1, 1, 1)
        ax.plot(times, soln.sum(1))
        make_ax_nice(ax, 'System')

        for pool in range(n):
            ax = fig.add_subplot(n+1, 1, 2+pool)
            ax.plot(times, soln[:,pool])
            make_ax_nice(ax, "$" + latex(self.model.state_variables[pool]) + "$")

        fig.tight_layout()
   
 
    def plot_phase_plane(self, ax, i, j, fontsize = 10):
        times = self.times
        soln = self.solve()
        ax.plot(soln[:, i], soln[:, j])

        x0 = soln[0, i]
        y0 = soln[0, j]
        ax.scatter([x0],[y0], s=60)

        x1 = soln[[len(times)//2-1], i][0]
        y1 = soln[[len(times)//2-1], j][0]
        x2 = soln[[len(times)//2+1], i][0]
        y2 = soln[[len(times)//2+1], j][0]
        ax.add_patch(mpatches.FancyArrowPatch((x1,y1), (x2,y2), arrowstyle='simple', mutation_scale=20, alpha=1))

        ax.set_xlabel(self._add_content_unit("$"+latex(self.model.state_variables[i])+"$"), fontsize=fontsize)
        ax.set_ylabel(self._add_content_unit("$"+latex(self.model.state_variables[j])+"$"), fontsize=fontsize)


    def plot_phase_planes(self, fig, fontsize = 10):
        n = len(self.model.state_vector)
        planes = [(i,j) for i in range(n) for j in range(i)]

        rows, cols = arrange_subplots(len(planes))

        for k, (i, j) in enumerate(planes):
            ax = fig.add_subplot(rows, cols, k+1)
            self.plot_phase_plane(ax, i, j, fontsize)
            ax.get_xaxis().set_ticks([])
            ax.get_yaxis().set_ticks([])

        fig.tight_layout()
    

    ## fluxes ##
    

    def plot_internal_fluxes(self, fig, fontsize = 10):
        internal_flux_funcs = self.internal_flux_funcs()
        n = len(internal_flux_funcs.keys())
        times = self.times
        #n=self.nr_pools
        i = 1
        for key, value in internal_flux_funcs.items():
            ax = fig.add_subplot(n,1,i)
            ax.plot(times, [internal_flux_funcs[key](t) for t in times])
    
            ax.set_title('Flux from $' + latex(self.model.state_variables[key[0]]) + '$ to $'
                                       + latex(self.model.state_variables[key[1]]) + '$',
                         fontsize=fontsize)
            ax.set_xlabel(self._add_time_unit('$' + latex(self.model.time_symbol) + '$'), fontsize=fontsize)
            ax.set_ylabel(self._add_flux_unit('flux'), fontsize=fontsize)
            i += 1

        fig.tight_layout()


    def plot_external_output_fluxes(self, fig, fontsize = 10):
        times = self.times
        output_flux_funcs = self.output_flux_funcs()
        n = len(output_flux_funcs.keys())
        
        i = 1
        for key, value in output_flux_funcs.items():
            ax = fig.add_subplot(n,1,i)
            ax.plot(times, [output_flux_funcs[key](t) for t in times])
            ax.set_title('External outflux from $' + latex(self.model.state_variables[key]) + '$', fontsize=fontsize)
            ax.set_xlabel(self._add_time_unit('$' + latex(self.model.time_symbol) + '$'), fontsize=fontsize)
            ax.set_ylabel(self._add_flux_unit('flux'), fontsize=fontsize)
            i += 1

        fig.tight_layout()
                
    
    def plot_external_input_fluxes(self, fig, fontsize = 10):
        times = self.times
        input_flux_funcs = self.external_input_flux_funcs()
        n = len(input_flux_funcs.keys())
        i = 1
        for key, value in input_flux_funcs.items():
            ax = fig.add_subplot(n,1,i)
            ax.plot(times, [input_flux_funcs[key](t) for t in times])
            ax.set_title('External influx to $' + latex(self.model.state_variables[key]) + '$', fontsize=fontsize)
            ax.set_xlabel(self._add_time_unit('$' + latex(self.model.time_symbol) + '$'), fontsize=fontsize)
            ax.set_ylabel(self._add_flux_unit('flux'), fontsize=fontsize)
            i += 1

        fig.tight_layout()


    # means # 


    def plot_mean_ages(self, fig, start_mean_ages):
        times = self.times
        n = self.nr_pools
        start_age_moments = np.ndarray((1,n), np.float, np.array(start_mean_ages))
        time_symbol = self.model.time_symbol
        states = self.model.state_variables

        ma_vector = self.age_moment_vector(1, start_age_moments)
        sma = self.system_age_moment(1, start_age_moments)

        def make_ax_nice(ax, title):
            ax.set_title(title)
            ax.set_xlabel(self._add_time_unit("$" + latex(time_symbol) + "$"))
            ax.set_ylabel(self._add_time_unit("mean age"))

            ax.set_xlim([times[0], times[-1]])

        ax = fig.add_subplot(n+1, 1, 1)
        ax.plot(times, sma)
        make_ax_nice(ax, "System")

        for i in range(n):
            ax = fig.add_subplot(n+1, 1, 2+i)
            ax.plot(times, ma_vector[:,i])
            make_ax_nice(ax, "$" + latex(states[i]) + "$")
                
        fig.tight_layout()


    def plot_mean_backward_transit_time(self, ax, start_mean_ages):
        times = self.times
        n = self.nr_pools
        start_age_moments = np.ndarray((1,n), np.float, np.array(start_mean_ages))
        time_symbol = self.model.time_symbol
        tr_val = self.backward_transit_time_moment(1, start_age_moments)
        ax.plot(times, tr_val)
        
        ax.set_title("Mean backward transit time")

        ax.set_xlabel(self._add_time_unit("$" + latex(time_symbol) + "$"))
        ax.set_ylabel(self._add_time_unit("mean BTT"))

        ax.set_xlim([times[0], times[-1]])


    ## densities ##


    # age #

    
    def add_line_to_density_plot_plotly(self, fig, data, color, name, time_stride = 1, width = 5, on_surface = True, bottom = True, legend_on_surface = False, legend_bottom = False):
        times = self.times
        strided_data = stride(data, time_stride)
        strided_times = stride(times, time_stride)
    
        if bottom:
            trace_bottom = go.Scatter3d(
            name=name,
            x=-strided_times, y=strided_data, z=0*strided_times,
            mode = 'lines',
            line=dict(
                color=color,
                width=width
                ),
            showlegend = legend_bottom
            )
            fig['data'] += [trace_bottom]

        if on_surface:
            # compute the density values on the surface
            #strided_times = -fig['data'][0]['x']
            strided_ages = fig['data'][0]['y']
            density_data = fig['data'][0]['z']

            strided_z = []
            for ti in range(len(strided_times)):
                time = strided_times[ti]
                age = strided_data[ti]

                if (np.isnan(age)) or (age < strided_ages[0]) or (age > strided_ages[-1]):
                    strided_z.append(np.nan)
                else:
                    ti_lower = strided_times.searchsorted(time)-1
                    ti_upper = ti_lower+1 if ti_lower+1<len(strided_times) else ti_lower
                    time_lower = strided_times[ti_lower]
                    time_upper = strided_times[ti_upper]
    
                    ai_lower = strided_ages.searchsorted(age)-1
                    ai_upper = ai_lower+1 if ai_lower+1<len(strided_ages) else ai_lower
                    age_lower = strided_ages[ai_lower]
                    age_upper = strided_ages[ai_upper]
    
                    bl_density_value = density_data[ai_lower, ti_lower]
                    br_density_value = density_data[ai_lower, ti_upper]
                    bottom_density_value = bl_density_value + (time-time_lower)/(time_upper-time_lower) * (br_density_value-bl_density_value)
    
                    tl_density_value = density_data[ai_upper, ti_lower]
                    tr_density_value = density_data[ai_upper, ti_upper]
                    top_density_value = tl_density_value + (time-time_lower)/(time_upper-time_lower) * (tr_density_value-tl_density_value)
    
                    density_value = bottom_density_value + (age-age_lower)/(age_upper-age_lower) * (top_density_value-bottom_density_value)
                    strided_z.append(density_value)


            trace_on_surface = go.Scatter3d(
            name=name,
            x=-strided_times, y=strided_data, z=strided_z,
            mode = 'lines',
            line=dict(
                color=color,
                width=width
                ),
            showlegend = legend_on_surface
            )
            fig['data'] += [trace_on_surface]



    def plot_3d_density_plotly(self, title, density_data, ages, age_stride = 1, time_stride = 1):
        data, layout = self._density_plot_plotly(density_data, ages, age_stride, time_stride)
        layout['title'] = title
        fig = go.Figure(data=data, layout=layout)
        
        return fig
    

    def add_equilibrium_surface_plotly(self, fig, opacity = 0.9, index = 0):
        data = fig['data'][0]
        x = data['x']
        y = data['y']
        z = data['z'].copy()
        for ti in range(z.shape[1]):
            z[:,ti] = z[:,index]
        eq_surface_data = go.Surface(x=x, 
                                      y=y, 
                                      z=z, 
                                      showscale=False,
                                      opacity = opacity,
                                      surfacecolor=np.zeros_like(z))
        fig['data'].append(eq_surface_data)


    ##### cumulative distribution methods #####


    def cumulative_pool_age_distributions_single_value(self, start_age_densities = None, F0 = None):
        n = self.nr_pools
        soln = self.solve()
        if soln[0,:].sum() == 0:
            start_age_densities = lambda a: np.zeros((n,))

        if F0 is None and start_age_densities is None:
            raise(Exception('Either F0 or start_age_densities must be given.'))

        times = self.times
        t0 = times[0]
        #sol_funcs = self.sol_funcs()
        #sol_funcs_array = lambda t: np.array([sol_funcs[pool](t) for pool in range(n)])
        sol_funcs_array = self.solve_single_value()

        if F0 is None:
            p0 = start_age_densities
            F0 = lambda a: np.array([quad(lambda s: p0(s)[pool], 0, a)[0] for pool in range(n)])

        Phi = self._state_transition_operator

        def G_sv(a, t):
            if a < t-t0: return np.zeros((n,))
            #print(t, t0, a-(t-t0))
            return Phi(t, t0, F0(a-(t-t0)))


        def H_sv(a, t):
            # count everything from beginning?
            if a >= t-t0: a = t-t0

            # mass at time t
            #x_t_old = np.array([sol_funcs[pool](t) for pool in range(n)])
            x_t = sol_funcs_array(t)
            # mass at time t-a
            #x_tma_old = [np.float(sol_funcs[pool](t-a)) for pool in range(n)]
            x_tma = sol_funcs_array(t-a)
            # what remains from x_tma at time t
            m = Phi(t, t-a, x_tma)
            # difference is not older than t-a
            res = x_t-m
            # cut off accidental negative values
            return np.maximum(res, np.zeros(res.shape))

        return lambda a, t: G_sv(a,t) + H_sv(a,t)
                

    def cumulative_system_age_distribution_single_value(self, start_age_densities = None, F0 = None):
        n = self.nr_pools
        soln = self.solve()
        if soln[0,:].sum() == 0:
            start_age_densities = lambda a: np.zeros((n,))
        
        if F0 is None and start_age_densities is None:
            raise(Exception('Either F0 or start_age_densities must be given.'))

        F_sv = self.cumulative_pool_age_distributions_single_value(start_age_densities=start_age_densities, F0=F0)
        
        return lambda a, t: F_sv(a,t).sum()


    #fixme: test
    def cumulative_backward_transit_time_distribution_single_value(self, start_age_densities = None, F0 = None):
        if F0 is None and start_age_densities is None:
            raise(Exception('Either F0 or start_age_densities must be given.'))

        F_sv = self.cumulative_pool_age_distributions_single_value(start_age_densities=start_age_densities, F0=F0)
        rho = self.output_rate_vector_at_t

        def F_btt_sv(a, t):
            res = (rho(t)*F_sv(a, t)).sum()
            #print(a, t, res)
            return res

        return F_btt_sv


#    #fixme: test
#    def cumulative_backward_transit_time_distribution_single_value_a_ti(self, start_age_densities = None, F0 = None):
#        if F0 is None and start_age_densities is None:
#            raise(Exception('Either F0 or start_age_densities must be given.'))
#
#        F_sv = self.cumulative_pool_age_distributions_single_value(start_age_densities=start_age_densities, F0=F0)
#        rho = self.output_rate_vector
#
#        times = self.times
#        def F_btt_sv_a_ti(a, ti):
#            res = (rho[ti]*F_sv(a, times[ti])).sum()
#            #print(a, t, res)
#            return res
#
#        return F_btt_sv_a_ti


    #fixme: test
    def cumulative_forward_transit_time_distribution_single_value(self, cut_off = True):
        times = self.times
        t_max = times[-1]
        Phi = self._state_transition_operator
        u_func = self.external_input_vector_func()

        def F_ftt_sv(a, t):
            #print(a, t, a+t>t_max)
            if cut_off and a+t>t_max: return np.nan
            u = u_func(t)
            res = u.sum() - Phi(t+a, t, u).sum()
            #print(a, t, u, res)
            return res

        return F_ftt_sv


#    #fixme: test
#    def cumulative_forward_transit_time_distribution_single_value_a_ti(self, cut_off = True):
#        times = self.times
#        t_max = times[-1]
#        Phi = self._state_transition_operator
#        u_vec = self.external_input_vector
#
#        def F_ftt_sv(a, ti):
#            t = times[ti]
#            #print(a, t, a+t>t_max)
#            if cut_off and a+t>t_max: return np.nan
#            u = u_vec[ti]
#            res = u.sum() - Phi(t+a, t, u).sum()
#            #print(a, t, u, res)
#            return res
#
#        return F_ftt_sv


    ##### quantiles #####


#    def pool_age_distributions_quantiles(self, quantile, start_values = None, start_age_densities = None, F0 = None, method = 'brentq', tol = 1e-8):
#        n = self.nr_pools
#        soln = self.solve()
#        if soln[0,:].sum() == 0:
#            start_age_densities = lambda a: np.zeros((n,))
#
#        if F0 is None and start_age_densities is None:
#            raise(Exception('Either F0 or start_age_densities must be given.'))
#
#        times = self.times
#
#        if start_values is None:
#            start_values = np.ones((len(times), n))
#
#        F_sv = self.cumulative_pool_age_distributions_single_value(start_age_densities=start_age_densities, F0=F0)
#        soln = self.solve()
#        def quantile_at_ti(ti):
#            def quantile_at_ti_in_pool(ti, pool):
#                #print('t:', times[ti], 'q*x:', quantile*soln[ti, pool])
#                if soln[ti, pool] == 0: 
#                    #print('return nan')
#                    return np.nan
#
#                def g(a):
#                    res = quantile*soln[ti, pool]-F_sv(a, times[ti])[pool]
#                    #print('a:', a, 'g(a):', res)
#                    return res
#    
#                start_age = start_values[ti, pool]
#                
#                if method == 'newton': a_star = newton(g, start_age, maxiter=500, tol = tol)
#                #if method == 'bisect': a_star = generalized_inverse_CDF(lambda a: F_sv(a, times[ti])[pool], quantile*soln[ti, pool], start_dist=start_age, method_f=bisect)
#                if method == 'brentq': a_star = generalized_inverse_CDF(lambda a: F_sv(a, times[ti])[pool], quantile*soln[ti, pool], start_dist=start_age, tol = tol)
#                
#
#                #print('---')
#                #print(a_star)
#                return a_star
#
#            return np.array([quantile_at_ti_in_pool(ti, pool) for pool in range(n)])
#
#        m = len(times)
#        #q_lst = [quantile_at_ti(ti) for ti in range(m)]
#
#        q_lst = []
#        for ti in tqdm(range(m)):
#            q_lst.append(quantile_at_ti(ti))
#
#        q_arr = np.array(q_lst)
#        return np.ndarray((len(times),n), np.float, q_arr)

    
    def pool_age_distributions_quantiles(self, quantile, start_values = None, start_age_densities = None, F0 = None, method = 'brentq', tol = 1e-8):
        n = self.nr_pools
        soln = self.solve()
        if soln[0,:].sum() == 0:
            start_age_densities = lambda a: np.zeros((n,))

        if F0 is None and start_age_densities is None:
            raise(Exception('Either F0 or start_age_densities must be given.'))

        times = self.times

        if start_values is None:
            start_values = np.ones((len(times), n))

        F_sv = self.cumulative_pool_age_distributions_single_value(start_age_densities=start_age_densities, F0=F0)
        soln = self.solve()

        res = []
        for pool in range(n):
            print('Pool:', pool)
            F_sv_pool = lambda a, t: F_sv(a,t)[pool]
            res.append(self.distribution_quantiles(quantile,
                                                   F_sv_pool,
                                                   norm_consts = soln[:,pool],
                                                   start_values = start_values[:,pool],
                                                   method = method,
                                                   tol = tol))

        return np.array(res).transpose()

    
    def system_age_distribution_quantiles(self, quantile, start_values = None, start_age_densities = None, F0 = None, method = 'brentq', tol = 1e-8):
        n = self.nr_pools
        soln = self.solve()
        if soln[0,:].sum() == 0:
            start_age_densities = lambda a: np.zeros((n,))

        if F0 is None and start_age_densities is None:
            raise(Exception('Either F0 or start_age_densities must be given.'))
        
        F_sv = self.cumulative_system_age_distribution_single_value(start_age_densities=start_age_densities, F0=F0)
        soln = self.solve()
        start_age_moments = self.moments_from_densities(1, start_age_densities)
        
        if start_values is None: start_values = self.system_age_moment(1, start_age_moments)
        a_star = self.distribution_quantiles(quantile, F_sv, norm_consts = soln.sum(1), start_values=start_values, method=method, tol=tol)

        return a_star


    def distribution_quantiles(self, quantile, F_sv, norm_consts = None, start_values = None,  method = 'brentq', tol = 1e-8):
        times = self.times
        
        if start_values is None:
            start_values = np.zeros((times,))

        if norm_consts is None:
            norm_consts = np.ones((times,))

        def quantile_at_ti(ti):
            #print('ti', ti)
            if norm_consts[ti] == 0: return np.nan

            def g(a):
                if np.isnan(a): return np.nan
                res =  quantile*norm_consts[ti] - F_sv(a, times[ti])
                #print('a:', a,'t', times[ti], 'g(a):', res, 'nc', norm_consts[ti], 'F_sv', F_sv(a, times[ti]))
                return res

            start_age = start_values[ti]
            
            if method == 'newton': a_star = newton(g, start_age, maxiter=500, tol=tol)
            if method == 'brentq': a_star = generalized_inverse_CDF(lambda a: F_sv(a, times[ti]), quantile*norm_consts[ti], start_dist=start_age, tol=tol)

            return a_star

        m = len(times)
        #q_lst = [quantile_at_ti(ti) for ti in range(len(times))]

        q_lst = []
        for ti in tqdm(range(len(times))):
            q_lst.append(quantile_at_ti(ti))

        return np.array(q_lst)


    ## by ode ##


    def pool_age_distributions_quantiles_by_ode(self, quantile, start_age_densities = None, F0 = None, tol = 1e-8):
        res = []
        for pool in range(self.nr_pools):
            print('Pool:', pool)
            res.append(self.pool_age_distribution_quantiles_pool_by_ode(quantile, 
                                                              pool,
                                                              start_age_densities=start_age_densities,
                                                              F0=F0,
                                                              tol=tol))

        return np.array(res).transpose()


    def pool_age_distribution_quantiles_pool_by_ode(self, quantile, pool, start_age_densities = None, F0 = None, tol = 1e-8):
        soln = self.solve()
        empty = soln[0, pool] == 0

        if not empty and F0 is None and start_age_densities is None:
            raise(Exception('Either F0 or start_age_densities must be given.'))
        
        times = self.times
        n = self.nr_pools

        if not empty and F0 is None:
            p0 = start_age_densities
            F0 = lambda a: np.array([quad(lambda s: p0(s)[i], 0, a)[0] for i in range(n)])
        
        p = self.pool_age_densities_single_value(start_age_densities)
        u = self.external_input_vector_func()
        F = self.cumulative_pool_age_distributions_single_value(start_age_densities=start_age_densities, F0=F0)
        sol_funcs = self.solve_single_value()

        # find last time index such that the pool is empty --> ti
        ti = len(times)-1
        content = soln[ti, pool]
        while (content > 0) and (ti > 0): 
            ti = ti-1
            content = soln[ti, pool]
        
        if content == 0: ti += 1
        if (ti == len(times)): return np.nan*np.ones((len(times),))
  
        if ti == 0:
            sv = generalized_inverse_CDF(lambda a: F0(a)[pool], quantile*self.start_values[pool])
        else:
            #if start_age_densities is None:
            #    raise(Exception('Cannot start delayed quantile computation, since start_age_densities are missing.'))
            CDFs = self.cumulative_pool_age_distributions_single_value(start_age_densities)
            CDF = lambda a: CDFs(a, times[ti])
            sv = generalized_inverse_CDF(lambda a: CDF(a)[pool], quantile*soln[ti, pool])

        times = times[ti:]

        t_max = times[-1]
        t_min = times[0]
        pb = tqdm(total = t_max-t_min)

        global last_t, last_res
        last_t = -1
        last_res = -1.0

        def rhs(y, t_val):
            #print('y', y, 't', t_val)
            y = np.float(y)
            global last_t, last_res
            
            t_val = min(t_val, t_max)
            
            # rhs will be called twice with the same value apparently,  
            # we can use this to speed it up
            if t_val == last_t: return last_res

            if (t_val <= t_max) and (t_val-t_min-pb.n > 0):
                #pb.n = t_val-t_min
                #pb.update(0)
                pb.update(t_val-t_min-pb.n)

            #print('y', y, 't', t_val)
        
            p_val = p(y, t_val)[pool]
            u_val = u(t_val)[pool]
            F_vec = F(y, t_val).reshape((n,1))
            x_vec = sol_funcs(t_val).reshape((n,1))
            A = self.A(t_val)

            #print('A', A)
            #print('x', x_vec)
            #print('A*x', A.dot(x_vec))
            #print('p', p_val)
            #print('u', u_val)
            #print('F', F_vec)
            #print('A*F', A.dot(F_vec))
            #print(A.dot(F_vec)[pool])
            #print(A.dot(F_vec)[1])

            if p_val == 0:
                raise(Exception('Division by zero during quantile computation.'))
            else:
                res = 1 + 1/p_val*(u_val*(quantile-1.0)+quantile*(A.dot(x_vec))[pool]-(A.dot(F_vec))[pool])
            #print('res', res)
            #print('---')

            last_t = t_val
            last_res = res
            return res

        short_res = odeint(rhs, sv, times, atol=tol, mxstep=10000)
        pb.close()

        res = np.ndarray((len(self.times),))
        res[:ti] = np.nan
        res[ti:] = short_res.reshape((len(times),))

        #print(res)
        return res


    def system_age_distribution_quantiles_by_ode(self, quantile, start_age_densities = None, F0 = None, tol = 1e-8):
        soln = self.solve()
        # check if system is empty at the beginning,
        # if so, then we use 0 as start value, otherwise
        # we need to compute it from F0 (preferably) or start_age_density
        empty = soln[0,:].sum() == 0

        if not empty and F0 is None and start_age_densities is None:
            raise(Exception('Either F0 or start_age_densities must be given.'))
        
        times = self.times
        original_times = times
        n = self.nr_pools

        if not empty and F0 is None:
            p0 = start_age_densities
            F0 = lambda a: np.array([quad(lambda s: p0(s)[pool], 0, a)[0] for pool in range(n)])
        
        p = self.system_age_density_single_value(start_age_densities)

        u = self.external_input_vector_func()
        F = self.cumulative_pool_age_distributions_single_value(start_age_densities=start_age_densities, F0=F0)
        sol_funcs =self.solve_single_value()

        # find last time index such that the system is empty --> ti
        ti = len(times)-1
        content = soln[ti,:]
        while (content.sum() > 0) and (ti > 0): 
            ti = ti-1
            content = soln[ti,:]
        
        if content.sum() == 0: ti += 1
        if (ti == len(times)): return np.nan*np.ones((len(times),))
  
        if ti == 0:
            sv = generalized_inverse_CDF(lambda a: F0(a).sum(), quantile*self.start_values.sum())
        else:
            #if start_age_densities is None:
            #    raise(Exception('Cannot start delayed quantile computation, since start_age_Densities are missing.'))
            CDFs = self.cumulative_system_age_distribution_single_value(start_age_densities)
            CDF = lambda a: CDFs(a, times[ti])
            sv = generalized_inverse_CDF(CDF, quantile*soln[ti,:].sum())

        times = times[ti:]

        t_max = times[-1]
        t_min = times[0]
        pb = tqdm(total = t_max-t_min)

        global last_t, last_res
        last_t = -1
        last_res = -1.0

        def rhs(y, t_val):
            y = np.float(y)
            global last_t, last_res
            
            t_val = min(t_val, t_max)

            # rhs will be called twice with the same value apparently,  
            # we can use this to speed it up
            if t_val == last_t: return last_res

            if (t_val <= t_max) and (t_val-t_min-pb.n > 0):
                #pb.n = t_val-t_min
                #pb.update(0)
                pb.update(t_val-t_min-pb.n)

            #pb.update(t_val-t_min, n=0)
            #print()
            #print('y', y, 't', t_val)
        
            p_val = p(y, t_val)
            u_vec = u(t_val)
            F_vec = F(y, t_val).reshape((n,1))
            x_vec = sol_funcs(t_val).reshape((n,1))
            A = self.A(t_val)

            #print('A', A)
            #print('x', x_vec)
            #print('A*x', A.dot(x_vec))
            #print('p', p_val)
            #print('u', u_vec)
            #print('F', F_vec)
            #print('A*F', A.dot(F_vec))

            #print(F_val/x_val.sum()*((A*x_val).sum()-(A*F_val).sum()))
            if p_val == 0:
                raise(Exception('Division by zero during quantile computation.'))
            else:
                res = 1 + 1/p_val*(u_vec.sum()*(quantile-1.0)+quantile*(A.dot(x_vec)).sum()-(A.dot(F_vec)).sum())
            #print('res', res)

            last_t = t_val
            last_res = res
            return res

        short_res = odeint(rhs, sv, times, atol=tol, mxstep=10000)
        pb.close()

        res = np.ndarray((len(original_times),))
        res[:ti] = np.nan
        res[ti:] = short_res.reshape((len(times),))

        #print(res)
        return res


#    def system_age_distribution_quantiles(self, quantile, start_mean_ages, start_age_densities = None, F0 = None,  method = 'newton', tol = 1e-8, parallel = False):
#        if F0 is None and start_age_densities is None:
#            raise(Exception('Either F0 or start_age_densities must be given.'))
#
#        times = self.times
#        sys_soln = self.solve().sum(1)
#
#        msa = self.system_age_moment(1, start_mean_ages.reshape((1,self.nr_pools)))
#        F_sv = self.cumulative_system_age_distribution_single_value(start_age_densities, F0)
#
#        def quantile_at_ti(ti):
#            if sys_soln[ti] == 0: return np.nan
#
#            def g(a):
#                return quantile*sys_soln[ti] - F_sv(a, times[ti])
#
#            start_age = msa[ti]
#
#            if method == 'newton': a_star = newton(g, start_age, maxiter=500, tol = tol)
#            if method == 'brentq': a_star = generalized_inverse_CDF(lambda a: F_sv(a, times[ti]), quantile*sys_soln[ti], start_dist=start_age, tol = tol)
#
#            return a_star
#
#        m = len(times)
#        if parallel:
#            pool = DPool(nr_processes())
#            q_lst = list(tqdm(pool.imap(quantile_at_ti, range(m)), total = m))
#            pool.close()
#        else:
#            q_lst = [quantile_at_ti(ti) for ti in range(len(times))]
#
#        return np.array(q_lst)


    ########## private methods #########


    def _solve_age_moment_system_single_value(self, max_order, start_age_moments = None, start_values = None):
        t0 = self.times[0]
        t_max = self.times[-1]

        def func(t):
            if t < t0:
                # times x pools 
                res = np.zeros((1, self.nr_pools))
                res[res==0] = np.nan
                return res
            
            #fixme: do we really want to cut off here? 
            if t > t_max: t = t_max

            new_times = [t0, t]
            soln = self._solve_age_moment_system(max_order, start_age_moments, times = new_times, start_values = start_values)

            return soln[-1]

        return func 


    def _solve_age_moment_system(self, max_order, start_age_moments = None, times = None, start_values = None, store = True):
        store = True
        if not ((times is None) and (start_values is None)): store = False

        if times is None: 
            times = self.times

        if start_values is None: start_values = self.start_values

        if not(isinstance(start_values, np.ndarray)):
            #print(start_values)
            raise(Exception("start_values should be a numpy array"))

        n = self.nr_pools
        if start_age_moments is None:
            start_age_moments = np.zeros((max_order, n))
        
        start_age_moments_list = flatten([a.tolist() for a in 
                            [start_age_moments[i,:] for i in range(start_age_moments.shape[0])]])
       
        storage_key = tuple(start_age_moments_list) + ((max_order,),)

        # return cached result if possible
        if store:
            if hasattr(self, "_previously_computed_age_moment_sol"):
                if storage_key in self._previously_computed_age_moment_sol.keys():
                    #print('using cached age moment system:', storage_key)
                    #print(self._previously_computed_age_moment_sol[storage_key])
                    return self._previously_computed_age_moment_sol[storage_key]
            else:
                self._previously_computed_age_moment_sol = {}

        srm = self.model
        state_vector, rhs = srm.age_moment_system(max_order)
       
        # compute solution
        new_start_values = np.zeros((n*(max_order+1),))
        new_start_values[:n] = np.array((start_values)).reshape((n,)) 
        new_start_values[n:] = np.array((start_age_moments_list))

        soln = numsol_symbolic_system(
            state_vector,
            srm.time_symbol,
            rhs,
            self.parameter_set,
            self.func_set,
            new_start_values, 
            times
        )
        
        # save all solutions for order <= max_order
        if store:
            for order in range(max_order+1):
                shorter_start_age_moments_list = start_age_moments_list[:order*n]
                #print(start_age_moments_list)
                #print(shorter_start_age_moments_list)
                storage_key = tuple(shorter_start_age_moments_list) + ((order,),)
                #print('saving', storage_key)

                self._previously_computed_age_moment_sol[storage_key] = soln[:,:(order+1)*n]
                #print(self._previously_computed_age_moment_sol[storage_key])

        return soln


    #fixme: test
    @property
    def _no_input_sol(self):
        if not hasattr(self, '_saved_no_input_sol'):
            m = self.model
            m_no_inputs = SmoothReservoirModel(
                    m.state_vector,
                    m.time_symbol,
                    {},
                    m.output_fluxes,
                    m.internal_fluxes)
            
            no_inputs_num_rhs = numerical_rhs(
                m_no_inputs.state_vector, 
                m_no_inputs.time_symbol, 
                m_no_inputs.F, 
                self.parameter_set,
                self.func_set,
                self.times)
    
            def no_input_sol(times, start_vector):
                #print('nos', times, start_vector)
                # Start and end time too close together? Do not integrate!
                if abs(times[0]-times[-1]) < 1e-14: return np.array(start_vector)
                sv = np.array(start_vector).reshape((self.nr_pools,))
                return odeint(no_inputs_num_rhs, sv, times, mxstep = 10000)[-1]
        
            self._saved_no_input_sol = no_input_sol

        return self._saved_no_input_sol


    #fixme: test
    def build_state_transition_operator_cache(self, size = 101):
        if size < 2:
            raise(Exception('Cache size must be at least 2'))

        times = self.times
        n = self.nr_pools
        t_min = times[0]
        t_max = times[-1]
        nc = size
        cached_times = np.linspace(t_min, t_max, nc)

        # build cache
        print("creating cache")
        ca = np.ndarray((nc, nc, n, n))
        ca = np.zeros((nc, nc, n, n)) 
        no_input_sol = self._no_input_sol

        for tm1_index in tqdm(range(nc-1)):
            tm1 = cached_times[tm1_index]
            sub_cached_times = np.linspace(tm1, t_max, nc)

            for i in range(n):
                e_i = np.zeros((n,1))
                e_i[i] = 1
                #ca[tm1_index,:,:,i] = no_input_sol(sub_cached_times, e_i) # leads to zig-zag functions, 
                # the ends do not fit together
                sv = e_i
                st = tm1
                for j in range(len(sub_cached_times)):
                    new_sv = no_input_sol([st, sub_cached_times[j]], sv)
                    ca[tm1_index,j,:,i] = new_sv.reshape((n,))
                    sv = new_sv
                    st = sub_cached_times[j]

        print("cache created")

        self._state_transition_operator_values = ca
        self._cache_size = size


    def save_state_transition_operator_cache(self, filename):
        cache = {'values': self._state_transition_operator_values,
                 'size': self._cache_size,
                 'times': self.times}
        
        with open(filename, 'wb') as output:
            pickle.dump(cache, output)


    def load_state_transition_operator_cache(self, filename):
        with open(filename, 'rb') as output:
            cache = pickle.load(output)
    
        if not np.all(self.times == cache['times']):
            raise(Exception('The cached state transition operator does not correspond to the current setting.'))

        self._state_transition_operator_values = cache['values']
        self._cache_size = cache['size']


    def _state_transition_operator(self, t, t0, x):
        if t0 > t:
            raise(Exception("Evaluation before t0 is not possible"))
        if t0 == t:
            return x
       
        n = self.nr_pools
        no_input_sol = self._no_input_sol

        if self._state_transition_operator_values is None:
            # do not use the cache, it has not yet been created
            #self.build_state_transition_operator_cache()
            soln = (no_input_sol([t0, t], x)).reshape((n,))        
        else:
            # use the already created cache
            times = self.times
            t_min = times[0]
            t_max = times[-1]
            nc = self._cache_size
    
            cached_times = np.linspace(t_min, t_max, nc)
            ca = self._state_transition_operator_values
    
            # find tm1
            tm1_ind = cached_times.searchsorted(t0)
            tm1 = cached_times[tm1_ind]
    
            # check if next cached time is already behind t
            if t <= tm1: return no_input_sol([t0, t], x)
    
            # first integrate x to tm1: y = Phi(tm1, t_0)x
            y = (no_input_sol([t0, tm1], x)).reshape((n,1))
    
            step_size = (t_max-tm1)/(nc-1)
            if step_size > 0:
                tm2_ind = np.int(np.min([np.floor((t-tm1)/step_size), nc-1]))
                tm2 = tm1 + tm2_ind*step_size
    
                #print(t, t0, t==t0, tm1_ind, tm1, tm2_ind, tm2, step_size) 
                B = ca[tm1_ind,tm2_ind,:,:]
                #print(t, t0, tm1, tm2, step_size, B)
                
                z = np.dot(B, y)
            else:
                tm2 = tm1
                z = y
            #z = (no_input_sol([tm1, tm2], y)[-1]).reshape((n,))
    
            # integrate z to t: sol=Phi(t,tm2)*z
            soln = (no_input_sol([tm2, t],z)).reshape((n,))
    
        return soln
        

    def _flux_vector(self, flux_vec_symbolic):
        sol = self.solve()
        srm = self.model
        n = self.nr_pools
        times = self.times
        
        tup = tuple(srm.state_vector) + (srm.time_symbol,)
        res = np.zeros((len(times), n))
        
        flux_vec_symbolic = sympify(flux_vec_symbolic, locals = _clash)
        flux_vec_symbolic = flux_vec_symbolic.subs(self.parameter_set)
        cut_func_set = {key[:key.index('(')]: val for key, val in self.func_set.items()}
        flux_vec_fun = lambdify(tup, flux_vec_symbolic, modules=[cut_func_set, 'numpy'])

        res = np.zeros((len(times), n))
        for ti in range(len(times)):
            args = [sol[ti, pool] for pool in range(n)] + [times[ti]]
            val = flux_vec_fun(*args)
            res[ti,:] = val.reshape((n,))

        return res


    ##### age density methods #####


    def _age_densities_1_single_value(self, start_age_densities = None):
        # for part that comes from initial value
        if start_age_densities is None:
            # all mass is assumed to have age 0 at the beginning
            def start_age_densities(a):
                if a != 0: return np.array((0,)*self.nr_pools)
                return np.array(self.start_values)

        # cut off negative ages in start_age_densities
        p0 = lambda a: start_age_densities(a) if a>=0 else np.zeros((self.nr_pools,))
        Phi = self._state_transition_operator
 
        t0 = self.times[0]

        #ppp = lambda a, t: self._state_transition_operator(t,t0,p0(a-(t-t0)))
        def ppp(a, t):
            #print('iv: ', a, t)

            #fixme: cut off accidental negative values
            #print('Y', a-(t-t0), p0(a-t-t0))
            res = np.maximum(Phi(t, t0, p0(a-(t-t0))), 0)
            #print('ppp:', res)
            return res

        return ppp

    
    # return a function p1 that takes an age np.array
    # and gives back an nd array (age, time, pool)
    def _age_densities_1(self, start_age_densities = None):
        # for part that comes from initial value

        ppp = self._age_densities_1_single_value(start_age_densities)
        pp = lambda a: np.array([ppp(a,t) for t in self.times], np.float)
        p1 = lambda ages: np.array([pp(a) for a in ages], np.float)
        
        return p1

        
    def _age_densities_2_single_value(self):
        # for part that comes from the input function u
       
        t0 = self.times[0]
        u = self.external_input_vector_func()
        #u = lambda x: np.array([1,2])

        def ppp(a, t):
            #print('input', a, t)
            if (a < 0) or (t-t0 <= a):
                val = np.zeros((1,self.nr_pools))[-1]
            else:
                u_val = u(t-a)
                #print('u_val', u_val)
                val = self._state_transition_operator(t, t-a, u_val)

            #fixme: cut off accidental negative values
            res = np.maximum(val, 0)
            #print('ppp:', res)
            return res

        return ppp
    

    # returns a function p2 that takes an age array "ages" as argument
    # and gives back a three-dimensional ndarray (ages x times x pools)
    def _age_densities_2(self):
        # for part that comes from the input function u
        ppp = self._age_densities_2_single_value()
        pp = lambda a: np.array([ppp(a,t) for t in self.times], np.float)
        p2 = lambda ages: np.array([pp(a) for a in ages], np.float)

        return p2


    ##### plotting methods #####
    
    
    def _density_plot_plotly(self, field, ages, age_stride = 1, time_stride = 1):
        times = self.times

        strided_field = stride(field, (age_stride, time_stride))
        strided_ages = stride(ages, age_stride)
        strided_times = stride(times, time_stride)
 
        surfacecolor = strided_field.copy()
        for ai in range(strided_field.shape[0]):
            for ti in range(strided_field.shape[1]):
                surfacecolor[ai,ti] = - (ai - ti)
        
        data = [go.Surface(x = -strided_times, 
                           y = strided_ages, 
                           z = strided_field, 
                           showscale=False, surfacecolor = surfacecolor, colorscale = 'Rainbow')]
        
        tickvals = np.linspace(strided_times[0], strided_times[-1], 5)
        ticktext = [str(v) for v in tickvals]
        tickvals = -tickvals
        
        layout = go.Layout(
            width = 800,
            height = 800,
            scene = dict(
                xaxis = dict(
                    title = 'Time',
                    tickmode = 'array',
                    tickvals = tickvals,
                    ticktext = ticktext
                    #range = [-times[0], -times[-1]]
                ),
                yaxis = dict(
                    title = 'Age',
                    range = [ages[0], ages[-1]]
                ),
                zaxis = dict(
                    title = 'Mass',
                    range = [0, np.amax(strided_field)]
                )
            )
        )

        return data, layout


    ## plot helper methods ##


    def _add_time_unit(self, label):
        if self.model.time_unit:
            label += r"$\quad(\mathrm{" + latex(self.model.time_unit) + "})$"

        return label


    def _add_content_unit(self, label):
        if self.model.content_unit:
            label += r"$\quad(\mathrm{" + latex(self.model.content_unit) + "})$"

        return label


    def _add_flux_unit(self, label):
        if self.model.content_unit and self.model.time_unit:
            label += r"$\quad(\mathrm{" + latex(self.model.content_unit) + "/" + latex(self.model.time_unit) + "})$"
        
        return label


    
