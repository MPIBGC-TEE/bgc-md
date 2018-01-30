#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:
# this is a pure python version 
# run with pyhton3 run_tests.py in a venv
import unittest
from concurrencytest import ConcurrentTestSuite, fork_for_tests
import bgc_md
import sys
# the following avoids errors due to buildbpt
import matplotlib
matplotlib.use('pdf')
# the following lines are only necessary if the bgc_md package is not installed
from pathlib import Path
p=Path(__file__).absolute().parents[2]
sys.path.append(p.as_posix())
import bgc_md.tests
print("################################### running tests ################################")

s=unittest.defaultTestLoader.discover(bgc_md.tests.__path__[0],pattern="Test*")
concurrent_suite = ConcurrentTestSuite(s, fork_for_tests(16))
##concurrent_suite = ConcurrentTestSuite(s, fork_for_tests(1))
r=unittest.TextTestRunner()
res=r.run(concurrent_suite)
if (len(res.errors)+len(res.failures))>0:
    sys.exit(1)
