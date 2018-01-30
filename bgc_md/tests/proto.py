#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import numpy as np
import sys 
from scipy.misc import factorial
from scipy.interpolate import interp1d 
from sympy import sin, symbols, Matrix, latex, Symbol, exp, solve, Eq, pi, Piecewise

import bgc_md.tests.exampleSmoothReservoirModels as ESRM
import bgc_md.tests.exampleSmoothModelRuns as ESMR

from testinfrastructure.InDirTest import InDirTest
from bgc_md.SmoothReservoirModel import SmoothReservoirModel  
from bgc_md.SmoothModelRun import SmoothModelRun 

class M:
    def __init__(self,func_set = {}):
        print(func_set)
        self.func_set = func_set

class TestSmoothModelRun(InDirTest):
    def test_1(self):
        d={"a":1}
        m = M(d)

    def test_2(self):
        m = M()
        
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
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSmoothModelRun)
    unittest.main()
