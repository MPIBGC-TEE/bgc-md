#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:

import numpy as np
import matplotlib.pyplot as plt

from sympy import symbols, sin, Symbol, cos

from bgc_md.SmoothReservoirModel import SmoothReservoirModel  
from bgc_md.SmoothModelRun import SmoothModelRun 

if __name__ == '__main__':

    # two-dimensional model
    C_0, C_1 = symbols('C_0 C_1')
    state_vector = [C_0, C_1]
    t = Symbol('t')
    input_fluxes = {0:2+1*sin(1/4*t), 1: 3}
    output_fluxes = {0: 1/6*C_0}
    internal_fluxes = {(0,1): 1/4*C_0, (1,0): 1/4*C_1}
    srm = SmoothReservoirModel(state_vector, t, input_fluxes, output_fluxes, internal_fluxes)
    
    # start values, time frame
    start_values = (1, 3)
    times = np.linspace(0,1000,1001)
    smr = SmoothModelRun(srm, {}, start_values, times)
    
    # start ages and age frame
    ages = np.linspace(0,200,201)
    start_age_densities = lambda a: np.exp(-a)*np.array(start_values)
    start_mean_ages = (1,1)
    
    # plot a figure for comparison
    #fig = plt.figure(figsize=(100,5))
    #stretch = {'x': 1.3, 'y': 1.3, 'z': 1}
    #smr.plot_age_densities(fig, [0, 1, 'system'], start_age_densities, ages, start_mean_ages, stretch) 
    #
    #for ax in fig.get_axes():
    #    ax.view_init(elev=10, azim=-60)
    #
    #fig.savefig("density_plots.pdf")
    
    
    smr.save_age_densities_csv('age_dens.csv', start_age_densities, ages)
    smr.save_mean_ages_csv('mean_ages.csv', start_mean_ages)
    smr.save_age_density_values_for_mean_ages('adv_ma.csv', start_age_densities, start_mean_ages)









