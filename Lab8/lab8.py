import sys
import ply.yacc as yacc
import ply.lex as lex


tokens = (
    'NAME', 'NUMBER',
)

literals = ['=', '>', '<', '+', '-', '*', '/', '(', ')']

# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t\n"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Parsing rules

#TODO: define precedence
precedence = (
    ('left','<','>'),
    ('left', '+', '-'),
    ('left', '*', '/')
)


def p_statement_assign(p):
    '''statement : assign expression'''
    print(":=")

def p_assign_seen(p):
    '''assign : NAME "="'''
    print("lvalue %s" % (p[1]))

def p_statement_expr(p):
    'statement : expression'

def p_expression_number(p):
    "expression : NUMBER"
    print("push %d" % (p[1]))


def p_expression_name(p):
    "expression : NAME"
    print("rvalue %s" % (p[1]))

#TODO: define additional rules
def p_expression_plus(p):
    "expression : expression '+' expression"
    print("+")
def p_expression_minus(p):
    "expression : expression '-' expression"
    print("-")

def p_expression_times(p):
    "expression : expression '*' expression"
    print("*")

def p_expression_divide(p):
    "expression : expression '/' expression"
    print("/")

def p_expression_greator(p):
    "expression : expression '<' expression"
    print("<")

def p_expression_less(p):
    "expression : expression '>' expression"
    print(">")

def p_expresion_parenthesis(p):
    "expression : '(' expression ')'"

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: python %s <input file>" % sys.argv[0])
    fp = open(sys.argv[1], "r")
    if (fp == 0):
        sys.exit("File not open: %s" % sys.argv[1])

    lexer = lex.lex()
    parser = yacc.yacc()

    for line in fp:
        print("Translating \"%s\"" % (line[:-1]))
        parser.parse(line)
        print("")
