#!/usr/local/bin/python3

import re

# Prompt variables from: 
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

_fullPS1 = None
_parserPos = 0
_colorRegex = re.compile(r'\\(e|033)\[\d{,2};?\d{,3}m')

def parse(ps1): 
    global _fullPS1, _parserPos
    _fullPS1 = ps1
    _parserPos = 0
    l = len(ps1)

    try:
        while _parserPos < l:
            if ps1[_parserPos] == '\\':
                if ps1[_parserPos + 1] == r'[':
                    _parserPos += validateEscape(ps1[_parserPos:])
                else:
                    _parserPos += validateVar(ps1[_parserPos:])        
            else:
                match = validVar('\\' + ps1[_parserPos])
                if match is not False:
                    logIssue(1,
                             'Did you mean "{0}" ({1})?'.format(match['match'], 
                                                                match['type']), 
                             False)
                _parserPos += 1
    except SyntaxError:
        return False
    else:
        print('Success: "{0}" is a valid PS1.'.format(ps1))
        return True 

def logIssue(deltaPos, msg, err=True):
    # Minus 1 to leave room for caret
    deltaPos += _parserPos - 1

    print('{0}: {1}\n{2}\n{3}^'.format('Error' if err else 'Warning', msg,
                                       _fullPS1, '-' * deltaPos))
    if err:
        raise SyntaxError()
    
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
        logIssue(2, '"{0}" is an invalid prompt variable.'.format(ps1[:2]))

def validateColor(ps1):
    colorStr = re.match(_colorRegex, ps1)
    if colorStr:
        return colorStr.group(0)
    else:
        logIssue(3, 'Color code is not properly formatted.')

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

        pos += 1
    
    logIssue(0, 'Escape sequence was never closed.')

def main():
    import os

    validPS1s = open("validPS1s.txt")
    for line in validPS1s:
        if line[0] != '#' and line[0] != '\n':
            parse(line.strip())

if __name__ == "__main__": main()
