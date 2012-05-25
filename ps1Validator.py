#!/usr/local/bin/python3

import re

colorRegex = re.compile(r'\\(e|033)\[\d{,2};?\d{,3}m')

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

class PS1Parser():
    _singletonInst = None
    
    def parse(self, ps1): 
        self.ps1 = ps1
        self._pos = 0
        l = len(ps1)

        while self._pos < l:
            if ps1[self._pos] == '\\':
                if ps1[self._pos + 1] == r'[':
                    self._pos += self.validateEscape(ps1[self._pos:])
                else:
                    self._pos += self.validateVar(ps1[self._pos:])        
            else:
                match = self.validVar('\\' + ps1[self._pos])
                if match is not False:
                    self.logIssue(1,
                             'Did you mean "{0}" ({1})?'.format(match['match'], 
                                                                match['type']), 
                             False)
                self._pos += 1
        
        print('Success: "{0}" is a valid PS1.'.format(ps1))

    def logIssue(self, deltaPos, msg, err=True):
        # Minus 1 to leave room for caret
        deltaPos += self._pos - 1

        print('{0}: {1}\n{2}\n{3}^'.format('Error' if err else 'Warning', msg,
                                           self.ps1, '-' * deltaPos))
        if err:
            print('Exiting...')
            raise SystemExit(0)
        
    def validVar(self, testVar):
        for key in promptVars:
            match = re.match(promptVars[key], testVar)
            if match is not None:
                return {'match': match.group(0), 'type': key}

        return False

    def validateVar(self, ps1):
        match = self.validVar(ps1)
        if match is not False:
            return len(match['match']) 
        else:
            self.logIssue(2, '"{0}" is an invalid prompt variable.'.format(ps1[:2]))

    def validateColor(self, ps1):
        colorStr = re.match(colorRegex, ps1)
        if colorStr:
            return colorStr.group(0)
        else:
            self.logIssue(0, 'Color code is not properly formatted.')

    def validateEscape(self, ps1):
        pos = 0
        l = len(ps1)

        while pos < l:
            if ps1[pos:pos + 2] == r'\e':
                colorStr = self.validateColor(ps1[pos:]) 
                pos += len(colorStr)
            if ps1[pos:pos + 2] == r'\]':
                # Return the length of the escaped expression
                return pos + 2

            pos += 1
        
        self.logIssue(0, 'Escape sequence was never closed.')
        

def main():
    import os

    parser = PS1Parser()
    test = r'\[\e[0;30mryuhx\]\ztj: '
    parser.parse(test)

    """ 
    validPS1s = open("validPS1s.txt")
    for line in validPS1s:
        if line[0] != '#' and line[0] != '\n':
            parsePS1(line.strip())
    """
if __name__ == "__main__": main()
