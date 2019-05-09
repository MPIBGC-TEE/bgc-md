from sympy import Symbol,Number,symbols,Matrix,Rational
from sympy.vector import CoordSysND,express,Vector,Dyadic,matrix_to_vector
from bgc_md.resolve.functions import permutationMatrix
class TestMvars(unittest.TestCase):
    def test_alternative_coordinate_systems_for_model_comparison(self):
        # Assume that we have a bunch of  different pool systems that are actually quite
        # similar but have a very different ordering of state variables.
        # To make the similarity obvious a user could add alternative coordinate systems to 
        # the respective models that lead to comparable matrices
        # Assume that all systems to be compared consist of 2 soil layers with a fast and slow
        # soil pool  pool in each layer and that we want to compare them by a layer-wise view
        # with first the fast and then the slow pools:
        # comp_ord=["e_soilfast1","e_soilslow1",  "e_soilfast2","e_soilslow2"]

        # Assume that The base vectors of the first system are called
        vector_names_a=["e_1", "e_2", "e_3" ,"e_4"]  
        A=CoordSysND(name="A",vector_names=vector_names_e,transformation='cartesian')
        #and the vector to be compared is 
        v_a=a*C.e_sf1+b*C.e_ss1
        # and that reordered by the user with knowledge of which pools are fast 
        # to the comparison order would be 
        ord_a=["e_3", "e_2", "e_1", "e_4"]  
        pm_a=permutationMatrix(vector_names_a,ord_a)
        A_comp=CoordSysND(name="A_comp",parent=A,rotation_matrix=pm_a)

        # Now suppose the vectors in a second model are called 
        vector_names_b=["E_1", "E_2", "E_3" ,"E_4"]  
        B=CoordSysND(name="B",vector_names=vector_names_b,transformation='cartesian')
        # and that reordered by the user with knowledge of which pools are fast 
        # to the comparison order would be 
        ord_b=["E_3", "E_2", "E_4", "E_1"]  
        pm_b=permutationMatrix(vector_names_b,ord_b)
        B_comp=CoordSysND(name="B_comp",parent=B,rotation_matrix=pm_b)
        a,b,c,d,e,f=symbols("a,b,c,d,e,f")
        pm_b=permutationMatrix(o1,o2)
        D=CoordSysND(name="D",parent=C,rotation_matrix=pm)
        v=a*C.e_sf1+b*C.e_ss1
        w=express(v,D)
        print(w)
        print(w.to_matrix(D))
