# vim:set ff=unix expandtab ts=4 sw=4:
#import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches
#from pathlib import Path
#from sympy import diff, exp, lambdify, flatten, latex, Symbol
#from scipy.integrate import odeint, quad 
#from scipy.interpolate import interp1d
#import numpy as np
#
#from .SmoothModelRun import SmoothModelRun
#from .helpers import has_pw, numsol_symbolic_system
from .helpers_reservoir import numsol_symbolic_system

class StoichiometricModelRun:

    def __init__(self, stm, parameter_set={}, start_values=None, times = None):
        self.model = stm
        self.parameter_set = parameter_set
        self.times = times
        self.start_values = start_values

        times = sorted(times)


    def solve(self):
        self.func_set = {}
        mod = self.model
        state_variables=mod.state_variables
        rhs=mod.rhs
        time_symbol=mod.time_symbol
        
        soln = numsol_symbolic_system(
            state_variables,
            time_symbol,
            rhs,
            self.parameter_set,
            self.func_set,
            self.start_values, 
            self.times
        )
        return soln
                

