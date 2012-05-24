#!/usr/local/bin/python3

import re

colorRE = re.compile(r'\\e\[\d{,2};?\d{,3}m')

# Prompt Variables from: 
# http://www.gnu.org/software/bash/manual/html_node/Printing-a-Prompt.html 
promptVars = {
    'bell':                         r'\\a',
    'date':                         r'\\d',
    'escape':                       r'\\e',
    'short hostname':               r'\\h',
    'full hostname':                r'\\H',
    'jobs':                         r'\\j',
    'device name':                  r'\\l',
    'newline':                      r'\\n',
    'carriage return':              r'\\r',
    'shell name':                   r'\\s',
    'time 24HH:MM:SS':              r'\\t',
    'time 12HH:MM:SS':              r'\\T',
    'time 12AM/PM':                 r'\\@',
    'time 24HH:MM':                 r'\\A',
    'username':                     r'\\u',
    'bash version':                 r'\\v',
    'bash release':                 r'\\V',
    'current working directory':    r'\\w',
    'basename $PWD':                r'\\W',
    'history number':               r'\\!',
    'command number':               r'\\#',
    'effective UID':                r'\\\$',
    'backslash':                    r'\\\\',
    'ASCII code':                   r'\d{3}',
    'strftime':                     r'\\D\{%[a-zA-z\+%]+\}'
}

def logIssue(ps1, pos, msg, err=True):
    print('{0}\n{1}^\n{2}: {3}'.format(ps1, '-' * (pos - 1),
                                       'Error' if err else 'Warning', msg))
    if err:
        raise SystemExit(0)
    
def validVar(testVar):
    for key in promptVars:
        match = re.match(promptVars[key], testVar)
        if match is not None:
            return {'match': match.group(0), 'type': key}

    return False

def validateVar(ps1):
    match = validVar(ps1)
    if match is not False:
        return len(match['match']) 
    else:
        logIssue(ps1, 2, '{0} is an invalid prompt variable'.format(ps1[:2]))

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
            match = validVar('\\' + ps1[pos])
            if match is not False:
                logIssue(ps1, pos + 1,
                         'Did you mean {0} ({1})?'.format(match['match'], match['type']), 
                         False)
            pos += 1
    
    print('{0} is a valid PS1'.format(ps1))
    
def main():
    import os
    
    validPS1s = open("validPS1s.txt")
    for line in validPS1s:
        if line[0] != '#' and line[0] != '\n':
            parsePS1(line.strip())

if __name__ == "__main__": main()
