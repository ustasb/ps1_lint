#!/usr/local/bin/python3

import re

# http://www.gnu.org/software/bash/manual/html_node/Printing-a-Prompt.html 
# \e is only tolerated if inside \[ ... \].
# \a and \r are considered invalid as they cause line wrapping issues.
PROMPT_VARS = (
    'u', # username
    'h', # short hostname
    'w', # current working directory
    'n', # newline
    'W', # basename $PWD
    'H', # full hostname
    '#', # command number
    '@', # time 12AM/PM
    'd', # date
    'j', # jobs
    'l', # device name
    's', # shell name
    't', # time 24HH:MM:SS
    'T', # time 12HH:MM:SS
    'A', # time 24HH:MM
    'v', # bash version
    'V', # bash release
    '!', # history number
    r'\\', # backslash
    r'\$(?!\()', # effective UID
    r'(0[4-7]|1([0-6]|7(?!7)))[0-7]', # Matches octal 040-176 
    r'D\{(%[a-zA-z\+%]\s*)+\}' # strftime
)

# Anything inside ``, \$(), ${} or formatted as $<varName> is ignored.
CMD_CODE_REGEX = re.compile(r'^((`[^`]+`|\\\$\([^)]+\)|\$\{[^\}]+\}|\$\w+)+)')
ESC_SEQ_START_REGEX = re.compile(r'^(\\(e|033)\[)')
# Control Sequence Introducers (CSI)
COLOR_CSI_REGEX = re.compile(r'^((([0-8]|3[0-7]|4[0-7]);){0,2}([0-8]|3[0-7]|4[0-7])m)')
CURSOR_MVMENT_CSI_REGEX = re.compile(r'^(2J|[suK]|(\d+([ABCD]|;\d+[Hf]))|(\d+;)+\d+m)')

# Custom exception class
class PS1Error(SyntaxError):
    def __init__(self, pos, msg):
        self.pos = pos
        self.msg = msg

def parse(ps1):
    parserPos = 0
    ps1Len = len(ps1)

    try:
        while parserPos < ps1Len:

            # If `, \$(, or ${ is encountered, look for its closing equivalent.
            if re.match(r'`|\\\$\(|\$\{', ps1[parserPos:]):
                commandSeq = re.match(CMD_CODE_REGEX, ps1[parserPos:])
                if commandSeq is not None:
                    parserPos += len(commandSeq.group(0))
                else:
                    raise PS1Error(0, 'Command sequence not closed.')
                continue
            
            elif re.match(ESC_SEQ_START_REGEX, ps1[parserPos:]) is not None:
                raise PS1Error(0, 'Color or cursor movement sequence '
                                  'encountered without being escaped by '
                                  '\[ ... \].')

            # Don't match backslashes followed by white space or at the end
            # of the line.
            elif re.match(r'\\(?!\s|$)', ps1[parserPos:]) is not None:
                parserPos += 1
                if ps1[parserPos] == '[':
                    parserPos += 1
                    parserPos += validateNonPrintSeq(ps1[parserPos:])
                else:
                    parserPos += validateVar(ps1[parserPos:])
                continue

            parserPos += 1

    except PS1Error as err:
        parserPos += err.pos
        print('Error: {0}\n{1}\n{2}^'.format(err.msg, ps1, '-' * parserPos))
        return False
    else:
        print('Success: "{0}" is a valid PS1!'.format(ps1))
        return True 

def validateVar(ps1):
    for var in PROMPT_VARS:
        match = re.match(var, ps1)
        if match is not None:
            return len(match.group(0))

    if re.match(r'a|r', ps1):
        raise PS1Error(-1, '"\\{0}" causes line wrapping issues and should '
                           'not be used.'.format(ps1[0]))
    elif re.match(r'\d{3}', ps1):
        raise PS1Error(-1, '"\\{0}" is an invalid ASCII octal code--it must '
                           'be between 040 and 176.'.format(ps1[:4]))
    else: 
        raise PS1Error(-1, '"\\{0}" is an invalid prompt '
                           'variable.'.format(ps1[0]))

def validateNonPrintSeq(ps1):
    pos = 0
    ps1Len = len(ps1)
    
    while pos < ps1Len:
        escSeqStart = re.match(ESC_SEQ_START_REGEX, ps1[pos:pos + 5]) 
        if escSeqStart is not None:
            escSeqStartLen = len(escSeqStart.group(0)) 
            pos += escSeqStartLen

            colorCSI = re.match(COLOR_CSI_REGEX, ps1[pos:])
            if colorCSI is not None:
                seqType = 'color'
                pos += len(colorCSI.group(0))
            else:
                cursorMvmentCSI = re.match(CURSOR_MVMENT_CSI_REGEX, ps1[pos:])
                if cursorMvmentCSI is not None:
                    seqType = 'cursor movement'
                    pos += len(cursorMvmentCSI.group(0))
                    print('Warning: Cursor movement sequences can cause '
                          'line wrapping issues.')
                else:
                    raise PS1Error(pos - escSeqStartLen, 'Invalid color or '
                                                         'cursor movement '
                                                         'sequence.')

            if ps1[pos:pos + 2] != r'\]':
                raise PS1Error(pos, 'Expecting non-printing sequence to '
                                    'close after declared {0} sequence '
                                    'but it did not.'.format(seqType))
        else:
            match = re.match(CMD_CODE_REGEX, ps1[pos:])
            if match is not None:
                pos += len(match.group(0))
            else:
                raise PS1Error(pos, '"{0}" should not be here. Only color or '
                                    'cursor movement sequences should be put '
                                    'inside \[ ... \].'.format(ps1[pos])) 

        if ps1[pos:pos + 2] == r'\]':
            # Return the entire length of the escaped expression.
            return pos + 2

    raise PS1Error(0, 'Escape sequence was never closed.')

if __name__ == '__main__':
    import sys
    parse(sys.argv[1])
