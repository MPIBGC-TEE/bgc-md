
import unittest
from testinfrastructure.helpers import pe

from bgc_md.resolve.IndexedSet import IndexedSet
from bgc_md.resolve.MVar import MVar
from bgc_md.resolve.Computer import Computer

class TestIndexedSet(unittest.TestCase):


    def test_init(self):
        myMvars= IndexedSet({
              MVar('coord_sys') 
            , MVar('state_vector')
        })

    def test_index(self):
        myMvars= IndexedSet({
              MVar('coord_sys') 
            , MVar('state_vector')
        })
        self.assertEqual(myMvars['coord_sys'].name,'coord_sys')

    def test_is(self):
        x =  IndexedSet({
              MVar('coord_sys') 
            , MVar('state_vector')
        })

        y =  IndexedSet({
              MVar('coord_sys') 
            , MVar('state_vector')
        })

        self.assertTrue(not(x is y))

    def test_hash(self):
        x =  IndexedSet({
              MVar('coord_sys') 
            , MVar('state_vector')
        })

        y =  IndexedSet({
              MVar('coord_sys') 
            , MVar('state_vector')
        })

        #print(x.__hash__())
        #print(y.__hash__())
        self.assertTrue( x.__hash__() == y.__hash__())

    def test_equals(self):
        x =  IndexedSet({
              MVar('coord_sys') 
            , MVar('state_vector')
        })

        y =  IndexedSet({
              MVar('coord_sys') 
            , MVar('state_vector')
        })
        self.assertTrue((x == y))

    def test_iter(self):
        # we want it to behave like a set
        x =  IndexedSet({
              MVar('coord_sys') 
            , MVar('state_vector')
        })

        for el in x:
            self.assertTrue(isinstance(el,MVar))

    #def test_as_dict_key(self):
    #    x = IndexedSet({'a': 1, 'b': 2})
    #    d={x:"foo"}
    #    self.assertTrue(d[x] == 'foo')
    
