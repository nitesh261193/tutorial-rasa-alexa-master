#!/usr/bin/python import sys
import os
import re

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.items())
    enums['key'] = reverse
    return type('Enum', (), enums)

Type = enum(
    'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD', 'EXP', 'FAC',
    'FUNC', 'VAR', 'NUMBER', 'LBRACE', 'RBRACE'
)

class Token(object):
    def __init__(self, type, alias, value):
        self.type = type
        self.alias = alias
        self.value = value

    def __str__(self):
        return '{2} <{1}>'.format(self.type, self.alias, self.value)

class Lexer(object):
    def __init__(self, stream):
        # Initialize class attributes ... 		self.stream = stream
        self.current = None
        self.offset = -1
        self.matchRes = None

        # ... and get the first character. 		self.getChar()

    def nextToken(self):
        if self.current is None:
            return None

        self.skipWhitespaces()

        if self.current == '+' and self.lookbefore() not in ('+','-','^','/','%'):
            return Token(Type.PLUS, Type.key[Type.PLUS], self.getChar())
        elif self.current == '-' and self.lookbefore() not in ('+','-','^','/','%'):
            return Token(Type.MINUS, Type.key[Type.MINUS], self.getChar())
        elif self.current == '*':
            return Token(Type.TIMES, Type.key[Type.TIMES], self.getChar())
        elif self.current == '/':
            return Token(Type.DIV, Type.key[Type.DIV], self.getChar())
        elif self.current == '%':
            return Token(Type.MOD, Type.key[Type.MOD], self.getChar())
        elif self.current == '^':
            return Token(Type.EXP, Type.key[Type.EXP], self.getChar())
        elif self.current == '!':
            return Token(Type.FAC, Type.key[Type.FAC], self.getChar())
        elif self.current == '(':
            return Token(Type.LBRACE, Type.key[Type.LBRACE], self.getChar())
        elif self.current == ')':
            return Token(Type.RBRACE, Type.key[Type.RBRACE], self.getChar())
        elif self.match('[a-zA-Z_][a-zA-Z0-9_]*(?=([ \t]+)?\()'):
            return Token(Type.FUNC, Type.key[Type.FUNC], self.getMatch())
        elif self.match('[+-]?[a-zA-Z_][a-zA-Z0-9_]*(?!([ \t]+)?\()'):
            return Token(Type.VAR, Type.key[Type.VAR], self.getMatch())
        elif self.match('[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'):
            return Token(Type.NUMBER, Type.key[Type.NUMBER], self.getMatch())
        else:
            print ('No match found')

    def skipWhitespaces(self):
        while self.current.isspace():
            self.getChar()

    def getChar(self):
        if self.offset + 1 >= len(self.stream):
            return None

        result = self.stream[self.offset]
        self.offset += 1
        self.current = self.stream[self.offset]

        return result

    def getMatch(self):
        if self.matchRes is None:
            return None

        result = self.matchRes.group(0)
        self.offset += len(result)

        if self.offset + 1 >= len(self.stream):
            self.current = None
        else:
            self.current = self.stream[self.offset]

        return result

    def match(self, format):
        # Prepare the given pattern ... 		pattern = re.compile(format)

        # ... and match the pattern against the stream. 		self.matchRes = re.match(pattern, self.stream[self.offset:])

        if self.matchRes is not None:
            return True
        else:
            return False

    def lookahead(self):
        return self.stream[self.offset+1:self.offset+2]

    def lookbefore(self):
        return self.stream[self.offset-1:self.offset]

def main(form):
    if form is not None:
        lex = Lexer(form)
        token = lex.nextToken()
        while token is not None:
            print (token)
            token = lex.nextToken()






