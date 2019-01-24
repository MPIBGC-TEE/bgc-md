#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    #failures = test_runner.run_tests(["tests"])#
    #failures = test_runner.run_tests(["tests.test_Variables.VariableTest.test_statevector"])#
    failures = test_runner.run_tests(["tests.test_Variables.VariableTest.test_storeModel"])#
    sys.exit(bool(failures))
