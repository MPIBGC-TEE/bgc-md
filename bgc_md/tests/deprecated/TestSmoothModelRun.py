#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:

from concurrencytest import ConcurrentTestSuite, fork_for_tests
import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np
import sys 
from scipy.misc import factorial
from scipy.interpolate import interp1d 
from sympy import sin, symbols, Matrix, Symbol, exp, solve, Eq, pi, Piecewise, Function

import bgc_md.tests.exampleSmoothReservoirModels as ESRM
import bgc_md.tests.exampleSmoothModelRuns as ESMR

from testinfrastructure.InDirTest import InDirTest
from bgc_md.SmoothReservoirModel import SmoothReservoirModel  
from bgc_md.SmoothModelRun import SmoothModelRun 


class TestSmoothModelRun(InDirTest):
        
    def test_init(self):
        #create a valid model run complete with start ages
        symbs = symbols("x,k,t")
        x, t, k = symbs 
        srm = ESRM.minimal(symbs) 
        times = np.linspace(0, 20, 1600)
        start_values = np.array([10])
        pardict = {k: 1}
        smr = SmoothModelRun(srm, pardict, start_values, times)
        self.assertEqual(smr.start_values, start_values)
        self.assertTrue(all(smr.times==times))
        
        #create a valid model run without start ages
        smr = SmoothModelRun(srm, pardict, start_values, times=times)
        #check if we can retrieve values back 
        #(although this looks too simple there was an error here)
        self.assertEqual(smr.start_values, start_values)
        self.assertTrue(all(smr.times==times))
       
        #fixme: 
        #check for incomplete param set...to be implemented
        # --> implemented in Model.py

    
    def test_linearize(self):
        # Atmosphere, Terrestrial Carbon and Surface layer
        C_A, C_T, C_S = symbols('C_A C_T C_S')
        
        # equilibrium contents
        A_e, T_e, S_e = symbols('A_e T_e S_e')
        
        # equilibrium fluxes
        F_0, F_1, F_2 = symbols('F_0 F_1 F_2')
        
        # nonlinear coefficients
        alpha, beta = symbols('alpha beta')
        
        # external flux from surface layer to deep ocean
        F_ex = F_0*C_S/S_e
        
        # fossil fuel inputs
        u_A = symbols('u_A')
        
        #########################################
        
        state_vector = Matrix([C_A, C_T, C_S])
        time_symbol = symbols('tau')
        
        input_fluxes = {0: u_A, 1: 0, 2: F_0}
        output_fluxes = {0: 0, 1: 0, 2: F_0*C_S/S_e}
        internal_fluxes = {(0,1): F_2*(C_A/A_e)**alpha, # A --> T
                           (0,2): F_1*C_A/A_e,          # A --> S
                           (1,0): F_2*C_T/T_e,          # T --> A
                           (2,0): F_1*(C_S/S_e)**beta}  # S --> A

        nonlinear_srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)
        
        A_eq, T_eq, S_eq = (700.0, 3000.0, 1000.0) 
        par_dict = {  A_e: A_eq,  T_e:  T_eq, S_e: S_eq, # equilibrium contents in Pg
                      F_0: 45.0,  F_1: 100.0, F_2: 60.0, # equilibrium fluxes in PgC/yr
                    alpha:  0.2, beta:  10.0           } # nonlinear coefficients
        
        # fossil fuel inputs
        par_dict[u_A] = 0
        
        # initialize model run 
        times = np.linspace(0, 10, 101)
        start_values = np.array([A_eq, T_eq, S_eq])
        nonlinear_smr = SmoothModelRun(nonlinear_srm, par_dict, start_values, times)
      
        linearized_smr = nonlinear_smr.linearize()
        #print(linearized_srm.F)
        soln = linearized_smr.solve()
        # system is in steady state, so the linearized solution
        # should stay constant
        self.assertTrue(np.allclose(soln[-1], start_values))


    def test_linearize_piecewise(self):
        # Atmosphere, Terrestrial Carbon and Surface layer
        C_A, C_T, C_S = symbols('C_A C_T C_S')
        
        # equilibrium contents
        A_e, T_e, S_e = symbols('A_e T_e S_e')
        
        # equilibrium fluxes
        F_0, F_1, F_2 = symbols('F_0 F_1 F_2')
        
        # nonlinear coefficients
        alpha, beta = symbols('alpha beta')
        
        # external flux from surface layer to deep ocean
        F_ex = F_0*C_S/S_e
        
        # fossil fuel inputs
        u_A = symbols('u_A')
        
        
        #########################################
        
        state_vector = Matrix([C_A, C_T, C_S])
        time_symbol = symbols('tau')
        
        input_fluxes = {0: u_A, 1: 0, 2: F_0}
        output_fluxes = {0: Piecewise((1, time_symbol < 0), (0, True)), 1: 0, 2: F_0*C_S/S_e}
        internal_fluxes = {(0,1): F_2*(C_A/A_e)**alpha, # A --> T
                           (0,2): F_1*C_A/A_e,          # A --> S
                           (1,0): F_2*C_T/T_e,          # T --> A
                           (2,0): F_1*(C_S/S_e)**beta}  # S --> A
        nonlinear_srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)
        
        A_eq, T_eq, S_eq = (700.0, 3000.0, 1000.0) 
        par_dict = {  A_e:  A_eq,  T_e:   T_eq, S_e: S_eq, # equilibrium contents in Pg
                      F_0:  45.0,  F_1:  100.0, F_2: 60.0, # equilibrium fluxes in PgC/yr
                    alpha:   0.2, beta:   10.0           } # nonlinear coefficients
        
        
        # fossil fuel inputs
        par_dict[u_A] = 0
        
        # initialize model run 
        times = np.linspace(0, 10, 101)
        start_values = np.array([A_eq, T_eq, S_eq])
        nonlinear_smr = SmoothModelRun(nonlinear_srm, par_dict, start_values, times)
       
        linearized_smr = nonlinear_smr.linearize()
        #print(linearized_srm.F)
        soln = linearized_smr.solve()
        # system is in steady state, so the linearized solution
        # should stay constant
        self.assertTrue(np.allclose(soln[-1], start_values))


    def test_moments_from_densities(self):
        # two_dimensional
        start_values = np.array([1,2])
        def start_age_densities(a):
            p1 = np.exp(-a) * start_values[0]
            p2 = 2*np.exp(-2*a) * start_values[1]
        
            return np.array([p1, p2])

        max_order = 5
        moments = SmoothModelRun.moments_from_densities(max_order, start_age_densities)

        ref1 = np.array([factorial(n)/1**n for n in range(1, max_order+1)])
        ref2 = np.array([factorial(n)/2**n for n in range(1, max_order+1)]) 
        ref = np.array([ref1, ref2]).transpose()

        self.assertTrue(np.allclose(moments, ref))

        # test empty pool
        start_values = np.array([0,2])
        def start_age_densities(a):
            p1 = np.exp(-a) * start_values[0]
            p2 = 2*np.exp(-2*a) * start_values[1]
        
            return np.array([p1, p2])

        max_order = 1
        moments = SmoothModelRun.moments_from_densities(max_order, start_age_densities)
        self.assertTrue(np.isnan(moments[0,0]))


    ########## public methods and properties ########## 
             
    
    def test_solve_symbolic(self):
        x, y, t = symbols("x y t")
        state_vector = Matrix([x,y])
        A = Matrix([[-1, 0],
                    [ 0,-2]])
        u = Matrix(2, 1, [0,1])
        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)
        smr = SmoothModelRun(srm, parameter_set={}, start_values=np.array([1,1]), times=np.linspace(0,1,10))
        a_ref = np.array([[ 1.        ,  1.        ], 
                          [ 0.89483932,  0.90036872],
                          [ 0.80073741,  0.82059019],
                          [ 0.71653131,  0.75670858],
                          [ 0.64118039,  0.70555616],
                          [ 0.57375342,  0.66459652],
                          [ 0.51341712,  0.63179857],
                          [ 0.45942583,  0.60553604],
                          [ 0.41111229,  0.58450666],
                          [ 0.36787944,  0.56766764]])
        ref = np.ndarray((10,2), np.float, a_ref)
        soln = smr.solve()
        self.assertTrue(np.allclose(soln, ref))
    

    def test_solve_semi_symbolic_piecewise(self):
        # test semi-symbolic semi-numerical SmoothReservoirModel
        C_0, C_1, C_2 = symbols('C_0 C_1 C_2')
        lambda_0 = Symbol('lambda_0')
        t = Symbol('t')
        u_0_expr = Function('u_0')(C_0, C_1, t)
        u_2_expr = Function('u_2')(t)

        X = Matrix([C_0, C_1, C_2])
        t_min,t_max = 0,10
        u_data_0 = np.array([[ t_min ,  0.1], [ t_max ,  0.2]])
        u_data_2 = np.array([[ t_min ,  0.4], [ t_max ,  0.5]])
        input_fluxes = {0: u_data_0, 2: u_data_2}

        symbolic_input_fluxes = {0: u_0_expr, 2: u_2_expr}
        
        u_0_interp = interp1d(u_data_0[:,0], u_data_0[:,1])
        def u0_func(C_0_val, C_1_val, t_val):
            return C_0_val + C_1_val + u_0_interp(t_val)
        
        u_1_interp = interp1d(u_data_2[:,0], u_data_2[:,1])
        def u2_func(t_val):
            return u_1_interp(t_val)

        func_set = {u_0_expr: u0_func, u_2_expr: u2_func}
        
        output_fluxes = {0:Piecewise((lambda_0*C_0,t<t_max/2),(10*lambda_0*C_0,True))}
        internal_fluxes = {(0,1): 5*C_0, (1,0): 4*C_1**2}
        srm = SmoothReservoirModel(
            X, 
            t, 
            symbolic_input_fluxes, 
            #{0: 1, 2: 1},
            output_fluxes, 
            internal_fluxes
        )

        start_values = np.array([1, 2, 3])
        times = np.linspace(t_min,t_max, 11)
        smr = SmoothModelRun(srm, parameter_set={lambda_0:.2}, start_values=start_values, times=times,func_set=func_set)
        
        soln = smr.solve()


    def test_solve_semi_symbolic(self):
        # test semi-symbolic semi-numerical SmoothReservoirModel
        C_0, C_1, C_2 = symbols('C_0 C_1 C_2')
        t = Symbol('t')

        u_0_expr = Function('u_0')(C_0, C_1, t)
        u_2_expr = Function('u_2')(t)

        X = Matrix([C_0, C_1, C_2])
        t_min, t_max = 0, 10
        u_data_0 = np.array([[ t_min ,  0.1], [ t_max ,  0.2]])
        u_data_2 = np.array([[ t_min ,  0.4], [ t_max ,  0.5]])
        input_fluxes = {0: u_data_0, 2: u_data_2}
        symbolic_input_fluxes = {0: u_0_expr, 2: u_2_expr}
        
        u_0_interp = interp1d(u_data_0[:,0], u_data_0[:,1])
        def u0_func(C_0_val, C_1_val, t_val):
            return C_0_val*0 + C_1_val*0 + u_0_interp(t_val)
        
        u_1_interp = interp1d(u_data_2[:,0], u_data_2[:,1])
        def u2_func(t_val):
            return u_1_interp(t_val)
        
        func_set = {u_0_expr: u0_func, u_2_expr: u2_func}
        
        output_fluxes = {}
        internal_fluxes = {(0,1): 5*C_0, (1,0): 4*C_1**2}
        srm = SmoothReservoirModel(
            X, 
            t, 
            symbolic_input_fluxes, 
            output_fluxes, 
            internal_fluxes
        )

        start_values = np.array([1, 2, 3])
        times = np.linspace(t_min,t_max, 11)
        smr = SmoothModelRun(srm, parameter_set={}, start_values=start_values, times=times,func_set=func_set)
        
        soln = smr.solve()


    ##### fluxes as functions #####


    def test_flux_funcs(self):
        # one-dimensional case, check that constant values do not lead
        # to problems like 1.subs({...})
        C = Symbol('C')
        state_vector = [C]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1}
        output_fluxes = {0: C}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)
        
        u = smr.external_input_flux_funcs()
        self.assertEqual(u[0](0.5), 1)
        

    def test_output_vector_func(self):
        # two-dimensional case
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1,3])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        self.assertTrue(np.allclose(smr.output_vector_func(1), np.array([0.36787945, 1.10363835])))
        

    ##### fluxes as vector-valued functions #####
    

    def test_external_input_vector_func(self):
        C_1, C_2 = symbols('C_1 C_2')
        state_vector = [C_1, C_2]
        time_symbol = Symbol('t')
        input_fluxes = {0: time_symbol, 1: 0}
        output_fluxes = {0: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5,2])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)
        
        u = smr.external_input_vector_func()
        self.assertTrue(np.allclose(u(0.5), np.array([0.5, 0])))


    ##### fluxes as vector over self.times #####


    def test_external_input_vector(self):
        # two-dimensional case
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 0.5*C_1} # even pool-dependent input
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1,3])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ref_a = np.array([[ 0.,          0.        ], # input starts right after t0
                          [ 1.,          1.42684416],
                          [ 1.,          1.35725616],
                          [ 1.,          1.29106198],
                          [ 1.,          1.22809615],
                          [ 1.,          1.16820118],
                          [ 1.,          1.11122731],
                          [ 1.,          1.05703214],
                          [ 1.,          1.00548009],
                          [ 1.,          0.95644224],
                          [ 1.,          0.90979601]])
        ref = np.ndarray((11, 2), np.float, ref_a)
        self.assertTrue(np.allclose(smr.external_input_vector, ref))


    def test_external_output_vector(self):
        # one-dimensional case
        C_0 = symbols('C_0')
        state_vector = [C_0]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: C_0}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1])
        times = np.linspace(0, 1, 11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ref_a = np.array([[ 1.        ], 
                          [ 0.90483744],
                          [ 0.81873077],
                          [ 0.74081821],
                          [ 0.67032006],
                          [ 0.60653067],
                          [ 0.54881165],
                          [ 0.49658532],
                          [ 0.44932898],
                          [ 0.40656968],
                          [ 0.36787945]])
        ref = np.ndarray((11, 1), np.float, ref_a)
        self.assertTrue(np.allclose(smr.external_output_vector, ref))

        # two-dimensional case
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1,3])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ref_a = np.array([[ 1.        ,  3.        ], 
                          [ 0.90483744,  2.71451231],
                          [ 0.81873077,  2.4561923 ],
                          [ 0.74081821,  2.22245462],
                          [ 0.67032006,  2.01096019],
                          [ 0.60653067,  1.81959201],
                          [ 0.54881165,  1.64643494],
                          [ 0.49658532,  1.48975595],
                          [ 0.44932898,  1.34798693],
                          [ 0.40656968,  1.21970905],
                          [ 0.36787945,  1.10363835]])
        ref = np.ndarray((11, 2), np.float, ref_a)
        self.assertTrue(np.allclose(smr.external_output_vector, ref))


    ##### age density methods #####


    def test_pool_age_densities_single_value(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        start_age_densities = lambda a: np.exp(-a)*start_values
        p_sv = smr.pool_age_densities_single_value(start_age_densities)

        a1_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 5.        ,  3.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 1.83939721,  1.10363832],
                  [ 1.83939724,  1.10363834],
                  [ 1.83939725,  1.10363835],
                  [ 1.83939724,  1.10363835],
                  [ 1.83939729,  1.10363837],
                  [ 1.83939727,  1.10363836]]])

        a2_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 0.        ,  0.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ]],
                
                 [[ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ]]])

        a_ref = a1_ref + a2_ref
        ref = np.ndarray((3,6,2), np.float, a_ref)
        y = p_sv(0,0)
        res_l = [[p_sv(a, t) for t in times] for a in ages]
        res = np.array(res_l)
        self.assertTrue(np.allclose(res, ref))


    def test_age_densities(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = Matrix([C_0, C_1])
        time_symbol = Symbol('t')
        #fixme: both input anoutput should be 1, 2, C_0, C_1
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)


    def test_system_age_density_single_value(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        start_age_densities = lambda a: np.exp(-a)*start_values
        p_sv = smr.system_age_density_single_value(start_age_densities)

        a1_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 5.        ,  3.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 1.83939721,  1.10363832],
                  [ 1.83939724,  1.10363834],
                  [ 1.83939725,  1.10363835],
                  [ 1.83939724,  1.10363835],
                  [ 1.83939729,  1.10363837],
                  [ 1.83939727,  1.10363836]]])

        a2_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 0.        ,  0.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ]],
                
                 [[ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ]]])

        a_ref = a1_ref + a2_ref
        ref = np.sum(np.ndarray((3,6,2), np.float, a_ref), axis=2)
        res_l = [[p_sv(a, t) for t in times] for a in ages]
        res = np.array(res_l)
        self.assertTrue(np.allclose(res, ref))


    def test_system_age_density(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        start_age_densities = lambda a: np.exp(-a)*start_values
        p = smr.pool_age_densities_func(start_age_densities)
        age_densities = p(ages)
        system_age_density = smr.system_age_density(age_densities)

        a1_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 5.        ,  3.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 1.83939721,  1.10363832],
                  [ 1.83939724,  1.10363834],
                  [ 1.83939725,  1.10363835],
                  [ 1.83939724,  1.10363835],
                  [ 1.83939729,  1.10363837],
                  [ 1.83939727,  1.10363836]]])

        a2_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 0.        ,  0.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ]],
                
                 [[ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ]]])

        a_ref = a1_ref + a2_ref
        ref = np.sum(np.ndarray((3,6,2), np.float, a_ref), axis=2)

        self.assertTrue(np.allclose(ref, system_age_density))


    ##### age moments methods #####


    def test_age_moment_vector_from_densities(self):
        # test mean age
        x, y, t = symbols("x y t")
        state_vector = Matrix([x,y])
        A = Matrix([[-1, 0],
                    [ 0,-2]])
        u = Matrix(2, 1, [0,1])
        start_values = np.array([1,2])
        times = np.linspace(0,1,3)

        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)
        smr = SmoothModelRun(srm, parameter_set={}, start_values=start_values, times=times)

        start_age_densities = lambda a: 2*np.exp(-2*a)*start_values

        # the solution to be tested
        order = 1
        ma_from_dens = smr.age_moment_vector_from_densities(order, start_age_densities)

        # test against solution from mean age system
        start_mean_ages = [0.5,0.5]
        n = srm.nr_pools
        start_age_moments = np.ndarray((1,n), np.float, np.array(start_mean_ages))

        ref_ma = smr.age_moment_vector(1, start_age_moments)

        self.assertTrue(np.allclose(ma_from_dens, ref_ma))


    def test_age_moment_vector_semi_explicit(self):
        x, y, t = symbols("x y t")
        X = Matrix([x,y])
        u = Matrix(2, 1, [1, 2])
        srm = SmoothReservoirModel.from_A_u(X, t, Matrix([[-1,0],[0,-1]]), u)
        
        start_values = np.array([1,1])
        times = np.linspace(0, 1, 10)
        smr = SmoothModelRun(srm, {}, start_values, times)
        n = smr.nr_pools

        def start_age_densities(a):
            p1 = np.exp(-a) * start_values[0]
            p2 = 2*np.exp(-2*a) * start_values[1]
        
            return np.array([p1, p2])

        start_age_moments = smr.moments_from_densities(1, start_age_densities)

        ma_ref = smr.age_moment_vector(1, start_age_moments)
        ma_semi_explicit = smr.age_moment_vector_semi_explicit(1, start_age_moments)
        self.assertTrue(np.allclose(ma_semi_explicit, ma_ref))

        # test empty start_ages
        ma_ref = smr.age_moment_vector(1)
        ma_semi_explicit = smr.age_moment_vector_semi_explicit(1)
        self.assertTrue(np.allclose(ma_semi_explicit, ma_ref))  

        # test that nothing fails for second moment
        start_age_moments = smr.moments_from_densities(2, start_age_densities)
        smr.age_moment_vector_semi_explicit(2, start_age_moments)
        smr.age_moment_vector_semi_explicit(2)

        # test empty second pool at beginning
        x, y, t = symbols("x y t")
        X = Matrix([x,y])
        u = Matrix(2, 1, [0, 1])
        srm = SmoothReservoirModel.from_A_u(X, t, Matrix([[-1,0],[0,-1]]), u)
        
        start_values = np.array([1,0])
        times = np.linspace(0, 1, 11)
        smr = SmoothModelRun(srm, {}, start_values, times)
        n = smr.nr_pools

        def start_age_densities(a):
            p1 = np.exp(-a) * start_values[0]
            p2 = np.exp(-a) * start_values[1]
        
            return np.array([p1, p2])

        start_age_moments = smr.moments_from_densities(2, start_age_densities)

        ma_ref = smr.age_moment_vector(2, start_age_moments)
        ma_semi_explicit = smr.age_moment_vector_semi_explicit(2, start_age_moments)
        self.assertTrue(np.allclose(ma_semi_explicit, ma_ref, equal_nan=True))


    def test_age_moment_vector(self):
        x, y, t = symbols("x y t")
        state_vector = Matrix([x,y])
        A = Matrix([[-1, 0],
                    [ 0,-2]])
        u = Matrix(2, 1, [9,1])
        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)

        start_values = np.array([1,1])
        smr = SmoothModelRun(srm, {}, start_values, times=np.linspace(0,1,10))

        start_age_densities = lambda a: np.exp(-a) * start_values
        start_age_moments = smr.moments_from_densities(1, start_age_densities)
    
        # set manually mean age in first pool to zero
        start_age_moments[0,0] = 0

        ma_vec = smr.age_moment_vector(1, start_age_moments)

        a_ref = np.array([[ 0.        ,  1.        ], 
                          [ 0.08202606,  0.99407994],
                          [ 0.14256583,  0.97750078],
                          [ 0.19599665,  0.95232484],
                          [ 0.24534554,  0.92082325],
                          [ 0.29165801,  0.8852548 ],
                          [ 0.33540449,  0.84768088],
                          [ 0.37683963,  0.80984058],
                          [ 0.41612357,  0.77309132],
                          [ 0.45337056,  0.73840585]])
        ref = np.ndarray((10,2), np.float, a_ref)
        self.assertTrue(np.allclose(ma_vec, ref)) 

        # test empty initial pool, pool remains empty
        x, y, t = symbols("x y t")
        state_vector = Matrix([x,y])
        A = Matrix([[-1, 0],
                    [ 0,-2]])
        u = Matrix(2, 1, [9,0])
        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)

        start_values = np.array([1,0])
        smr = SmoothModelRun(srm, {}, start_values, times=np.linspace(0,1,10))

        start_age_densities = lambda a: np.exp(-a) * start_values
        start_age_moments = smr.moments_from_densities(1, start_age_densities)
    
        # set manually mean age in first pool to zero
        start_age_moments[0,0] = 0

        ma_vec = smr.age_moment_vector(1, start_age_moments)
        a_ref = np.array([[ 0.        , np.nan], 
                          [ 0.08202608, np.nan],
                          [ 0.14256586, np.nan],
                          [ 0.19599667, np.nan],
                          [ 0.24534558, np.nan],
                          [ 0.29165805, np.nan],
                          [ 0.33540452, np.nan],
                          [ 0.37683967, np.nan],
                          [ 0.41612361, np.nan],
                          [ 0.45337059, np.nan]])

        ref = np.ndarray((10,2), np.float, a_ref)
        self.assertTrue(np.allclose(ma_vec, ref, equal_nan=True))

        # test empty initial pool, pool receives input
        # test second moment for technical problems
        x, y, t = symbols("x y t")
        state_vector = Matrix([x,y])
        A = Matrix([[-1, 0],
                    [ 0,-2]])
        u = Matrix(2, 1, [9,1])
        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)

        start_values = np.array([1,0])
        smr = SmoothModelRun(srm, {}, start_values, times=np.linspace(0,1,10))

        start_age_densities = lambda a: np.exp(-a) * start_values
        start_age_moments = smr.moments_from_densities(2, start_age_densities)
    
        # set manually mean age in first pool to zero
        start_age_moments[0,0] = 0

        ma_vec = smr.age_moment_vector(2, start_age_moments)
        a_ref = np.array([[ 2.        ,      np.nan], 
                          [ 0.98002901,  0.00388848],
                          [ 0.64334871,  0.01466488],
                          [ 0.48944833,  0.03104518],
                          [ 0.41297607,  0.05182637],
                          [ 0.37772024,  0.07590221],
                          [ 0.36766021,  0.10227516],
                          [ 0.37445696,  0.13006409],
                          [ 0.39322901,  0.15850783],
                          [ 0.42084832,  0.18696471]])

        ref = np.ndarray((10,2), np.float, a_ref)
        self.assertTrue(np.allclose(ma_vec, ref, equal_nan=True))


    def test_system_age_moment(self):
        # create a parallel model with identical initial conditions and check that in this
        # case the pool age moments are both equal to the system age moments
        x, y, t = symbols("x y t")
        X = Matrix([x,y])
        u = Matrix([0,0])
        srm = SmoothReservoirModel.from_A_u(X, t, Matrix([[-1,0],[0,-1]]), u)

        start_values = np.array([1,1])
        smr = SmoothModelRun(srm, {}, start_values, np.linspace(0,1,10))
        n = smr.nr_pools
        
        order = 2
        start_age_densities = lambda a: np.exp(-a) * start_values
        start_age_moments = smr.moments_from_densities(order, start_age_densities)

        system_age_moment = smr.system_age_moment(order, start_age_moments)
        age_moment_vector = smr.age_moment_vector(order, start_age_moments)

        for pool in range(n):
            self.assertTrue(np.allclose(age_moment_vector[:,pool], system_age_moment))

        # test empty system and empty pools
        x, y, t = symbols("x y t")
        X = Matrix([x,y])
        u = Matrix(2, 1, [0,1])
        srm = SmoothReservoirModel.from_A_u(X, t, Matrix([[-1,0],[0,-1]]), u)

        start_values = np.array([0,0])
        smr = SmoothModelRun(srm, {}, start_values, np.linspace(0,1,10))
        n = smr.nr_pools
        
        order = 1
        start_age_densities = lambda a: np.exp(-a) * start_values
        start_age_moments = smr.moments_from_densities(order, start_age_densities)

        age_moment_vector = smr.age_moment_vector(order, start_age_moments)
        system_age_moment = smr.system_age_moment(order, start_age_moments)

        self.assertTrue(np.all(np.isnan(age_moment_vector[:,0])))
        self.assertTrue(np.isnan(age_moment_vector[0,1]))
        self.assertTrue(np.allclose(age_moment_vector[:,1], system_age_moment, equal_nan=True))


    ##### transit time density methods #####


    def test_backward_transit_time_density_single_value(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        start_age_densities = lambda a: np.exp(-a)*start_values

        p_sv = smr.backward_transit_time_density_single_value(start_age_densities)
        self.assertEqual(round(p_sv(1, 1), 4), round((5+3)*np.exp(-1), 4))


    def test_backward_transit_time_density(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        start_age_densities = lambda a: np.exp(-a)*start_values

        a1_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 5.        ,  3.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 1.83939721,  1.10363832],
                  [ 1.83939724,  1.10363834],
                  [ 1.83939725,  1.10363835],
                  [ 1.83939724,  1.10363835],
                  [ 1.83939729,  1.10363837],
                  [ 1.83939727,  1.10363836]]])

        a2_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 0.        ,  0.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ]],
                
                 [[ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ]]])

        a_ref = a1_ref + a2_ref
        
        tt_a_ref = np.array(
                 [[ 0.        ,  0.        ,  0.       ,   0.        ,  0.        ,  0.        ],
                  [ 8.        ,  3.        ,  3.       ,   3.        ,  3.        ,  3.        ],
                  [ 2.94303553,  2.94303558,  2.9430356,   2.94303559,  2.94303566,  2.94303564]])
        tt_ref = np.ndarray((3,6), np.float, tt_a_ref)

        p = smr.pool_age_densities_func(start_age_densities)
        age_densities = p(ages)
        btt_dens = smr.backward_transit_time_density(age_densities)
        self.assertTrue(np.allclose(btt_dens, tt_ref))


    def test_forward_transit_time_density_single_value(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        start_age_densities = lambda a: np.exp(-a)*start_values

        p_btt_sv = smr.backward_transit_time_density_single_value(start_age_densities)
        p_ftt_sv = smr.forward_transit_time_density_single_value()
    
        # no input at time t0 --> no forward transit time
        self.assertTrue(np.isnan(p_ftt_sv(1, 0)))

        self.assertEqual(round(p_btt_sv(0.5, 1), 5), round(p_ftt_sv(0.5, 0.5), 5))

        # test behaviour if t+a is out of bounds
        self.assertTrue(np.isnan(p_ftt_sv(1, 1)))


    def test_forward_transit_time_density(self):
        # two-dimensional, test FTT=BTT in steady state
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1, 2])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(0,1,3)
        # negative ages will be cut off automatically
        start_age_densities = lambda a: np.exp(-a)*start_values
        p = smr.pool_age_densities_func(start_age_densities)
        age_densities = p(ages)
        btt_arr = smr.backward_transit_time_density(age_densities)
        p_ftt = smr.forward_transit_time_density_func()
        ftt_arr = p_ftt(ages)

        for age in range(ftt_arr.shape[0]):
            for time in range(ftt_arr.shape[1]):
                if not np.isnan(ftt_arr[age, time]):
                    self.assertEqual(round(ftt_arr[age, time], 4), round(btt_arr[age,time], 4))
        

    ##### transit time moment methods #####


    def test_backward_transit_time_moment_from_density(self):
        # test mean BTT 
        x, y, t = symbols("x y t")
        state_vector = Matrix([x,y])
        A = Matrix([[-1, 0],
                    [ 0,-2]])
        u = Matrix(2, 1, [0,1])
        start_values = np.array([1,2])
        times = np.linspace(0,1,3)

        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)
        smr = SmoothModelRun(srm, parameter_set={}, start_values=start_values, times=times)

        start_age_densities = lambda a: 2*np.exp(-2*a)*start_values

        # the solution to be tested
        order = 1
        mbtt_from_dens = smr.backward_transit_time_moment_from_density(order, start_age_densities)

        # test against solution from mean age system

        start_age_moments = smr.moments_from_densities(1, start_age_densities)
        ref_mbtt = smr.backward_transit_time_moment(1, start_age_moments)

        self.assertTrue(np.allclose(mbtt_from_dens, ref_mbtt))
        

    def test_backward_transit_time_moment(self):
        x, y, t = symbols("x y t")
        state_vector = Matrix([x,y])
        A = Matrix([[-1, 0],
                    [ 0,-2]])
        u = Matrix(2, 1, [9,1])
        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)

        start_values = np.array([1,1])
        smr = SmoothModelRun(srm, {}, start_values, times=np.linspace(0,1,10))

        start_age_densities = lambda a: np.exp(-a) * start_values
        start_age_moments = smr.moments_from_densities(1, start_age_densities)
    
        # set manually mean age in first pool to zero
        start_age_moments[0,0] = 0 # first moment, first pool

        mbtt = smr.backward_transit_time_moment(1, start_age_moments)

        #mbtt_ref = smr.mean_backward_transit_time(tuple(start_age_moments[0]))
        mbtt_ref = np.array([ 0.66666667,  0.53297587,  0.46610489,  0.43540266,  0.42581404,  
                              0.42913526,  0.44055127,  0.45707559,  0.47677664,  0.4983646 ])

        self.assertTrue(np.allclose(mbtt, mbtt_ref)) 


    def test_forward_transit_time_moment(self):
        # if we start in steady state
        # and keep the inputs constant
        # forward and backward transit times should coincide.

        x, y, t = symbols("x y t")
        state_vector = Matrix([x,y])
        k = 10
        A = Matrix([[-k,  0],
                    [ 0, -k]])
        u = Matrix(2, 1, [1,1])
        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)

        start_values = np.array(-A**(-1)*u)
        smr = SmoothModelRun(srm, {}, start_values, times=np.linspace(0,1,11))

        start_age_densities = lambda a: np.exp(-a*k) / start_values*np.array(u)
        start_age_moments = smr.moments_from_densities(1, start_age_densities)
    
        mbtt = smr.backward_transit_time_moment(1, start_age_moments)
        mftt = smr.forward_transit_time_moment(1)

        self.assertTrue(np.allclose(mbtt[1:], mftt[1:]))
        self.assertTrue(np.isnan(mftt[0]))

        # test integration to infinity 
        x, t = symbols("x t")
        state_vector = Matrix([x])
        A = Matrix([-1])
        u = Matrix([1])
        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)
        
        start_values = np.array([1])
        n = 101
        times = np.linspace(0, 100, n)
        smr = SmoothModelRun(srm, {}, start_values, times)
        mftts = smr.forward_transit_time_moment(1)
        self.assertTrue(np.allclose(mftts[1:], np.ones((100,))))

        # some code to show possible problems with the sto
