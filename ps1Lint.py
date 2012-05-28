#!/usr/local/bin/python3

import re

# http://www.gnu.org/software/bash/manual/html_node/Printing-a-Prompt.html 
promptVars = (
    r'a', #bell
    r'd', #date
    r'e', #escape
    r'h', #short hostname
    r'H', #full hostname
    r'j', #jobs
    r'l', #device name
    r'n', #newline
    r'r', #carriage return
    r's', #shell name
    r't', #time 24HH:MM:SS
    r'T', #time 12HH:MM:SS
    r'@', #time 12AM/PM
    r'A', #time 24HH:MM
    r'u', #username
    r'v', #bash version
    r'V', #bash release
    r'w', #current working directory
    r'W', #basename $PWD
    r'!', #history number
    r'#', #command number
    r'\$', #effective UID
    r'\\', #backslash
    r'd{3}', #ASCII code
    r'D\{%[a-zA-z\+%]+\}' #strftime
)

_fullPS1 = None
_parserPos = 0
_colorRegex = re.compile(r'\[(\d;)?(0|([349][0-7])?|10[0-7])m')
# Cursor movement: http://tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html
_cursorMvmentRegex = re.compile(r'\[\d?\d?;?\d?\d?[HfABCDJKsu]')

def parse(ps1): 
    global _fullPS1, _parserPos
    _fullPS1 = ps1
    _parserPos = 0
    l = len(ps1)

    try:
        while _parserPos < l:
            if ps1[_parserPos] == '\\':
                
                _parserPos += 1

                if ps1[_parserPos] == '[':
                    _parserPos += 1
                    _parserPos += validateEscape(ps1[_parserPos:])
                else:
                    _parserPos += validateVar(ps1[_parserPos:])        
                continue

            _parserPos += 1
    except SyntaxError:
        return False
    else:
        print('Success: "{0}" is a valid PS1!'.format(ps1))
        return True 

def logError(pos, msg):
    pos += _parserPos

    print('Error: {0}\n{1}\n{2}^'.format(msg, _fullPS1, '-' * pos))

    raise SyntaxError()

def validateVar(ps1):
    for var in promptVars:
        match = re.match(var, ps1)
        if match:
            return len(match.group(0))
    
    logError(0, '"{0}" is an invalid prompt variable.'.format(ps1[0]))

def validateColor(ps1, pos=0):
    colorStr = re.match(_colorRegex, ps1)
    if colorStr:
        return colorStr.group(0)
    else:
        logError(pos - 1, 'Invalid color code. See -c for valid colors.')

def validateEscape(ps1):
    pos = 0
    l = len(ps1)

    while pos < l:
        colorCodeOpen = re.match(r'\\(e|033)', ps1[pos:pos + 4]) 
        if colorCodeOpen:
            pos += len(colorCodeOpen.group(0))

            cursorMvmentMatch = re.match(_cursorMvmentRegex, ps1[pos:])
            if cursorMvmentMatch:
                pos += len(cursorMvmentMatch.group(0))
            else:
                # If there's no match, assume the author intended a color code.
                colorStr = validateColor(ps1[pos:], pos) 
                pos += len(colorStr)
        else:
            # Anything inside quotes is okay.
            match = re.match(r'[\'"].*[\'"]', ps1[pos:])
            if match:
                pos += len(match.group(0))
            else:
                logError(pos, 'Meaningless "{0}" character inside '
                              'escape sequence.'.format(ps1[pos])) 

        if ps1[pos:pos + 2] == r'\]':
            # Return the entire length of the escaped expression.
            return pos + 2

        pos += 1
    
    logError(0, 'Escape sequence was never closed.')
