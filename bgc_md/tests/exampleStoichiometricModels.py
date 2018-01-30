# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from sympy import zeros,Matrix,symbols,pprint
from bgc_md.StoichiometricModel import StoichiometricModel
def minimalBuildingBlocks(symbs):
    R,L,C,a_1_2,a_2_1=symbs
    n=3                                           
    X=Matrix(n,1,[R,L,C])             #
    m=2
    A=zeros(m,m)
    A[0,1]  = a_1_2 #this is the coefficient for b
    A[1,0]  = a_2_1
                                                  
    #the columns of B represent the stochiometrie 
    B=Matrix(zeros(n,m))
    B[:,0] = Matrix(n,1,[1,1,0])
    B[:,1] = Matrix(n,1,[0,0,1])
    return(X,A,B) 

def chavesBuildingBlocks():
    t=symbols('t')
    R_1,R_2,L,C_1,C_2,a_1_2,a_2_1,a_1_3,a_3_1,a_2_4,a_4_2,a_3_4,a_4_3=symbols("R_1,R_2,L,C_1,C_2,a_1_2,a_2_1,a_1_3,a_3_1,a_2_4,a_4_2,a_3_4,a_4_3")
    symbs = R_1,R_2,L,C_1,C_2,a_1_2,a_2_1,a_1_3,a_3_1,a_2_4,a_4_2,a_3_4,a_4_3
    n=5                                           # vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
    X=Matrix(n,1,[R_1,R_2,L,C_1,C_2])             #
    m=4
    A=zeros(m,m)
    A[0,1]  = a_1_2 #this is the coefficient for b
    A[1,0]  = a_2_1
    A[0,2]  = a_1_3
    A[2,0]  = a_3_1
    A[1,3]  = a_2_4
    A[3,1]  = a_4_2
    A[2,3]  = a_3_4
    A[3,2]  = a_4_3
                                                  
    #the columns of B represent the stochiometrie 
    B=Matrix(zeros(n,m))
    B[:,0] = Matrix(n,1,[1,0,1,0,0])
    B[:,1] = Matrix(n,1,[0,0,0,1,0])
    B[:,2] = Matrix(n,1,[0,1,1,0,0])
    B[:,3] = Matrix(n,1,[0,0,0,0,1])
    return(symbs,t,X,A,B) 


def minimalModel(symbs,time_symbol=None):
    mod = StoichiometricModel(*minimalBuildingBlocks(symbs))
    if time_symbol:
        mod.time_symbol=time_symbol
    return mod

def chavesModel():
    symbs,t,X,A,B = chavesBuildingBlocks()

    mod = StoichiometricModel(X,A,B,t)
    return mod
