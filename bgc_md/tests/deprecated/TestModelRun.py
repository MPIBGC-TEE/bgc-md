#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from concurrencytest import ConcurrentTestSuite, fork_for_tests
import unittest

from bgc_md.ReservoirModel import ReservoirModel  
from bgc_md.ModelRun import ModelRun 
from sympy import sin, cos, symbols, Matrix, lambdify, tanh, DiracDelta, Piecewise, Symbol
from testinfrastructure.InDirTest import InDirTest

import numpy as np
import sys 
#import bgc_md.tests.exampleSmoothReservoirModels as erm
#import bgc_md.tests.exampleSmoothModelRuns as EMR

class TestModelRun(InDirTest):
        
    def test_init(self):
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        t = Symbol('t')
        input_fluxes = {0: Piecewise((1, t<=1), (0, True)) + 1*DiracDelta(3-t),
                        1: Piecewise((2, t<=2), (0, True)) + 2*DiracDelta(3-t) + 4*DiracDelta(4-t)}
        output_fluxes = {0: 1*C_0, 1: 1*C_1}
        internal_fluxes = {}
        rm = ReservoirModel(state_vector, t, input_fluxes, output_fluxes, internal_fluxes)

        times = np.linspace(0,5,11)
        start_values = [5,3]
        mr = ModelRun(rm, start_values=start_values, times=times)
        
        ref_split_data = [{'intensity': [0, 0], 'times': [0.0, 0.5, 1.0]}, 
                          {'intensity': [0, 0], 'times': [1.0, 1.5, 2.0]}, 
                          {'intensity': [0, 0], 'times': [2.0, 2.5, 3.0]}, 
                          {'intensity': [1, 2], 'times': [3.0, 3.5, 4.0]}, 
                          {'intensity': [0, 4], 'times': [4.0, 4.5, 5.0]}]  
        self.assertTrue(mr.split_data,ref_split_data)

             
    def test_plot_sols(self):
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        t = Symbol('t')
        input_fluxes = {0: Piecewise((1, t<=1), (0, True)) + 1*DiracDelta(3-t),
                        1: Piecewise((2, t<=2), (0, True)) + 2*DiracDelta(3-t) + 4*DiracDelta(4-t)}
        output_fluxes = {0: 1*C_0, 1: 1*C_1/(C_0+1)}
        internal_fluxes = {(0,1): 1*C_1}
        rm = ReservoirModel(state_vector, t, input_fluxes, output_fluxes, internal_fluxes)

        times = np.linspace(0,10,1001)
        start_values = [5,0]
        mr = ModelRun(rm, start_values=start_values, times=times)
        
        fig = plt.figure()
        mr.plot_sols(fig)
        fig.savefig('testfig.pdf')

    def test_plot_phase_plane(self):
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        t = Symbol('t')
        input_fluxes = {0: Piecewise((1, t<=1), (0, True)) + 1*DiracDelta(3-t),
                        1: Piecewise((2, t<=2), (0, True)) + 2*DiracDelta(3-t) + 4*DiracDelta(4-t)}
        output_fluxes = {0: 1*C_0, 1: 1*C_1/(C_0+1)}
        internal_fluxes = {(0,1): 1*C_1}
        rm = ReservoirModel(state_vector, t, input_fluxes, output_fluxes, internal_fluxes)

        times = np.linspace(0,10,1001)
        start_values = [5,0]
        mr = ModelRun(rm, start_values=start_values, times=times)
        
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        mr.plot_phase_plane(ax, 0, 1)
        fig.savefig('testfig.pdf')

    def test_plot_phase_planes(self):
        C_0, C_1, C_2 = symbols('C_0 C_1 C_2')
        state_vector = [C_0, C_1, C_2]
        t = Symbol('t')
        input_fluxes = {0: Piecewise((1, t<=1), (0, True)) + 1*DiracDelta(3-t),
                        1: Piecewise((2, t<=2), (0, True)) + 2*DiracDelta(3-t) + 4*DiracDelta(4-t),
                        2: 1}
        output_fluxes = {0: 1*C_0, 1: 1*C_1/(C_0+1), 2: 1*C_2}
        internal_fluxes = {(0,1): 1*C_1}
        rm = ReservoirModel(state_vector, t, input_fluxes, output_fluxes, internal_fluxes)

        times = np.linspace(0,10,1001)
        start_values = [5,0,5]
        mr = ModelRun(rm, start_values=start_values, times=times)
        
        fig = plt.figure()
        mr.plot_phase_planes(fig)
        fig.savefig('testfig.pdf')



#
#    def test_plot_internal_fluxes(self):
#        fig=plt.figure()
#        mr=EMR.nonlinear_two_pool()
#        mr.plot_internal_fluxes(fig)
#        fig.savefig("plot.pdf")
#        plt.close(fig.number)
#
#    def test_plot_output_fluxes(self):
#        mr=EMR.nonlinear_two_pool()
#        fig=plt.figure()
#        mr.plot_output_fluxes(fig)
#        fig.savefig("plot.pdf")
#        plt.close(fig.number)
#
#    def test_plot_mean_ages_rasmussen(self):
#        mr=EMR.critics()
#        fig=plt.figure()
#        mr.plot_mean_ages_rasmussen(fig)
#        fig.savefig("plot.pdf")
#        plt.close(fig.number)
#
#    def test_mean_system_age_rasmussen(self):
#        # create a parallel model with identical 
#        # initial conditions and check that in this
#        # case the pool_system_ages
#        # are both equal to the system_system age
#        x,y,t=symbols("x,y,t")
#        X=Matrix([x,y])
#        rm=SmoothReservoirModel.from_A_u(X,t,Matrix([[-1,0],[0,-1]]))
#        mr=SmoothModelRun(rm,{},[1,1],[1,1],np.linspace(0,1,100))
#        n=mr.nr_pools
#        soln=mr.solve_mean_age_system()
#        msa=mr.mean_system_age_rasmussen
#        for i in range(n,2*n):
#            print(i)
#            self.assertTrue((((soln[:,i]-msa)**2).sum() < 1e-16))
#
#
#
#    def test_plot_mean_transit_time_rasmussen(self):
#        mr=EMR.critics()
#        fig=plt.figure()
#        mr.plot_mean_ages_rasmussen(fig)
#        fig.savefig("plot.pdf")
#        plt.close(fig.number)
#   
####################################################################################################




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModelRun)
    # Run same tests across 16 processes
    #concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(16))
    concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(1))
    runner = unittest.TextTestRunner()
    res=runner.run(concurrent_suite)
    # to let the buildbot fail we set the exit value !=0 if either a failure or error occurs
    if (len(res.errors)+len(res.failures))>0:
        sys.exit(1)
