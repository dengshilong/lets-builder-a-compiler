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


def is_al_num(c):
    return is_alpha(c) or is_digit(c)


def get_name():
    """get a name"""
    global _look
    token = ''
    if not is_alpha(_look):
        expected('Name')
    while is_al_num(_look):
        token += _look.upper()
        get_char()
    return token


def get_num():
    """get a number"""
    global _look
    value = ''
    if not is_digit(_look):
        expected('Integer')
    while is_digit(_look):
        value += _look
        get_char()
    return value


def emit(s):
    sys.stdout.write(s)


def emit_ln(s):
    emit(s + '\n')


def init(inp=None):
    global _input
    _input = inp
    get_char()


def ident():
    name = get_name()
    if _look == '(':
        match('(')
        match(')')
        emit_ln('BSR ' + name)
    else:
        emit_ln('MOVE ' + name + '(PC),D0')


def factor():
    if _look == '(':
        match('(')
        expression()
        match(')')
    elif is_alpha(_look):
        ident()
    else:
        emit_ln('MOVE #' + get_num() + ',D0')


def multiply():
    match('*')
    factor()
    emit_ln('MULS (SP)+,D0')


def divide():
    match('/')
    factor()
    emit_ln('MOVE (SP)+,D1')
    emit_ln('DIVS D1,D0')


def is_addop(c):
    return c in ['-', '+']


def term():
    factor()
    while _look in ['*', '/']:
        emit_ln('MOVE D0,-(SP)')
        if _look == '*':
            multiply()
        elif _look == '/':
            divide()
        else:
            expected('Mulop')


def add():
    match('+')
    term()
    emit_ln('ADD (SP)+,D0')


def subtract():
    match('-')
    term()
    emit_ln('SUB (SP)+,D0')
    emit_ln('NEG D0')


def expression():
    if is_addop(_look):
        emit_ln('CLR D0')
    else:
        term()
    while is_addop(_look):
        emit_ln('MOVE D0,-(SP)')
        if _look == '+':
            add()
        elif _look == '-':
            subtract()
        else:
            expected('Addop')


def assignment():
    name = get_name()
    match('=')
    expression()
    emit_ln('LEA ' + name + '(PC),A0')
    emit_ln('MOVE D0,(A0)')


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

