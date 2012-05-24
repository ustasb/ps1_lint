#!/usr/local/bin/python3

import re

colorRE = re.compile(r'\\e\[\d{,2};?\d{,3}m')

# Prompt Variables from: 
promptVars = {
    'bell':             r'\\a',
    'date':             r'\\d',
    'escape':           r'\\e',
    'hostnameMin':      r'\\h',
    'hostnameFull':     r'\\H',
    'jobs':             r'\\j',
    'deviceName':       r'\\l',
    'newline':          r'\\n',
    'carriageReturn':   r'\\r',
    'shellName':        r'\\s',
    'time24HH:MM:SS':   r'\\t',
    'time12HH:MM:SS':   r'\\T',
    'time12AMPM':       r'\\@',
    'time24HH:MM':      r'\\A',
    'username':         r'\\u',
    'bashVersion':      r'\\v',
    'bashRelease':      r'\\V',
    'cwd':              r'\\w',
    'basename$PWD':     r'\\W',
    'historyNumber':    r'\\!',
    'commandNumber':    r'\\#',
    'effUID':           r'\\\$',
    'backslash':        r'\\\\',
    'octalValChr':      r'\d{3}',
    'strftime':         r'\\D\{%[a-zA-z\+%]+\}'
}

def logIssue(ps1, pos, msg, err=True):
    print('{0}\n{1}^\n{2}: {3}'.format(ps1, '-' * (pos - 1),
                                       'Error' if err else 'Warning', msg))
    if err:
        raise SystemExit(0)
    
def validateVar(ps1):
    for regex in promptVars.values():
        print(regex, ps1)
        match = re.match(regex, ps1)
        if match: 
            return len(match.group(0)) 

    logIssue(ps1, 2, '{} is an invalid prompt variable'.format(ps1))

def validateColor(ps1):
    colorStr = re.match(colorRE, ps1)
    if colorStr:
        return colorStr.group(0)
    else:
        logIssue(ps1, 0, 'Color code is not properly formatted')

def validateEscape(ps1):
    pos = 0
    l = len(ps1)

    while pos < l:
        if ps1[pos:pos + 2] == r'\e':
            colorStr = validateColor(ps1[pos:]) 
            pos += len(colorStr)
            if ps1[pos:pos + 2] == r'\]':
                #print('Matched {}'.format(ps1[:i + 2]))
                # Return the length of the escaped expression
                return pos + 2
            else:
                logIssue(ps1, pos,
                         'Escape sequence not closed after declared color code')
        else:
            pass
        
        pos += 1
    
    logIssue(ps1, 0, 'Escape sequence was never closed.')

def parsePS1(ps1):
    pos = 0
    l = len(ps1)

    while pos < l:
        if ps1[pos] == '\\':
            if ps1[pos + 1] == r'[':
                pos += validateEscape(ps1[pos:])
            else:
                pos += validateVar(ps1[pos:])        
        else:
            pos += 1
    
    print('{} is a valid PS1'.format(ps1))
    
def main():
    import os
    
    validPS1s = open("validPS1s.txt")
    for line in validPS1s:
        if line[0] != '#' and line[0] != '\n':
            parsePS1(line.strip())

if __name__ == "__main__": main()
