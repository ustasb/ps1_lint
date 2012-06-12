#!/usr/local/bin/python3

import os
import sys
import timeit
import tests.ps1LintTest

# Suppress output while timing tests.
oldStdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
timeTaken = timeit.timeit(tests.ps1LintTest.test, number=50)

# Print a test to the console.
sys.stdout = oldStdout
tests.ps1LintTest.test()
print('Running 50 times took {0} seconds.'.format(timeTaken))
