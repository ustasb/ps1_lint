#!/usr/local/bin/python3

import ps1Parser

testPS1s = open('testPS1s.txt')

for ps1 in testPS1s:
    if ps1[0] == '+': 
        isValid = ps1Parser.parse(ps1[1:].strip())
        print('{0}: {1}'.format('Pass' if isValid is True else 'Fail', ps1))
    elif ps1[0] == '-':
        isValid = ps1Parser.parse(ps1[1:].strip())
        print('{0}: {1}'.format('Pass' if isValid is False else 'Fail', ps1)) 
