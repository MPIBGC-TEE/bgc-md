#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:

import unittest

import numpy as np
from sympy import symbols
#
import bgc_md.tests.exampleStoichiometricModels as ESTM
#
from bgc_md.StoichiometricModel import StoichiometricModel
from bgc_md.StoichiometricModelRun import StoichiometricModelRun
#from bgc_md.helpers import melt,pp


class TestStoichiometricModelRun(unittest.TestCase):
        
    def test_init(self):
        #create a valid model run 
        R_1,R_2,L,C_1,C_2,a_1_2,a_2_1,a_1_3,a_3_1,a_2_4,a_4_2,a_3_4,a_4_3=symbols("R_1,R_2,L,C_1,C_2,a_1_2,a_2_1,a_1_3,a_3_1,a_2_4,a_4_2,a_3_4,a_4_3")
        symbs=R_1,R_2,L,C_1,C_2,a_1_2,a_2_1,a_1_3,a_3_1,a_2_4,a_4_2,a_3_4,a_4_3
        srm = ESTM.chavesModel() 
        times = np.linspace(0, 20, 1600)
        start_values = np.array([7,2,15,0.5,0.5])
        pardict = {
            a_1_2:  0.25,
            a_2_1:  2.7 ,
            a_1_3:  0.8 ,
            a_3_1:  0.9 ,
            a_2_4:  0.45,
            a_4_2:  0.55,
            a_3_4:  0.25,
            a_4_3:  2.5
        }
        stmr = StoichiometricModelRun(srm, pardict, start_values, times)
       
        #fixme: 
        #make sure that exceptions are thrown for incompatible parameter sets

    def test_solve(self):
        symbs,t,X,A,B = ESTM.chavesBuildingBlocks()
        R_1,R_2,L,C_1,C_2,a_1_2,a_2_1,a_1_3,a_3_1,a_2_4,a_4_2,a_3_4,a_4_3=symbs

        srm = StoichiometricModel(X,A,B,t)
        times = np.linspace(0, 20, 1600)
        start_values = np.array([7,2,15,0.5,0.5])
        pardict = {
            a_1_2:  0.25,
            a_2_1:  2.7 ,
            a_1_3:  0.8 ,
            a_3_1:  0.9 ,
            a_2_4:  0.45,
            a_4_2:  0.55,
            a_3_4:  0.25,
            a_4_3:  2.5
        }
        stmr = StoichiometricModelRun(srm, pardict, start_values, times)
        print(stmr.solve())


    


####################################################################################################
if __name__ == '__main__':
    unittest.main()
 
 
 
 
 
 
 
 
