import sys

from io import StringIO

_look = None
_input = None
table = {}

def read():
    return _input.read(1) if sys.stdin.readable() else None

def get_char():
    """get a char to look"""
    global _look
    _look = read()


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


def is_addop(c):
    return c in ['-', '+']


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
    result = ord(_look) - ord('0')
    get_char()
    return result


def get_num():
    global _look
    value = 0
    if not is_digit(_look):
        expected('Integer')
    while is_digit(_look):
        value = value * 10 + ord(_look) - ord('0')
        get_char()
    return value


def emit(s):
    sys.stdout.write(s)


def emit_ln(s):
    emit('{}\n'.format(s))


def init_table():
    global table
    for i in range(0, ord('Z') - ord('A')):
        table[chr(i + ord('A'))] = 0

def factor():
    global _look
    if _look == '(':
        match('(')
        value = expression()
        match(')')
    elif is_alpha(_look):
        value = table[get_name()]
    else:
        value = get_num()
    return value


def term():
    global _look
    value = factor()
    while _look in ['*', '/']:
        if _look == '*':
            match('*')
            value = value * factor()
        if _look == '/':
            match('/')
            value = value / factor()
    return value


def expression():
    global _look
    if is_addop(_look):
        value = 0
    else:
        value = term()
    while is_addop(_look):
        if _look == '+':
            match('+')
            value = value + term()
        if _look == '-':
            match('-')
            value = value - term()
    return value


def assignment():
    name = get_name()
    match('=')
    table[name] = expression()


def init(inp=None):
    global _input
    _input = inp
    get_char()


def my_input():
    global _table
    match('?')
    table[get_name()] = read()


def ouput():
    global _table
    match('!')
    emit_ln(table[get_name()])


def main():
    init_table()
    print("Enter your code on a single line. Enter '.' by itself to quit.")
    while True:
        line = input()
        if line == ".":
            break
        init(inp=StringIO(line))
        if _look == '?':
            my_input()
        elif _look == '!':
            ouput()
        else:
            assignment()


if __name__ == '__main__':
    main()

