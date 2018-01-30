#!/usr/bin/env python3 
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest
from bgc_md.StoichiometricModel import StoichiometricModel
from sympy import zeros,Matrix,symbols,pprint,simplify
from unittest import TestCase
import bgc_md.tests.exampleStoichiometricModels as ESTM
class TestStoichiometricModel(TestCase):

    def test_init(self):
        #create a valid model from the matrices A and B
        symbs,t,X,A,B=ESTM.chavesBuildingBlocks()
        mod=StoichiometricModel(X,A,B,t) 
        # fixme mm: to be extended for other combinations of ingredients



    def test_rhs(self):	
        symbs,t,X,A,B=ESTM.chavesBuildingBlocks()
        R_1,R_2,L,C_1,C_2,a_1_2,a_2_1,a_1_3,a_3_1,a_2_4,a_4_2,a_3_4,a_4_3=symbs
        mod=StoichiometricModel(X,A,B,t) 
        rhs=mod.rhs
        rhs_ref=Matrix(5,1,[
            -(a_2_1+a_3_1)*R_1*L+a_1_2*C_1+a_1_3*R_2*L,
            -(a_1_3+a_4_3)*R_2*L+a_3_1*R_1*L+a_3_4*C_2,
            -a_2_1*R_1*L-a_4_3*R_2*L + a_1_2*C_1 + a_3_4*C_2,
            -(a_1_2+a_4_2)*C_1 + a_2_1*R_1*L + a_2_4*C_2,
            -(a_3_4 + a_2_4)*C_2 + a_4_2*C_1 + a_4_3*R_2*L])
        	
        compare=simplify(rhs-rhs_ref)
        #pprint(compare)
        self.assertEqual(compare,zeros(5,1))
    
    def test_stoichiometric_space(self):	
        mod=ESTM.chavesModel()
        bs=mod.stoichiometric_space

####################################################################################################
if __name__ == '__main__':
    unittest.main()
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
 
 
 
 
 
 
 
 
 
 
