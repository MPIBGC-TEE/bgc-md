from sympy import Basic,Symbol,Matrix,symbols
from sympy.vector import CoordSysND
from sympy.vector import Vector
#
#
#from typing import List
#        #for i in enumerate(
#
#
import unittest    
class TestMyTens(unittest.TestCase):
    def test_resolve_indexed_expression(self):
        # suppose v is a vector (in the physical coordinate independent sense)
        # in coord system 1 it has components [a,b,c,d]
        #first define a coordinate system

        vector_names=["e_1","e_2","e_3","e_4"]
        C=CoordSysND(name="C",vector_names=vector_names)

        
        a,b,c,d=symbols("a,b,c,d")
        v=a*C.e_1+b*C.e_2
        #print(v.to_matrix(C))

        #D=C.create_new(
        #     name="D"
        #    ,vector_names=["E_1","E_2","E_3","E_4"]
        #    ,transformation=lambda x1,x2,x3,x4:tuple(
        #        Matrix([
        #             [0,0,0,1]
        #            ,[0,1,0,0]
        #            ,[0,0,1,0]
        #            ,[1,0,0,0]
        #        ])
        #        *Matrix([x1,x2,x3,x4])
        #    )
        #)
        #print(v.to_matrix(D))
        #ed={Symbol('v'):sympify('Matrix([a,b,c,d])')}
        ## and the
        #res_exp=sympify('v[1]+v[2]',locals={'v':IndexedBase('v')}) # unfortunately sympyfy does not recognize 'sum(v[1:3])' which evaluates to the same result
        ## We confine ourselves here to what sympify can do at the moment
        #res=geometric_resolve(res_exp,sl,ed) 
        #pe('res',locals())
        ## now suppose res is coordinate invariant
        ## and we want to compute it for a representation of v in different
        ## and vp is related to v by
