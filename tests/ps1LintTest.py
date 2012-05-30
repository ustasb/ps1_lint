#!/usr/local/bin/python3

import ps1Lint

lineNum = 0
tests = 0
testsPassed = 0
testPS1s = open('tests/testPS1s.txt')

def test(lineNum, ps1, validPS1):
    global tests, testsPassed 
    
    tests += 1
    print('{0}. Line {1}'.format(tests, lineNum))
    
    ps1 = ps1.strip()
    isValid = ps1Lint.parse(ps1[1:])

    if isValid is validPS1:
        testsPassed += 1
        result = 'Pass'
    else:
        result = 'Fail'

    print('{0}: This PS1 is{1}valid.\n'
          .format(result, ' ' if validPS1 is True else ' NOT '))

for ps1 in testPS1s:
    lineNum += 1
    
    if ps1[0] == '+': 
        test(lineNum, ps1, True)
    elif ps1[0] == '-':
        test(lineNum, ps1, False)

testPS1s.close()

print('{0}\n{1} tests passed out of {2}.\n{0}'.format('-' * 40, 
                                                      testsPassed, tests))
