#!/usr/bin/bash

# If we assemble all tests into one testsuite some of the tests fail
# while they are ok if every module is run separately.
# Until this is solved we do it via bash
set -e
for f in Test*.py;do python3 -m unittest $f;done


#import sys
#import unittest
#import argparse
#from concurrencytest import ConcurrentTestSuite, fork_for_tests
#parser=argparse.ArgumentParser()
#parser.add_argument("TestModule",nargs='?')
#args=parser.parse_args()
#if args.TestModule is not None:
#    print('########################## args #######################')
#    print(args.TestModule)
#    suite=unittest.defaultTestLoader.discover(".",pattern=args.TestModule)
#    print(suite)
#else:
#    #suite=unittest.defaultTestLoader.discover(bgc_md.tests.__path__[0],pattern="Test*.py")
#    suite=unittest.defaultTestLoader.discover(".",pattern="Test*.py")
#
#runner = unittest.TextTestRunner()
##concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(16))
##res=runner.run(concurrent_suite)
#res=runner.run(suite)
#
## to let the buildbot fail we set the exit value !=0 if either a failure or error occurs
#if (len(res.errors)+len(res.failures))>0:
#    sys.exit(1)

