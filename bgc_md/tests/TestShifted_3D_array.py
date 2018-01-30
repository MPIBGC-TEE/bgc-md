import unittest
from bgc_md.Shifted_3D_array import Shifted_3D_array
import numpy as np

class TestShifted_3D_array(unittest.TestCase):
#################################################
    def test_creation(self):
        #create an ndarray 
        arr = np.arange(8)
                # fixme:
                # we should make sure (test) that the shape of the array we turn into a Shifted_3D_array is really 3D...
        
        # and create an instance from it
        obj= Shifted_3D_array(arr)
        self.assertEqual(obj.t_shift,0)
        #now combine with shift settings
        obj= Shifted_3D_array(arr,Ts_shift=2)
        self.assertEqual(obj.Ts_shift,2)
 

    def test_t_shift(self):
        arr = np.arange(8)
        arr.resize(2,2,2)
        a= Shifted_3D_array(arr)
        a[0,0,0]=1
        a[1,0,0]=2
        a.set_t_shift(1)
    #    print(type(a))
    #    print(a[0,0,0])
        self.assertEqual(a[0,0,0],2)
    
####################################################################################################
if __name__ == '__main__':
    s=unittest.defaultTestLoader.discover(".",pattern=__file__)
    res=unittest.TextTestRunner().run(s)
    # uncomment to run same tests across 16 processes
    # cs= ConcurrentTestSuite(s, fork_for_tests(16))
    # res=unittest.TextTestRunner().run(cs)
