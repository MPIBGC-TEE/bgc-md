
import unittest
from FrozenDict import FrozenDict
class TestFrozenDict(unittest.TestCase):
    def test_init(self):
        fd = FrozenDict({'a': 1, 'b': 2})

    def test_is(self):
        x = FrozenDict({'a': 1, 'b': 2})
        y = FrozenDict({'a': 1, 'b': 2})
        self.assertEqual((x is y),False)

    def test_equals(self):
        x = FrozenDict({'a': 1, 'b': 2})
        y = FrozenDict({'a': 1, 'b': 2})
        self.assertTrue((x == y))

    def test_as_dict_key(self):
        x = FrozenDict({'a': 1, 'b': 2})
        d={x:"foo"}
        self.assertTrue(d[x] == 'foo')
    
