# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import sys
import yaml
from sympy import Symbol, Matrix, var, sin, cos, Matrix, lambdify, symbols, MatrixSymbol, diag, Eq, simplify, Piecewise, DiracDelta
import numpy as np
from bgc_md.ReservoirModel import ReservoirModel
from testinfrastructure.InDirTest import InDirTest


######### TestClass #############
class TestReservoirModel(InDirTest):
    
    def test_init(self):
        C_0, C_1 = symbols('C_0 C_1')
        state_vector = [C_0, C_1]
        t = Symbol('t')
        input_fluxes = {0: Piecewise((1, t<=1), (0, True)) + 1*DiracDelta(3-t),
                        1: Piecewise((2, t<=2), (0, True)) + 2*DiracDelta(3-t) + 4*DiracDelta(4-t)}
        output_fluxes = {0: 1*C_0, 1: 1*C_1}
        internal_fluxes = {}
        rm = ReservoirModel(state_vector, t, input_fluxes, output_fluxes, internal_fluxes)

        self.assertEqual(rm.clean_model.input_fluxes, {0: Piecewise((1, t<=1), (0, True)),
                                                       1: Piecewise((2, t<=2), (0, True))})
        
        self.assertEqual(rm.jump_times, [1,2,3,4])
        self.assertEqual(rm.impulsive_fluxes, {3: {0: 1, 1:2}, 4: {1: 4}})


