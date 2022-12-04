import sys
import ply.lex as lex

# List of token names. This is always required
tokens = (
    'INCLUDE', 'HEADER',
    'INT', 'FLOAT',
    'NAME', 'NUMBER'
)

# literals
literals = ['(', ')', '{', '}', ';', ',', '=', '+']

# Regular expression rules for simple tokens
t_INCLUDE   = r'\#include'
t_HEADER    = r'<[A-Za-z0-9_]+(\.h|\.hpp)?>'
t_NAME      = r'[A-Za-z][A-Za-z0-9_]*'

# Ignored characters
t_ignore = ' \t'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_INT(t):
    r'int'
    t.value = 'long'
    return t

def t_FLOAT(t):
    r'float'
    t.value = 'double'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: python %s <input file>" % sys.argv[0])
    fp = open(sys.argv[1], "r")
    if (fp == 0):
        sys.exit("File not open: %s" % sys.argv[1])

    lexer = lex.lex()

    commands = fp.readlines()
    commands = ''.join(commands)
    fp.close()

    lexer.input(commands)

    # process and print each token
    lineno = 1
    lexpos = 0
    while True:
        tok = lexer.token()
        if not tok: break

        # row matching
        num = tok.lineno - lineno
        if num > 0:
            print('\n' * num, end='')
            lineno = tok.lineno
            lexpos += num
            prev = ''

        # column matching
        num = tok.lexpos - lexpos
        if num > 0: print(' ' * num, end='')
        lexpos = tok.lexpos + len(str(tok.value))
        if tok.type in ['INT', 'FLOAT']: lexpos -= 1

        print(tok.value, end='')
