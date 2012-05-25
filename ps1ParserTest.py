#!/usr/local/bin/python3

import ps1Parser

tests = 0
testsPassed = 0
testPS1s = open('testPS1s.txt')

def test(ps1, validPS1):
    global tests, testsPassed 
    
    tests += 1
    print('{0}.'.format(tests))
    
    ps1 = ps1.strip()
    isValid = ps1Parser.parse(ps1[1:])

    if isValid is validPS1:
        testsPassed += 1
        result = 'Pass'
    else:
        result = 'Fail'

    print('{0}: This PS1 is{1}valid.\n'
          .format(result, ' ' if validPS1 is True else ' NOT '))

for ps1 in testPS1s:
    if ps1[0] == '+': 
        test(ps1, True)
    elif ps1[0] == '-':
        test(ps1, False)

print('{0}\n{1} tests passed out of {2}.\n{0}'.format('-' * 40, 
                                                      testsPassed, tests))