#        Phi = smr._state_transition_operator
#        Phi(1, 0, [1])
#        A = smr._state_transition_operator_values[0,:,:,:].reshape((101,))
#
#        from scipy.integrate import odeint
#        def rhs(X, t):
#            return -X
#
#        def f(X, t):
#            return odeint(rhs, X, [53, t])[-1]
#
#
#        C = np.array([f(A[ti], t+1) for ti, t in enumerate(np.linspace(0, 99, 100))]).reshape((100,))
#
#        ft = np.linspace(7, 10, 1001)
#        print('A')
#        plt.plot(ft, [Phi(54+t, 54, [1]) for t in ft])
#        print('B')
#        plt.plot(ft, np.exp(-ft), color = 'red')
#        ##plt.plot(ft, [f(t) for t in ft], ls = ':', linewidth = 5)
#        plt.show()
#
#        def integrand(a):
#            return Phi(54+a, 54, [1]).sum()
#
#        from scipy.integrate import quad
#        print(quad(integrand, 0, np.infty)[0])
#
#        #print(A)
#        #print(np.exp(-np.linspace(0,100,101)))
#        #print(C)



    @unittest.skip('just for now')
    def test_apply_to_forward_transit_time_simulation(self):
        x, t = symbols("x t")
        state_vector = Matrix([x])
        A = Matrix([-1*(1.4+sin(2*pi/10*t))])
        #A = Matrix([-1])
        u = Matrix([1])
        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)
        
        start_values = np.array([1])
        n = 101
        times = np.linspace(0, 100, n)
        smr = SmoothModelRun(srm, {}, start_values, times)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        fine_times = np.linspace(times[1], times[-1], n*100)
        for M in [0, 3, 11]:
        #for M in []:
            N = 1000
            if M == 0: N = 100
            sim_dict = smr.apply_to_forward_transit_time_simulation(f_dict = {'mean': np.mean}, N = N, M = M)

            for f_name, sub_dict in sim_dict.items():
                points = ax.plot(times, sub_dict['values'], ls = '-', label = f_name + ', M=' + str(M))
                if M == 0:
                    ax.plot(fine_times, sub_dict['smoothing_spline'](fine_times), ls = '--', label = f_name + ', smoothing, M=' + str(M), color = points[-1].get_color())
                else:
                    ax.plot(fine_times, sub_dict['interpolation'](fine_times), ls = '--', label = f_name + ', interpolation, M=' + str(M), color = points[-1].get_color())
       
        sim_dict = smr.apply_to_forward_transit_time_simulation(f_dict = {'mean': np.mean}, N = 100, MH = True)
        for f_name, sub_dict in sim_dict.items():
            points = ax.plot(times, sub_dict['values'], ls = '-', label = f_name + ', MH')
            ax.plot(fine_times, sub_dict['interpolation'](fine_times), ls = '--', label = f_name + ', interpolation, MH', color = points[-1].get_color())

        # plot true value (if integration is possible)
        mftts = smr.forward_transit_time_moment(1)
        ax.plot(times, mftts, color = 'black', label = 'integrated')

        ax.legend() 
        fig.savefig('test.pdf')
        #plt.show()


    ##### comma separated values output methods #####


    def test_save_and_load_csv(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0:1+0.3*sin(1/4*time_symbol), 1: 3}
        output_fluxes = {0: 1/6*C_0}
        internal_fluxes = {(0,1): C_0, (1,0): 1/4*C_1}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1, 3])
        times = np.linspace(0,50,5)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(0,50,5)
        start_age_densities = lambda a: np.exp(-a)*start_values
        start_age_moments = smr.moments_from_densities(1, start_age_densities)

        # test if saving and loading yields no diferences
        p = smr.pool_age_densities_func(start_age_densities)
        pool_age_densities = p(ages)
        system_age_density = smr.system_age_density(pool_age_densities)
        filename = 'age_dens.csv'
        smr.save_pools_and_system_density_csv(filename, pool_age_densities, system_age_density, ages)
        loaded_age_densities = smr.load_pools_and_system_densities_csv(filename, ages)

        self.assertTrue(np.allclose(pool_age_densities, loaded_age_densities[:,:,:2]))

        pool_age_mean = smr.age_moment_vector(1, start_age_moments)
        system_age_mean = smr.system_age_moment(1, start_age_moments)
        smr.save_pools_and_system_value_csv('age_mean.csv', pool_age_mean, system_age_mean)

        loaded_pool_age_mean, loaded_system_age_mean = smr.load_pools_and_system_value_csv('age_mean.csv')
        self.assertTrue(np.allclose(pool_age_mean,loaded_pool_age_mean))
        self.assertTrue(np.allclose(system_age_mean,loaded_system_age_mean))

        filename = 'btt_dens.csv'
        btt_density = smr.backward_transit_time_density(pool_age_densities)
        smr.save_density_csv(filename, btt_density, ages)

        btt_mean = smr.backward_transit_time_moment(1, start_age_moments)
        smr.save_value_csv(filename, btt_mean)


    ##### plotting methods #####

    
    ## solutions ##


    def test_plot_solutions(self):
        fig = plt.figure()
        mr = ESMR.nonlinear_two_pool()
        mr.plot_solutions(fig)
        fig.savefig("plot.pdf")
        plt.close(fig.number)


    def test_plot_phase_plane(self):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        mr = ESMR.nonlinear_two_pool()
        mr.plot_phase_plane(ax, 0, 1)
        fig.savefig("plot.pdf")
        plt.close(fig.number)
    

    def test_plot_phase_planes(self):
        fig = plt.figure()
        mr = ESMR.emanuel_1()
        mr.plot_phase_planes(fig)
        fig.savefig("plot.pdf")
        plt.close(fig.number)
    

    ## fluxes ##


    def test_plot_internal_fluxes(self):
        fig = plt.figure()
        smr = ESMR.nonlinear_two_pool()
        smr.plot_internal_fluxes(fig)
        fig.savefig("plot.pdf")
        plt.close(fig.number)


    def test_plot_external_output_fluxes(self):
        smr = ESMR.nonlinear_two_pool()
        fig = plt.figure()
        smr.plot_external_output_fluxes(fig)
        fig.savefig("plot.pdf")
        plt.close(fig.number)


    def test_plot_external_input_fluxes(self):
        smr = ESMR.nonlinear_two_pool()
        fig = plt.figure()
        smr.plot_external_input_fluxes(fig)
        fig.savefig("plot.pdf")
        plt.close(fig.number)


    ## means ##


    def test_plot_mean_ages(self):
        smr = ESMR.critics()
        fig = plt.figure()
        smr.plot_mean_ages(fig, np.array([0,0]))
        fig.savefig("plot.pdf")
        plt.close(fig.number)


    def test_plot_mean_backward_transit_time(self):
        smr = ESMR.critics()
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        smr.plot_mean_backward_transit_time(ax, np.array([0,0]))
        fig.savefig("plot.pdf")
        plt.close(fig.number)



    ## densities ##


    # age #

    #fixme: make it work
