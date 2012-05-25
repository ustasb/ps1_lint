#!/usr/local/bin/python3

import re

colorRegexTpl = (r'\[', r'\d{,2}', r';?', r'\d{,3}', r'm')
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
_colorRegex = re.compile(''.join(colorRegexTpl))
# http://tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html
_cursorMvmentRegex = re.compile(r'\[\d?\d?;?\d?\d?[HfABCDJKsu]')

def parse(ps1, warnings=False): 
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
                if warnings is True:
                    match = validVar('\\' + ps1[_parserPos])
                    if match is not False:
                        msg = ('Did you mean "{0}"'
                               '({1})?'.format(match['match'], match['type']))
                        logIssue(0, msg, False)

                _parserPos += 1
    except SyntaxError:
        return False
    else:
        print('Success: "{0}" is a valid PS1!'.format(ps1))
        return True 

def logIssue(pos, msg, err=True):
    pos += _parserPos

    print('{0}: {1}\n{2}\n{3}^'.format('Error' if err else 'Warning', msg,
                                       _fullPS1, '-' * pos))
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
        logIssue(0, '"{0}" is an invalid prompt variable.'.format(ps1[:2]))

def validateColor(ps1, pos=0):
    print(ps1)
    colorStr = re.match(_colorRegex, ps1)
    if colorStr:
        return colorStr.group(0)
    else:
        for i, chr in enumerate(ps1):
            if re.match(colorRegexTpl[i], chr) is None:
                logIssue(pos, 'Invalid color code. Mising "{0}" in sequence '
                              '"\e[x;ym".'.format(colorRegexTpl[i]))

def validateEscape(ps1):
    escapeSeqLen = 2 # \]
    pos = escapeSeqLen
    l = len(ps1)

    while pos < l:
        colorCodeOpen = re.match(r'\\(e|033)', ps1[pos:pos + 4]) 
        if colorCodeOpen is not None:
            pos += len(colorCodeOpen.group(0))

            cursorMvmentMatch = re.match(_cursorMvmentRegex, ps1[pos:])
            if cursorMvmentMatch is not None:
                pos += len(cursorMvmentMatch.group(0))
            else:
                colorStr = validateColor(ps1[pos:], pos) 
                pos += len(colorStr)
        else:
            match = re.match(r'[\'"].*[\'"]', ps1[pos:])
            if match is not None:
                pos += len(match.group(0))
            else:
                logIssue(pos, 'Meaningless "{0}" character inside '
                              'escape sequence.'.format(ps1[pos])) 

        if ps1[pos:pos + 2] == r'\]':
            # Return the entire length of the escaped expression
            return pos + escapeSeqLen

        pos += 1
    
    logIssue(0, 'Escape sequence was never closed.')
