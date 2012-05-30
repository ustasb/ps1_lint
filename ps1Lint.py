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
    r'[0-3][0-7][0-7]', # ASCII octal code
    r'D\{(%[a-zA-z\+%]\s*)+\}' # strftime
)

# Control Sequence Introducer (CSI)
_cursorMvmentCSIRegex = re.compile(r'(2J|\d.*[ABCD]|\d*;\d*[Hf]|[suK])(?!.*m)')
_colorCSIRegex = re.compile(r'(([0-8]|3[0-7]|4[0-7]);){0,2}([0-8]|3[0-7]|4[0-7])m')

class PS1Error(SyntaxError):
    def __init__(self, pos, msg):
        self.pos = pos
        self.msg = msg

def parse(ps1): 
    parserPos = 0
    l = len(ps1)

    try:
        while parserPos < l:

            # Anything inside ``, ${} or \$() is ignored
            if re.match(r'`|\\\$\(|\$\{', ps1[parserPos:]):
                commandSeq = re.match(r'`[^`]*`|\\\$\([^)]*\)|\$\{[^}]*\}',
                                      ps1[parserPos:])
                if commandSeq:
                    parserPos += len(commandSeq.group(0))
                else:
                    raise PS1Error(0, 'Command sequence not closed.')
                continue

            if ps1[parserPos] == '\\':
                
                parserPos += 1

                if ps1[parserPos] == '[':
                    parserPos += 1
                    parserPos += validateNonPrintSeq(ps1[parserPos:])
                else:
                    parserPos += validateVar(ps1[parserPos:])        
                continue

            parserPos += 1
    except SyntaxError as err:
        parserPos += err.pos

        print('Error: {0}\n{1}\n{2}^'.format(err.msg, ps1, '-' * parserPos))

        return False
    else:
        print('Success: "{0}" is a valid PS1!'.format(ps1))
        return True 

def validateVar(ps1):
    for var in promptVars:
        match = re.match(var, ps1)
        if match:
            return len(match.group(0))
    
    raise PS1Error(0, '"{0}" is an invalid prompt variable.'.format(ps1[0]))

def validateNonPrintSeq(ps1):
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
                    raise PS1Error(pos, 'Invalid color or cursor movement sequence.')

        else:
            # Anything inside quotes or ${} is okay.
            match = re.match(r'([\'"])[^\1]*\1|\$\{[^}]*\}', ps1[pos:])
            if match:
                pos += len(match.group(0))
            else:
                raise PS1Error(pos, 'Meaningless "{0}" character inside '
                              'escape sequence.'.format(ps1[pos])) 

        if ps1[pos:pos + 2] == r'\]':
            # Return the entire length of the escaped expression.
            return pos + 2

        pos += 1
    
    raise PS1Error(0, 'Escape sequence was never closed.')

def main():
    import sys

    parse(r'\[\033[44m\]')

if __name__ == '__main__': main()
