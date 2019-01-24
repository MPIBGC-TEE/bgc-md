from sympy import Basic,Symbol,Matrix,symbols
from sympy.vector import CoordSysND, Vector,express
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
        C=CoordSysND(name="C",vector_names=vector_names,transformation='cartesian')

        
        a,b,c,d=symbols("a,b,c,d")
        v=a*C.e_1+b*C.e_2

        rotMat=Matrix([
             [0,0,0,1]
            ,[0,1,0,0]
            ,[0,0,1,0]
            ,[1,0,0,0]
        ])
        D=CoordSysND(name="D",parent=C,rotation_matrix=rotMat,location=Vector.zero)
        w=express(v,D)
        print(w.to_matrix(D))
        #ed={Symbol('v'):sympify('Matrix([a,b,c,d])')}
        ## and the
        #res_exp=sympify('v[1]+v[2]',locals={'v':IndexedBase('v')}) # unfortunately sympyfy does not recognize 'sum(v[1:3])' which evaluates to the same result
        ## We confine ourselves here to what sympify can do at the moment
        #res=geometric_resolve(res_exp,sl,ed) 
        #pe('res',locals())
        ## now suppose res is coordinate invariant
        ## and we want to compute it for a representation of v in different
        ## and vp is related to v by
