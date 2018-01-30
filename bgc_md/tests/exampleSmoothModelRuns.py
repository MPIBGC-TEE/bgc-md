import bgc_md.tests.exampleSmoothReservoirModels as ESRM
from bgc_md.SmoothReservoirModel import SmoothReservoirModel  
from bgc_md.SmoothModelRun import SmoothModelRun 
from sympy import symbols
import numpy as np

def critics():
    symbs = symbols("t, k_01,k_10,k_0o,k_1o") 
    t, k_01,k_10,k_0o,k_1o = symbs 
    srm = ESRM.critics(symbs)
    pardict = {k_0o: 0.01, k_1o: 0.08, k_01: 0.09, k_10: 1}
    start_values = np.array([0.001,0.001])
    times = np.linspace(0,100,1000)
    smr = SmoothModelRun(srm, pardict, start_values, times)
    return smr

def nonlinear_two_pool():
    symbs = symbols("t k_01 k_10 k_0o k_1o")
    t, k_01,k_10,k_0o,k_1o = symbs
    srm = ESRM.nonlinear_two_pool(symbs)
    # now create the modelrun
    pardict = {
        k_01:1/100,
        k_10:1/100,
        k_0o:1/2,
        k_1o:1/2
        }
    times = np.linspace(0, 20, 1600)   # time grid forward
    start_values = np.array([1,2])
    smr = SmoothModelRun(srm, pardict, start_values, times)
    return smr


def emanuel_1():
    symbs = symbols("I_1 I_3 x_1 x_2 x_3 x_4 x_5 t F_1 F_2 F_3 F_4 F_5 F_21 F_41 F_42 F_52 F_43 F_53 F_54")
    I_1,I_3,x_1,x_2,x_3,x_4,x_5,t,F_1, F_2, F_3, F_4, F_5, F_21, F_41, F_42, F_52, F_43, F_53, F_54 = symbs
    srm = ESRM.emanuel(symbs)
    # now create the modelrun

    pardict = {I_1: 77, I_3: 36, F_1: 2.081, F_2: 0.0686, F_3: 0.5217, F_4: 0.5926, F_5: 9.813e-3, F_21: 0.8378, F_41:  0.5676, F_42: 0.0322, F_52: 4.425e-3, F_43: 0.1739, F_53: 0.0870, F_54: 0.0370}
    start_values = np.array([37.00144, 451.89224, 69.00518, 80.2446, 1118.12122])
    times = np.arange(0, (10+(1/365)), 1/365)   # time grid forward
    smr = SmoothModelRun(srm, pardict, start_values, times)
    return smr
