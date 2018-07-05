import sys

from io import StringIO

_look = None
_input = None

def get_char():
    """get a char to look"""
    global _look
    _look = _input.read(1) if sys.stdin.readable() else None


def error(s):
    """
    report an error
    """
    sys.stderr.write("\n" + s + "\n")


def abort(s):
    """
    report an error and raise a exception
    """
    error(s)
    sys.exit(1)
    pass


def expected(s):
    """
    report on an input value not present
    """
    abort("'%s' expected." % s)

def match(ch):
    """
    require that the next input read be the character given as a parameter.
    abort if not found.
    """
    if _look == ch:
        get_char()
    else:
        expected(ch)


def is_alpha(c):
    """judge is a char"""
    return (c.upper() >= 'A' and c.upper() <= 'Z')


def is_digit(c):
    """judge is a digit"""
    return c >= '0' and c <= '9'


def get_name():
    """get a name"""
    global _look
    if not is_alpha(_look):
        expected('Name')
    result = _look.upper()
    get_char()
    return result


def get_num():
    """get a number"""
    global _look
    if not is_digit(_look):
        expected('Integer')
    result = _look
    get_char()
    return result


def emit(s):
    sys.stdout.write(s)


def emit_ln(s):
    emit(s + '\n')


def init(inp=None):
    global _input
    _input = inp
    get_char()

def term():
    emit_ln('MOVE #' + get_num() + ',D0')


def add():
    match('+')
    term()
    emit_ln('ADD D1,D0')


def subtract():
    match('-')
    term()
    emit_ln('SUB D1,D0')
    emit_ln('NEG D0');


def expression():
    term()
    while _look in ['+', '-']:
        emit_ln('MOVE D0,D1')
        if _look == '+':
            add()
        elif _look == '-':
            subtract()
        else:
            expected('Addop')


def main():
    print("Enter your code on a single line. Enter '.' by itself to quit.")
    while True:
        line = input()
        if line == ".":
            break
        init(inp=StringIO(line))
        expression()


if __name__ == '__main__':
    main()

