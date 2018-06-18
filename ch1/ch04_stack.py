#!/usr/bin/env python
# vim: set fileencoding=utf8
"""
    ch01.cradle
    ~~~~~~~~~~~

    A framework of commonly-used routines for the Let's Build a Compiler (in Python)!
    project, chapter 1.

    :copyright: 2013 by Austin Hastings, see AUTHORS for more details.
    :license: GPL v3+, see LICENSE for more details.
"""
import sys
import io
import pdb

##### Error handling

def abort(msg):
    """
    Report an error and raise a SystemExit exception.
    """
    error(msg)
    sys.exit(1)

def error(msg):
    """
    Report an error. Wrap the message in newlines to separate it from other output.
    """
    sys.stderr.write("\n" + msg + "\n")

def expected(what):
    """
    Report on an input value not present. Abort.
    """
    abort("'%s' expected." % what)

##### Input handling

_input = None
peek = None
"""
Stores the input look-ahead character. This is the next character in the input
stream, and will be returned by get_char().

For those with a 'C' background, using this variable avoids having to deal with
`ungetc()` all the time.
"""

def get_char():
    """
    Advance the input to the next character. Return the character consumed,
    or None. Note that this function changes `Peek`, and returns the *old*
    value of `Peek`.
    """
    global peek
    result = peek
    peek = _input.read(1) if sys.stdin.readable() else None
    return result

def get_number():
    """
    Expect that the next input will be a number. Read and return
    the (single-digit) number. Abort if not found..
    """
    dig = get_char()
    if not dig.isdigit():
        expected('Number')
    return dig

def get_word():
    """
    Expect that the next input will be a word - either an identifier or
    a key word. Read and return the (single-character) word. Abort if
    not found.
    """
    word = get_char()
    if not word.isalpha():
        expected('Word')
    return word

def match(ch):
    """
    Require that the next input read be the character given as a parameter.
    Abort if not found.
    """
    if get_char() != ch:
        expected(ch)

##### Output functions

def emit(text):
    sys.stdout.write(text)

def emit_ln(text):
    sys.stdout.write(text + "\n")

##### Processing

def init(inp=None):
    global _input
    _input = inp
    get_char()

def compile():
    pass


def term():
    emit_ln('MOVE #' + get_number() + ',D0')


def add():
    match('+');
    term();
    # emit_ln('ADD D1,D0');
    emit_ln('ADD (SP)+,D0')


def subtract():
   match('-');
   term();
   # emit_ln('SUB D1,D0');
   emit_ln('SUB (SP)+,D0')
   emit_ln('NEG D0');

def expression():
    term()
    while peek in ['+', '-']:
        # emit_ln('MOVE D0,D1');
        emit_ln('MOVE D0,-(SP)');
        if peek == '+':
            add()
        elif peek == '-':
            subtract()
        else:
            expected('add op')


def main():
    print("Enter your code on a single line. Enter '.' by itself to quit.")
    while True:
        line = input()
        if line == ".":
            break
        init(inp=io.StringIO(line))
        # compile()
        expression()

if __name__ == '__main__':
    main()

