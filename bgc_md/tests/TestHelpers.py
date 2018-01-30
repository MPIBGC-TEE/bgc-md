# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import sys
from concurrencytest import ConcurrentTestSuite, fork_for_tests

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sympy import Matrix, symbols, sin, Piecewise, DiracDelta

from bgc_md.helpers import py2tex_silent

class TestHelpers(unittest.TestCase):

    def test_py2tex_silent(self):
        # check corrected handling of parentheses
        self.assertEqual(py2tex_silent('A - B + C'), 'A-B+C')
        self.assertEqual(py2tex_silent('A - (B + C)'), r'A-\left(B+C\right)')

        # check space between factors
        # change pytexit.py visit_Mult for more space or a \cdot or whatever
        self.assertEqual(py2tex_silent('A*B*C'), r'A\cdot B\cdot C')


####################################################################################################


if __name__ == '__main__':
    suite=unittest.defaultTestLoader.discover(".",pattern=__file__)
    # Run same tests across 16 processes
    concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(16))
    runner = unittest.TextTestRunner()
    res=runner.run(concurrent_suite)
    # to let the buildbot fail we set the exit value !=0 if either a failure or error occurs
    if (len(res.errors)+len(res.failures))>0:
        sys.exit(1)
