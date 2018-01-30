# this module provides some examples of reservoir systems that are used in the tests
# to avoid global variables we put them in functions
from sympy import symbols, tanh, sin, cos, Matrix, pi
from bgc_md.SmoothReservoirModel import SmoothReservoirModel

def critics(symbs):
    t, k_01,k_10,k_0o,k_1o = symbs 
    x_0,x_1 = symbols("x_0 x_1")
    state_variables = [x_0, x_1] # order is important
    s1 = 10
    s2 = 20
    t1 = 20
    k = 1
    inputs = {
        0: s1+1/2*(1-tanh(-k*(t-t1))*(s2-s1))
        }
    outputs = {
        0: k_0o*x_0, # output from pool 0
        1: k_1o*x_1*(1+sin(t/2)) #output from pool 0
        }
    internal_fluxes = {
        (0,1):k_01*x_0 # flux from pool0  to pool 1
        }
    time_symbol = t
    srm = SmoothReservoirModel(state_variables, time_symbol, 
                             inputs,outputs, internal_fluxes, 
                             content_unit="kg C", time_unit="yr")
    return srm


def nonlinear_two_pool(symbs):
    t, k_01, k_10, k_0o, k_1o = symbs
    C_0, C_1 = symbols("C_0 C_1")
    state_variables = [C_0, C_1] # order is important
    inputs = {
        0: sin(t)+2, # input to pool 0
        1: cos(t)+2  # input to pool 1
        }
    outputs={
        0: k_0o*C_0**3, # output from pool 0
        1: k_1o*C_1**3  # output from pool 0
        }
    internal_fluxes={
        (0,1): k_01*C_0*C_1**2, # flux from pool0  to pool 1
        (1,0): k_10*C_0*C_1 # flux from pool1  to pool 0
        }
    time_symbol = t
    srm = SmoothReservoirModel(state_variables, time_symbol,
                               inputs,outputs,internal_fluxes,
                               content_unit="kg C", time_unit="yr")
    return srm


def minimal(symbs):
    x,t,k=symbs 
    inputs={0:1}
    outputs={0:-x*k}
    internal_fluxes={}
    mod=SmoothReservoirModel([x],t,inputs,outputs,internal_fluxes)
    return(mod)

def emanuel(symbs):
    u_1, u_3, x_1, x_2, x_3, x_4, x_5, t, F_1, F_2, F_3, F_4, F_5, F_21, F_41, F_42, F_52, F_43, F_53, F_54 = symbs
    x = Matrix(5,1,[x_1, x_2, x_3, x_4, x_5])
    u = (1+sin(t*pi*2)/2)*Matrix(5, 1, [u_1, 0, u_3, 0, 0])
    
    A  = (1+cos(t*pi*2))*Matrix([[-F_1,        0,       0,       0,        0],
                                 [F_21,     -F_2,       0,       0,        0],
                                 [   0,        0,    -F_3,       0,        0],
                                 [F_41,     F_42,    F_43,    -F_4,        0],
                                 [   0,     F_52,    F_53,    F_54,     -F_5]])
    srm = SmoothReservoirModel.from_A_u(x,t,A,u)
    return srm