#    def test_internal_flux_type(self):
#        # test simple cases
#        C_0, C_1  = symbols('C_0 C_1')
#        state_vector = [C_0, C_1]
#        time_symbol = Symbol('t')
#        input_fluxes = {}
#        output_fluxes = {}
#
#        internal_fluxes = {(0,1): 5*C_0, (1,0): 4*C_1**2}
#        rm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)
#
#        self.assertEqual(rm.internal_flux_type(0,1), 'linear')
#        self.assertEqual(rm.internal_flux_type(1,0), 'nonlinear')
#
#        # (1,0): 4 is considered to be nonlinear : in A the corresponding entry in 4/C_1
#        internal_fluxes = {(0,1): C_0+5, (1,0): C_1/C_0}
#
#        rm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)
#
#        self.assertEqual(rm.internal_flux_type(0,1), 'no substrate dependence')
#        self.assertEqual(rm.internal_flux_type(1,0), 'nonlinear')
#
#
#    def test_output_flux_type(self):
#        # test simple cases
#        C_0, C_1  = symbols('C_0 C_1')
#        state_vector = [C_0, C_1]
#        time_symbol = Symbol('t')
#        input_fluxes = {}
#        internal_fluxes = {}
#        
#        output_fluxes = {0: 5*C_0, 1: C_1**2}
#        rm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)
#
#        self.assertEqual(rm.output_flux_type(0), 'linear')
#        self.assertEqual(rm.output_flux_type(1), 'nonlinear')
#
#        # (1,0): 4 is considered to be nonlinear : in A the corresponding entry in 4/C_1
#        output_fluxes = {0: C_0+5, 1: C_1/C_0}
#
#        rm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)
#
#        self.assertEqual(rm.output_flux_type(0), 'no substrate dependence')
#        self.assertEqual(rm.output_flux_type(1), 'nonlinear')
#
#
#    def test_xi_T_N_u_representation(self):
#        u_0, u_1, C_0, C_1, gamma  = symbols('u_0 u_1 C_0 C_1 gamma')
#        state_vector = [C_0, C_1]
#        time_symbol = Symbol('t')
#        input_fluxes = {0: u_0, 1: u_1}
#        output_fluxes = {1: 3*gamma*C_0*C_1}
#        internal_fluxes = {(0,1): gamma*3*5*C_0*C_1, (1,0): gamma*3*4*C_0}
#
#        rm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)
#        xi, T, N, C, u = rm.xi_T_N_u_representation
#
#        self.assertEqual(u, Matrix([u_0, u_1]))
#        self.assertEqual(xi, 3*gamma)
#        self.assertEqual(T, Matrix([[-1, 4/(C_1 + 4)], [1, -1]]))
#        self.assertEqual(N, Matrix([[5*C_1, 0], [0, C_0*(C_1 + 4)/C_1]]))
#
#    def test_NTu_matrices_to_fluxes_and_back(self):
#        # f = u + xi*T*N*
#        t, C_1, C_2, C_3, gamma, k_1, k_2, k_3, t_12, t_13, t_21, t_23, t_31, t_32, u_1, u_2, u_3, xi \
#            = symbols('t C_1 C_2 C_3 gamma k_1 k_2 k_3 t_12 t_13 t_21 t_23 t_31 t_32 u_1 u_2 u_3 xi')
#        C = Matrix(3,1, [C_1, C_2, C_3])
#        u = Matrix(3,1, [u_1, u_2, u_3])
#        xi = gamma
#        T = Matrix([[  -1, t_12, t_13],
#                    [t_21,   -1, t_23],
#                    [t_31, t_32,   -1]])
#        N = diag(k_1, k_2, k_3)
#        A = gamma*T*N
#
#        rm=SmoothReservoirModel.from_A_u(C,t,A,u)
#
#        self.assertEqual(rm.input_fluxes, {0: u_1, 1: u_2, 2: u_3})
#        self.assertEqual(rm.output_fluxes, {0: gamma*k_1*(1-t_21-t_31)*C_1,
#                                   1: gamma*k_2*(1-t_12-t_32)*C_2,
#                                   2: gamma*k_3*(1-t_13-t_23)*C_3})
#        self.assertEqual(rm.internal_fluxes, {
#            (0,1): gamma*t_21*k_1*C_1, (0,2): gamma*t_31*k_1*C_1,
#            (1,0): gamma*t_12*k_2*C_2, (1,2): gamma*t_32*k_2*C_2,
#            (2,0): gamma*t_13*k_3*C_3, (2,1): gamma*t_23*k_3*C_3})
#
#        # test backward conversion to matrices
#        xi2, T2, N2, C2, u2 = rm.xi_T_N_u_representation
#        self.assertEqual(xi,xi2)
#        self.assertEqual(u,u2)
#        self.assertEqual(T,T2)
#        self.assertEqual(N,N2)
#
#
#    def test_Au_matrices_to_fluxes_and_back(self):
#        # f = u + xi*A*C
#        t,C_1, C_2, C_3, k_1, k_2, k_3, a_12, a_13, a_21, a_23, a_31, a_32, u_1, u_2, u_3, gamma, xi \
#        = symbols('t,C_1 C_2 C_3 k_1 k_2 k_3 a_12 a_13 a_21 a_23 a_31 a_32 u_1 u_2 u_3 gamma xi')
#        C = Matrix(3,1, [C_1, C_2, C_3])
#        u = Matrix(3,1, [u_1, u_2, u_3])
#        A = gamma*Matrix([
#                [-k_1, a_12, a_13],
#                [a_21, -k_2, a_23],
#                [a_31, a_32, -k_3]
#            ])
#        rm = SmoothReservoirModel.from_A_u(C,t,A,u)
#        self.assertEqual(rm.input_fluxes, {0: u_1, 1: u_2, 2: u_3})
#        self.assertEqual(rm.output_fluxes, {0: gamma*(k_1-a_21-a_31)*C_1,
#                                   1: gamma*(k_2-a_12-a_32)*C_2,
#                                   2: gamma*(k_3-a_13-a_23)*C_3})
#
#        self.assertEqual(rm.internal_fluxes, {
#            (0,1): gamma*a_21*C_1, (0,2): gamma*a_31*C_1,
#            (1,0): gamma*a_12*C_2, (1,2): gamma*a_32*C_2,
#            (2,0): gamma*a_13*C_3, (2,1): gamma*a_23*C_3})
#            
#        ## test backward conversion to compartmental matrix 
#        A2 = rm.compartmental_matrix
#        u2 = rm.external_inputs
#        self.assertEqual(u,u2)
#        self.assertEqual(A,A2)
#
#
#    def test_matrix_to_flux_and_back_nonlinear(self):
#        # f = u + xi*T*N*C
#        t,C_1, C_2, C_3, gamma, k_1, k_2, k_3, t_12, t_13, t_21, t_23, t_31, t_32, u_1, u_2, u_3, xi \
#            = symbols('t,C_1 C_2 C_3 gamma k_1 k_2 k_3 t_12 t_13 t_21 t_23 t_31 t_32 u_1 u_2 u_3 xi')
#        C = Matrix(3,1, [C_1, C_2, C_3])
#        u = Matrix(3,1, [u_1, u_2, u_3])
#        xi = gamma*2
#        T = Matrix([[  -1, t_12*C_2, t_13],
#                    [t_21,   -1, t_23],
#                    [t_31*k_1, t_32,   -1]])
#        N = diag(k_1*C_2, k_2/C_3, k_3)
#        rm = SmoothReservoirModel.from_A_u(C,t,xi*T*N,u)
#         
#        self.assertEqual(rm.input_fluxes, {0: u_1, 1: u_2, 2: u_3})
#        self.assertEqual(rm.output_fluxes, {0: 2*gamma*k_1*(1-t_21-t_31*k_1)*C_1*C_2,
#                                   1: -2*gamma*k_2*(-1+t_12*C_2+t_32)*C_2/C_3,
#                                   2: 2*gamma*k_3*(1-t_13-t_23)*C_3})
#        self.assertEqual(rm.internal_fluxes, {
#            (0,1): 2*gamma*t_21*k_1*C_1*C_2, (0,2): 2*gamma*t_31*k_1**2*C_1*C_2,
#            (1,0): 2*gamma*t_12*k_2*C_2**2/C_3, (1,2): 2*gamma*t_32*k_2*C_2/C_3,
#            (2,0): 2*gamma*t_13*k_3*C_3, (2,1): 2*gamma*t_23*k_3*C_3})
#
#        # test backward conversion to matrices
#        
#        xi2, T2, N2, C2,u2 = rm.xi_T_N_u_representation
#        self.assertEqual(xi,xi2)
#        self.assertEqual(u,u2)
#        self.assertEqual(T,T2)
#        self.assertEqual(N,N2)
#
#
#    def test_figure(self):
#        C_0, C_1  = symbols('C_0 C_1')
#        state_vector = [C_0, C_1]
#        time_symbol = Symbol('t')
#        input_fluxes = {}
#        output_fluxes = {}
#        internal_fluxes = {(0,1): 5*C_0*C_1, (1,0): 4*C_0}
#
#        rm = SmoothReservoirModel(state_vector, time_symbol, input_fluxes, output_fluxes, internal_fluxes)
#        fig = rm.figure()
#        fig.savefig("reservoir_model_plot.pdf")
#
#
#
