#!/usr/local/bin/python3

import re

# http://www.gnu.org/software/bash/manual/html_node/Printing-a-Prompt.html 
promptVars = (
    'a', # bell
    'd', # date
    'e', # escape
    'h', # short hostname
    'H', # full hostname
    'j', # jobs
    'l', # device name
    'n', # newline
    'r', # carriage return
    's', # shell name
    't', # time 24HH:MM:SS
    'T', # time 12HH:MM:SS
    '@', # time 12AM/PM
    'A', # time 24HH:MM
    'u', # username
    'v', # bash version
    'V', # bash release
    'w', # current working directory
    'W', # basename $PWD
    '\!', # history number
    '#', # command number
    r'\\', # backslash
    r'\$(?!\()', # effective UID
    r'[0231][0-7][0-7]', # ASCII octal code
    r'D\{(%[a-zA-z\+%]\s*)+\}' # strftime
)

_fullPS1 = None
_parserPos = 0
# Control Sequence Introducer (CSI)
_cursorMvmentCSIRegex = re.compile(r'^(2J|\d.*[ABCD]|\d*;\d*[Hf]|[suK])(?!.*m)')
_colorCSIRegex = re.compile(r'^(([0-8]|3[0-7]|4[0-7]);){0,2}([0-8]|3[0-7]|4[0-7])m')

def parse(ps1): 
    global _fullPS1, _parserPos
    _fullPS1 = ps1
    _parserPos = 0
    l = len(ps1)

    try:
        while _parserPos < l:

            # Commands inside `` or \$() are ignored
            if re.match(r'`|\\\$\(', ps1[_parserPos:]):
                commandSeq = re.match(r'^`[^`]*`|\\\$\([^)]*\)', ps1[_parserPos:])
                if commandSeq:
                    _parserPos += len(commandSeq.group(0))
                else:
                    logError(0, 'Command sequence not closed.')
                continue

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
    colorCSI = re.match(_colorCSIRegex, ps1)
    if colorCSI:
        return colorCSI.group(0)
    else:
        logError(pos - 1, 'Invalid color code. See -c for valid colors.')

def validateEscape(ps1):
    pos = 0
    l = len(ps1)
    
    while pos < l:
        escSeqBegin = re.match(r'\\(e|033)\[', ps1[pos:pos + 5]) 
        if escSeqBegin:
            pos += len(escSeqBegin.group(0))

            colorCSI = re.match(_colorCSIRegex, ps1[pos:])
            if colorCSI:
                pos += len(colorCSI.group(0))
            else:
                cursorMvmentCSI = re.match(_cursorMvmentCSIRegex, ps1[pos:])
                if cursorMvmentCSI:
                    pos += len(cursorMvmentCSI.group(0))
                else:
                    logError(pos, 'Invalid color or cursor movement sequence.')

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

def main():
    import sys

    parse(r'\[\033[44m\]')

if __name__ == '__main__': main()
