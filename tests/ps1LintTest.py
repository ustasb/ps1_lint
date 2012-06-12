import ps1Lint

def test():
    lineNum = 0
    test.tests = 0
    test.testsPassed = 0

    with open('tests/ps1s', 'r') as testPS1s:
        for ps1 in testPS1s:
            lineNum += 1
            
            if ps1[0] == '+': 
                testLine(lineNum, ps1, True)
            elif ps1[0] == '-':
                testLine(lineNum, ps1, False)

    print('{0}\n{1} tests passed out of ''{2}.\n'
          '{0}'.format('-' * 40, test.testsPassed, test.tests))

def testLine(lineNum, ps1, validPS1):
    test.tests += 1
    print('{0}. Line {1}'.format(test.tests, lineNum))
    
    ps1 = ps1.strip()
    isValid = ps1Lint.parse(ps1[1:])

    if isValid is validPS1:
        test.testsPassed += 1
        result = 'Pass'
    else:
        result = 'Fail'

    print('{0}: This PS1 is{1}valid.\n'
          .format(result, ' ' if validPS1 is True else ' NOT '))
