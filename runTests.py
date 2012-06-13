#!/usr/local/bin/python3

import os
import sys
import timeit
import tests.ps1LintTest

TESTS = 50

# Suppress output while timing tests.
oldStdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
timeTaken = timeit.timeit(tests.ps1LintTest.test, number=TESTS)

# Print a test to the console.
sys.stdout = oldStdout
tests.ps1LintTest.test()
print('Running {0} times took {1} seconds.'.format(TESTS, timeTaken))
