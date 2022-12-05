import sys
import ply.lex as lex
import ply.yacc as yacc

tokens = ('BEGIN', 'DIR')

t_BEGIN = r'B'
t_DIR = r'[ENWS]'

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def p_seq_b(p):
    """seq : BEGIN"""
    p[0] = (0, 0)

def p_seq_instr(p):
    """seq : seq instr"""
    p[0] = tuple(sum(x) for x in zip(p[1], p[2]))

def p_instr_move(p):
    """instr : DIR"""
    if p[1] == 'E': p[0] = (1, 0)
    elif p[1] == 'N': p[0] = (0, 1)
    elif p[1] == 'W': p[0] = (-1, 0)
    elif p[1] == 'S': p[0] = (0, -1)
    else: return

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: python %s <input file>" % sys.argv[0])
    fp = open(sys.argv[1], "r")
    if (fp == 0):
        sys.exit("File not open: %s" % sys.argv[1])

    lexer = lex.lex()
    parser = yacc.yacc()
    for line in fp:
        result = parser.parse(line)
        print(result)
