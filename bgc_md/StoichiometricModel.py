#!/usr/bin/env python3 
from string import Template
from sympy import zeros,Matrix
class StoichiometricModel:
    def __init__(self,X,A,B,time_symbol=None):
        self.state_variables=X
        self.A=A
        self.B=B
        self.time_symbol=time_symbol
        nx=X.shape[0]
        nb=B.shape[0]
        ma1=A.shape[1]
        ma0=A.shape[0]
        mb=B.shape[1]
        if not(nx==nb):
            raise(Exception(Template("The number of species in X=${X} and B=${B} is incompatible").substitute(X=X,B=B)))
        if not(ma1==ma0):
            raise(Exception("A is a quadratic nxn matrix where n is the number of complexes"))
        if not(mb==ma0):
            raise(Exception("The number of rows in B must conincide with the number of rows in A"))
        self.n=nx
        self.m=mb


    @property
    def rhs(self):
        X=self.state_variables
        A=self.A
        B=self.B
        n = self.n
        m = self.m
        X_dot=zeros(n,1)
        for i in range(m):
            for j in range(m):
                Prod=1
                for k in range(n):
                    Prod=Prod*X[k]**B[k,j]
                X_dot+=A[i,j]*Prod*(B[:,i]-B[:,j])
        
        return(X_dot)

    @property
    def stoichiometric_space(self):
        B=self.B
        n = self.n
        m = self.m
        SB=(Matrix([(B[:,i]-B[:,j]).transpose() for i in range (m) for j in range(i)])).transpose()

        SS=SB.columnspace()
        return SS


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
