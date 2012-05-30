#!/usr/local/bin/python3

class PS1Error(SyntaxError):
    def __init__(self, pos, msg):
        self.pos = pos
        self.msg = msg

try:
    raise PS1Error('foo', 'bar')
except PS1Error as e:
    print(e.pos, e.msg)
