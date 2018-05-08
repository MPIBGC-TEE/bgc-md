#!/usr/bin/env python3
import sys
import unittest
import argparse
from concurrencytest import ConcurrentTestSuite, fork_for_tests
parser=argparse.ArgumentParser()
parser.add_argument("TestModule")
args=parser.parse_args()
print(args)
suite=unittest.defaultTestLoader.discover(".",pattern=args.TestModule)
concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(16))
runner = unittest.TextTestRunner()
res=runner.run(concurrent_suite)
# to let the buildbot fail we set the exit value !=0 if either a failure or error occurs
if (len(res.errors)+len(res.failures))>0:
    sys.exit(1)