#    def test_plotly(self):
#        # two-dimensional
#        C_0, C_1 = symbols('C_0 C_1')
#        state_vector = [C_0, C_1]
#        time_symbol = Symbol('t')
#        input_fluxes = {0:1+1/4*sin(time_symbol), 1: 3}
#        output_fluxes = {0: C_0}
#        internal_fluxes = {(1,0): 1/6*C_1}
#        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)
#
#        start_values = np.array([1, 3])
#        times = np.linspace(0,10,11)
#        smr = SmoothModelRun(srm, {}, start_values, times)
#
#        ages = np.linspace(0,10,11)
#        start_age_densities = lambda a: np.exp(-a)*start_values
#        p = smr.pool_age_densities_func(start_age_densities)
#        age_densities = p(ages)
#        start_mean_ages = [1,1]
#        pool = 0        
#
#        fig = plt.figure()
#        ax = fig.add_subplot(111, projection='3d')
#        smr.plot_age_density_pool(ax, pool, age_densities, start_age_densities, ages, start_mean_ages) 
#
#        fig.savefig('testfig.pdf') 


    ##### cumulative distribution methods #####


    def test_cumulative_pool_age_distributions_single_value(self):
        # two-dimensional, no inputs
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 0, 1: 0}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        F_sv = smr.cumulative_pool_age_distributions_single_value(start_age_densities)

        ref = np.array([5-5*np.exp(-1), 3-3*np.exp(-1)])
        self.assertTrue(np.allclose(F_sv(1, 0), ref))

        ref = np.array([(5-5*np.exp(-1))*np.exp(-1), (3-3*np.exp(-1))*np.exp(-1)])
        self.assertTrue(np.allclose(F_sv(2, 1), ref))

        # two-dimensional, empty start system
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 0}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([0, 0])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        F_sv = smr.cumulative_pool_age_distributions_single_value(start_age_densities)
        ref = np.array([(1.0-np.exp(-1))-np.exp(-1.0/2)*(1-np.exp(-1.0/2)),0])
        self.assertTrue(np.allclose(F_sv(0.5, 1), ref))

        # two-dimensional, nonempty start system, input to first pool
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 0}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        F_sv = smr.cumulative_pool_age_distributions_single_value(start_age_densities)
        ref = np.array([(5-5*np.exp(-0.5))*np.exp(-0.5) + (1.0-np.exp(-0.5)),
                        (3-3*np.exp(-0.5))*np.exp(-0.5)])
        self.assertTrue(np.allclose(F_sv(1, 0.5), ref))


    def test_cumulative_system_age_distribution_single_value(self):
        # two-dimensional, nonempty start system, input to first pool
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 0}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        F_sv = smr.cumulative_system_age_distribution_single_value(start_age_densities)
        ref = np.array([(5-5*np.exp(-0.5))*np.exp(-0.5) + (1.0-np.exp(-0.5)),
                        (3-3*np.exp(-0.5))*np.exp(-0.5)])
        self.assertTrue(np.allclose(F_sv(1, 0.5), ref.sum()))


    def test_pool_age_distributions_quantiles(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 0, 1: 1}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1, 0])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        
        # compute the median with different numerical methods
        start_age_moments = smr.moments_from_densities(1, start_age_densities)
        start_values_q = smr.age_moment_vector(1, start_age_moments)
        a_star_newton = smr.pool_age_distributions_quantiles(0.5, start_values=start_values_q, start_age_densities=start_age_densities, method='newton')
        a_star_brentq = smr.pool_age_distributions_quantiles(0.5, start_age_densities=start_age_densities, method='brentq')
        self.assertTrue(np.allclose(a_star_newton[:,0], np.log(2)+times))
        self.assertTrue(np.allclose(a_star_brentq[:,0], np.log(2)+times))

        a, t = symbols('a t')
        ref_sym = solve(Eq(1/2*(1-exp(-t)), 1 - exp(-a)), a)[0]
        ref = np.array([ref_sym.subs({t: time}) for time in times], dtype=np.float)
        ref[0] = np.nan
        
        self.assertTrue(np.allclose(a_star_newton[:,1], ref, equal_nan=True))
        self.assertTrue(np.allclose(a_star_brentq[:,1], ref, equal_nan=True))

    
    def test_pool_age_distributions_quantiles_by_ode(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 0, 1: 1}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1, 0])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        
        # compute the median with different numerical methods
        start_age_moments = smr.moments_from_densities(1, start_age_densities)
        start_values_q = smr.age_moment_vector(1, start_age_moments)
        a_star = smr.pool_age_distributions_quantiles_by_ode(0.5, start_age_densities=start_age_densities)
        self.assertTrue(np.allclose(a_star[:,0], np.log(2)+times))

        a, t = symbols('a t')
        ref_sym = solve(Eq(1/2*(1-exp(-t)), 1 - exp(-a)), a)[0]
        ref = np.array([ref_sym.subs({t: time}) for time in times], dtype=np.float)
        ref[0] = np.nan
        
        self.assertTrue(np.allclose(a_star[:,1], ref, equal_nan=True))

    
    def test_system_age_distribution_quantiles(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 0, 1: 1}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1, 0])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        
        a_star_newton = smr.system_age_distribution_quantiles(0.5, start_age_densities=start_age_densities, method='newton')
        a_star_brentq = smr.system_age_distribution_quantiles(0.5, start_age_densities=start_age_densities, method='brentq')
        
        self.assertTrue(np.allclose(a_star_newton, np.log(2)))
        self.assertTrue(np.allclose(a_star_brentq, np.log(2)))

        # test empty start_system
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 0, 1: 1}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([0, 0])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        
        a_star = smr.system_age_distribution_quantiles(0.5, start_age_densities=start_age_densities)
        self.assertTrue(np.isnan(a_star[0]))


    def test_system_age_distribution_quantiles_by_ode(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 0, 1: 1}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1, 0])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        
        a_star = smr.system_age_distribution_quantiles_by_ode(0.5, start_age_densities=start_age_densities)
        
        self.assertTrue(np.allclose(a_star, np.log(2)))

        # test empty start_system
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 0, 1: 1}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([0, 0])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        
        a_star = smr.system_age_distribution_quantiles_by_ode(0.5, start_age_densities=start_age_densities)
        self.assertTrue(np.isnan(a_star[0]))

        # test steady state
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 1}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1, 1])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        a_star = smr.system_age_distribution_quantiles_by_ode(0.5, start_age_densities=start_age_densities)
        self.assertTrue(np.allclose(a_star, np.log(2)))


    ########## private methods ########## 
             
    
    def test_solve_age_moment_system_single_value(self):
        x, y, t = symbols("x y t")
        state_vector = Matrix([x,y])
        A = Matrix([[-1, 0],
                    [ 0,-2]])
        u = Matrix(2, 1, [9,1])
        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)
        t_end = 1
        t_mid=(t_end-0)/2
        start_values = np.array([1,1])
        smr = SmoothModelRun(srm, {}, start_values, times=np.linspace(0,t_end ,11))

        start_age_densities = lambda a: np.exp(-a) * start_values
        start_age_moments = smr.moments_from_densities(1, start_age_densities)
    
        # set manually mean age in first pool to zero
        start_age_moments[0,0] = 0

        ams_func = smr._solve_age_moment_system_single_value(1, start_age_moments)
        ams = ams_func(t_mid)
        soln = ams[:2]
        self.assertTrue(np.allclose(soln, smr.solve_single_value()(t_mid)))
        ma = ams[2:]

        ref = np.array([ 0.26884456,  0.90341213])
        self.assertTrue(np.allclose(ma, ref)) 

        ## test missing start_age_moments
        ams_func = smr._solve_age_moment_system_single_value(1)
        ams=ams_func(t_mid)
        soln = ams[:2]
        self.assertTrue(np.allclose(soln, smr.solve_single_value()(t_mid)))
        ma = ams[2:]
        ref_ams_func = smr._solve_age_moment_system_single_value(1, np.zeros((1,2))) # 1 moment, 2 pools
        ref_ams=ref_ams_func(t_mid)
        ref_ma = ref_ams[2:]
        self.assertTrue(np.allclose(ma, ref_ma))

        # test second order moments!
        start_age_moments = smr.moments_from_densities(2, start_age_densities)
        ams_func = smr._solve_age_moment_system_single_value(2, start_age_moments)

        # test missing start_age_moments
        ams_func = smr._solve_age_moment_system_single_value(2)


    def test_solve_age_moment_system(self):
        x, y, t = symbols("x y t")
        state_vector = Matrix([x,y])
        A = Matrix([[-1, 0],
                    [ 0,-2]])
        u = Matrix(2, 1, [9,1])
        srm = SmoothReservoirModel.from_A_u(state_vector, t, A, u)

        start_values = np.array([1,1])
        smr = SmoothModelRun(srm, {}, start_values, times=np.linspace(0,1,10))

        start_age_densities = lambda a: np.exp(-a) * start_values
        start_age_moments = smr.moments_from_densities(1, start_age_densities)
    
        # set manually mean age in first pool to zero
        start_age_moments[0,0] = 0

        ams = smr._solve_age_moment_system(1, start_age_moments)
        soln = ams[:,:2]
        self.assertTrue(np.allclose(soln, smr.solve()))
        ma = ams[:,2:]

        a_ref = np.array([[ 0.        ,  1.        ], 
                          [ 0.08202606,  0.99407994],
                          [ 0.14256583,  0.97750078],
                          [ 0.19599665,  0.95232484],
                          [ 0.24534554,  0.92082325],
                          [ 0.29165801,  0.8852548 ],
                          [ 0.33540449,  0.84768088],
                          [ 0.37683963,  0.80984058],
                          [ 0.41612357,  0.77309132],
                          [ 0.45337056,  0.73840585]])
        ref = np.ndarray((10,2), np.float, a_ref)
        self.assertTrue(np.allclose(ma, ref)) 

        # test missing start_age_moments
        ams = smr._solve_age_moment_system(1)
        soln = ams[:,:2]
        self.assertTrue(np.allclose(soln, smr.solve()))
        ma = ams[:,2:]
        ref_ams = smr._solve_age_moment_system(1, np.zeros((1,2))) # 1 moment, 2 pools
        ref_ma = ref_ams[:,2:]
        self.assertTrue(np.allclose(ma, ref_ma))

        # test second order moments!
        start_age_moments = smr.moments_from_densities(2, start_age_densities)
        ams = smr._solve_age_moment_system(2, start_age_moments)

        # test missing start_age_moments
        ams = smr._solve_age_moment_system(2)


    def test_save_and_load_state_transition_operator_cache(self):
        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = Matrix([C_0, C_1])
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)

        smr = SmoothModelRun(srm, {}, start_values, times)
        
        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        start_age_densities = lambda a: np.exp(-a)*start_values
        smr.build_state_transition_operator_cache()

        ca = smr._state_transition_operator_values
        size = smr._cache_size

        filename = 'sto.cache'
        smr.save_state_transition_operator_cache(filename)
        smr.load_state_transition_operator_cache(filename)
    
        self.assertEqual(size, smr._cache_size)
        self.assertTrue(np.all(ca==smr._state_transition_operator_values))


    def test_state_transition_operator(self):
        # one-dimensional case
        C = Symbol('C')
        state_vector = [C]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1} # are inputs really ignored in the computation of Phi?
        output_fluxes = {0: C}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        x = np.array([1])

        Phix = smr._state_transition_operator(1,0,x)

        self.assertEqual(Phix.shape, (1,))
        self.assertTrue(abs(Phix-np.exp(-1))<3e-05)

        # two-dimensional case
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5,3])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        x = np.array([1,3])
        Phix = smr._state_transition_operator(1,0,x)
       
        self.assertEqual(Phix.shape, (2,))
        
        # test t<t_0
        with self.assertRaises(Exception):
            Phix = smr._state_transition_operator(0,1,x)

        # test if operator works correctly also late in time
        C = Symbol('C')
        state_vector = [C]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1} # are inputs really ignored in the computation of Phi?
        output_fluxes = {0: C}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5])
        times = np.linspace(0,100,101)
        smr = SmoothModelRun(srm, {}, start_values, times)

        x = np.array([1])

        Phix = smr._state_transition_operator(91,89,x)
        self.assertTrue(abs(Phix-np.exp(-2))<3e-07)


    def test_output_rate_vector_at_t(self):
        # two-dimensional case
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1,3])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        self.assertTrue(np.allclose(smr.output_rate_vector_at_t(1), np.array([1, 1])))
        
    
    def test_output_rate_vector(self):
        # one-dimensional case
        C_0 = symbols('C_0')
        state_vector = [C_0]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: C_0}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1])
        times = np.linspace(0, 1, 11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ref = np.ones((11, 1))
        self.assertTrue(np.allclose(smr.output_rate_vector, ref))

        # two-dimensional case
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: time_symbol*C_0, 1: 2*C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([1,3])
        times = np.linspace(0,1,11)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ref_a = np.array([[ 1.        ,  3.        ], 
                          [ 0.90483744,  2.71451231],
                          [ 0.81873077,  2.4561923 ],
                          [ 0.74081821,  2.22245462],
                          [ 0.67032006,  2.01096019],
                          [ 0.60653067,  1.81959201],
                          [ 0.54881165,  1.64643494],
                          [ 0.49658532,  1.48975595],
                          [ 0.44932898,  1.34798693],
                          [ 0.40656968,  1.21970905],
                          [ 0.36787945,  1.10363835]])
        ref = np.ones((11, 2))
        ref[:,0] = np.linspace(0, 1, 11)
        ref[:,1] = 2
        self.assertTrue(np.allclose(smr.output_rate_vector, ref))


    ##### age density methods #####
    
    
    def test_age_densities_1_single_value(self):
        # one-dimensional
        C = Symbol('C')
        state_vector = [C]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: C}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        p1_sv = smr._age_densities_1_single_value(start_age_densities)

        # negative ages will be cut off automatically
        ages = np.linspace(-1,1,3)
        a_ref = np.array([[[ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ]],
                         
                          [[ 5.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ]],
                         
                          [[ 1.83939721],
                           [ 1.83939724],
                           [ 1.83939725],
                           [ 1.83939724],
                           [ 1.83939729],
                           [ 1.83939727]]])
                 
        ref = np.ndarray((3,6,1), np.float, a_ref)
        res_l = [[p1_sv(a, t) for t in times] for a in ages]
        res = np.array(res_l)
        self.assertTrue(np.allclose(res, ref))

        # test missing start_age_densities
        a_ref = np.array([[[ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ]],
                         
                          [[ 5.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ]],
                         
                          [[ 0         ],
                           [ 0         ],
                           [ 0         ],
                           [ 0         ],
                           [ 0         ],
                           [ 1.83939727]]])
        
        ref = np.ndarray((3,6,1), np.float, a_ref)
        p1_sv = smr._age_densities_1_single_value()
        res_l = [[p1_sv(a,t) for t in times] for a in ages]
        res = np.array(res_l)
        self.assertTrue(np.allclose(res, ref))

        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        start_age_densities = lambda a: np.exp(-a)*start_values
        p1_sv = smr._age_densities_1_single_value(start_age_densities)

        a_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 5.        ,  3.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 1.83939721,  1.10363832],
                  [ 1.83939724,  1.10363834],
                  [ 1.83939725,  1.10363835],
                  [ 1.83939724,  1.10363835],
                  [ 1.83939729,  1.10363837],
                  [ 1.83939727,  1.10363836]]])

        ref = np.ndarray((3,6,2), np.float, a_ref)
        res_l = [[p1_sv(a,t) for t in times] for a in ages]
        res = np.array(res_l)
        self.assertTrue(np.allclose(res, ref))

        # test missing start_age_densities
        a_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 5.        ,  3.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 1.83939727,  1.10363836]]])

        ref = np.ndarray((3,6,2), np.float, a_ref)
        p1_sv = smr._age_densities_1_single_value()
        res_l = [[p1_sv(a,t) for t in times] for a in ages]
        res = np.array(res_l)
        self.assertTrue(np.allclose(res, ref))


    def test_age_densities_1(self):
        # one-dimensional
        C = Symbol('C')
        state_vector = [C]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: C}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        start_age_densities = lambda a: np.exp(-a)*start_values
        p1 = smr._age_densities_1(start_age_densities)

        # negative ages will be cut off automatically
        ages = np.linspace(-1,1,3)
        a_ref = np.array([[[ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ]],
                         
                          [[ 5.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ]],
                         
                          [[ 1.83939721],
                           [ 1.83939724],
                           [ 1.83939725],
                           [ 1.83939724],
                           [ 1.83939729],
                           [ 1.83939727]]])
                 
        ref = np.ndarray((3,6,1), np.float, a_ref)
        self.assertTrue(np.allclose(p1(ages), ref))

        # test missing start_age_densities
        a_ref = np.array([[[ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ]],
                         
                          [[ 5.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ],
                           [ 0.        ]],
                         
                          [[ 0         ],
                           [ 0         ],
                           [ 0         ],
                           [ 0         ],
                           [ 0         ],
                           [ 1.83939727]]])
        
        ref = np.ndarray((3,6,1), np.float, a_ref)
        p1 = smr._age_densities_1()
        res = np.array(p1(ages))
        self.assertTrue(np.allclose(res, ref))

        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        start_age_densities = lambda a: np.exp(-a)*start_values
        p1 = smr._age_densities_1(start_age_densities)

        a_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 5.        ,  3.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 1.83939721,  1.10363832],
                  [ 1.83939724,  1.10363834],
                  [ 1.83939725,  1.10363835],
                  [ 1.83939724,  1.10363835],
                  [ 1.83939729,  1.10363837],
                  [ 1.83939727,  1.10363836]]])

        ref = np.ndarray((3,6,2), np.float, a_ref)
        self.assertTrue(np.allclose(p1(ages), ref))

        # test missing start_age_densities
        a_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 5.        ,  3.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 1.83939727,  1.10363836]]])

        ref = np.ndarray((3,6,2), np.float, a_ref)
        p1 = smr._age_densities_1()
        res = np.array(p1(ages))
        self.assertTrue(np.allclose(res, ref))


    def test_age_densities_2_single_value(self):
        # one-dimensional
        C = Symbol('C')
        state_vector = [C]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1}
        output_fluxes = {0: C}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        p2_sv = smr._age_densities_2_single_value()

        # negative ages will be cut off automatically
        ages = np.linspace(-1,1,3)
        a_ref = np.array([[[ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ]],
                         
                          [[ 0. ],
                           [ 1. ],
                           [ 1. ],
                           [ 1. ],
                           [ 1. ],
                           [ 1. ]],
                         
                          [[ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ]]])
                 
        ref = np.ndarray((3,6,1), np.float, a_ref)
        res_l = [[p2_sv(a, t) for t in times] for a in ages]
        res = np.array(res_l)
        self.assertTrue(np.allclose(res, ref))

        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        p2_sv = smr._age_densities_2_single_value()

        a_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 0.        ,  0.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ]],
                
                 [[ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ]]])

        ref = np.ndarray((3,6,2), np.float, a_ref)
        res_l = [[p2_sv(a, t) for t in times] for a in ages]
        res = np.array(res_l)
        self.assertTrue(np.allclose(res, ref))


    def test_age_densities_2(self):
        # one-dimensional
        C = Symbol('C')
        state_vector = [C]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1}
        output_fluxes = {0: C}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        p2 = smr._age_densities_2()

        # negative ages will be cut off automatically
        ages = np.linspace(-1,1,3)
        a_ref = np.array([[[ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ]],
                         
                          [[ 0. ],
                           [ 1. ],
                           [ 1. ],
                           [ 1. ],
                           [ 1. ],
                           [ 1. ]],
                         
                          [[ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ],
                           [ 0. ]]])
                 
        ref = np.ndarray((3,6,1), np.float, a_ref)
        self.assertTrue(np.allclose(p2(ages), ref))

        # two-dimensional
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        time_symbol = Symbol('t')
        input_fluxes = {0: 1, 1: 2}
        output_fluxes = {0: C_0, 1: C_1}
        internal_fluxes = {}
        srm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)

        start_values = np.array([5, 3])
        times = np.linspace(0,1,6)
        smr = SmoothModelRun(srm, {}, start_values, times)

        ages = np.linspace(-1,1,3)
        # negative ages will be cut off automatically
        p2 = smr._age_densities_2()

        a_ref = np.array(
                [[[ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ],
                  [ 0.        ,  0.        ]],
                
                 [[ 0.        ,  0.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ],
                  [ 1.        ,  2.        ]],
                
                 [[ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ],
                  [ 0         ,  0         ]]])

        ref = np.ndarray((3,6,2), np.float, a_ref)
        self.assertTrue(np.allclose(p2(ages), ref))

    
    ##### plot methods #####


    def test_density_plot(self):
        # actually tested by
        #   test_plot_age_density_pool
        #   test_plot_age_densities
        #   test_plot_system_age_densities
        pass





####################################################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSmoothModelRun)
#    # Run same tests across 16 processes
#    concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(16))
#    concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(1))
#    runner = unittest.TextTestRunner()
#    res=runner.run(concurrent_suite)
#    # to let the buildbot fail we set the exit value !=0 if either a failure or error occurs
#    if (len(res.errors)+len(res.failures))>0:
#        sys.exit(1)

    unittest.main()
