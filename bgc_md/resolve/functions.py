from functools import reduce
from sympy import Symbol,Number,Matrix
from sympy.matrices import SparseMatrix
from sympy.vector import CoordSysND,express,Vector,Dyadic
from sympy.combinatorics import Permutation
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from testinfrastructure.helpers import pe
from typing import List,Tuple
def srm_from_B_u_tens(
    # fixme mm 21.03 2019
    # This could become an alternative constructor (@classmethod) 
    # for CompartmetalSystems.SmoothReservoirModel
    # It is still here because it requires our special branch of sympy
    # and CompartmentalSystems should not suffer from this dependency
    # on the other hand Compartmental systems does not care about tensors
    # and vectors and does not have to. So it would also make sense to
    # keep the conversion code out of it.
    
        C:CoordSysND
        ,state_vector:Vector
        ,time_symbol:Symbol
        ,B:Dyadic
        ,u:Vector
    )->'SmoothReservoirModel':
    #pe('C',locals())
    #pe('state_vector',locals())
    #pe('time_symbol',locals())
    #pe('B',locals())
    #pe('u',locals())
    state_vector_mat=express(state_vector,C).to_matrix(C)
    B_mat=express(B,C).to_matrix(C)
    u_mat=express(u,C).to_matrix(C)
    return SmoothReservoirModel.from_B_u(state_vector_mat,time_symbol,B_mat,u_mat)

def dyad_from_matrix_and_coord_sys(
        m: Matrix
        ,C:CoordSysND
    ):
    bv=C.base_vectors()
    r=range(len(bv))
    dyads=[m[i,j]*bv[i]|bv[j] for i in r for j in r]
    return reduce(lambda acc,x:acc+x,dyads)  
    
def matrix_from_dyad_and_vector_list(
        B:Dyadic
        ,l:List[Vector]
    ):
    return matrix_from_dyad_and_vector_lists(B,l,l)

def matrix_from_dyad_and_vector_lists(
        B:Dyadic
        ,l1:List[Vector]
        ,l2:List[Vector]
    ):
    def f(i,j):
        return (l1[i].dot(B)).dot(l2[j])
    return Matrix(len(l1),len(l2),f)

def default_coordinate_system(
        state_tuple : Tuple[Symbol]
    ):
    return CoordSysND(name="C",vector_names=["e_" + str(sym) for sym in state_tuple],transformation='cartesian')
    
def permutationMatrix(
         l1:List[str]
        ,l2:List[str]
    ):
    n=len(l1)
    s=set(l1)
    ns=len(s)
    assert(n==ns) # no double entries in the first list
    assert(set(l1)==set(l2)) # make sure that we really deal with a permutation 
    p=Permutation([l2.index(el) for el in l1])
    return SparseMatrix(n,n,{(i,p(i)):1 for i in range(n)})
     

