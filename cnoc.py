"""
CNOC - contains no contains
simple language for AND-ing, OR-ing and NOT-ing string matches

("something" or not ("anotherthing" and "anything"))
see tests
"""

class CnocException(Exception): pass

reserved = {
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
}

tokens = ['LPAREN','RPAREN', 'ID', 'STR'] + list(reserved.values())

# Tokens
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

def t_ID(t):
    r'(and|or|not)'
    t.type = reserved.get(t.value)
    return t

def t_STR(t):
    r'"[^\"]+"'
    return t

# Ignored characters
t_ignore = " \t"

def t_error(t):
    raise CnocException("CNOC erorr: Illegal character '%s'"%t.value[0], t)
    #t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

class Node(object):
    def string(self):
        u = str(self)
        if u[0] == '(' and u[-1] == ')': return u[1:-1]
        return u

class BinOp(Node):
    def __init__(self, a, b):
        assert isinstance(a, Node) and isinstance(b, Node)
        self.a, self.b = a, b
    def __str__(self):
        return u'(%s %s %s)'%(self.a, self.name, self.b)

class And(BinOp):
    name = 'and'
    def run(self, content):
        return self.a.run(content) and self.b.run(content)

class Or(BinOp):
    name = 'or'
    def run(self, content):
        return self.a.run(content) or self.b.run(content)

class Not(Node):
    def __init__(self, a):
        assert isinstance(a, Node)
        self.a = a
    def __str__(self): return u'not %s'%self.a
    def run(self, content):
        return not self.a.run(content)

class Str(Node):
    def __init__(self, data):
        self.data = data
    def run(self, content):
        return self.data.lower() in content.lower()
    def __str__(self):
        return '"%s"'%self.data

precedence = (
    ('left', 'AND', 'OR'),
    ('right', 'NOT',),
)

def p_expression_not(t):
    'expression : NOT expression'
    if t[1] == 'not': t[0] = Not(t[2])
    else:
        raise CnocException('CNOC error: unknown operator "%s"'%t[2])

def p_expression_binop(t):
    '''expression : expression AND expression
                  | expression OR expression'''
    if t[2] == 'and': t[0] = And(t[1], t[3])
    elif t[2] == 'or': t[0] = Or(t[1], t[3])
    else:
        raise CnocException('CNOC error: unknown binary operator "%s"'%t[2])

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_str(t):
    'expression : STR'
    t[0] = Str(t[1].strip('"'))

def p_error(t):
    if not t:
        raise CnocException('CNOC error: Expecting node or right parenthesis but end of input', t)
    elif t.type == 'AND' or t.type == 'OR':
        raise CnocException('CNOC error: Operation %s missing first operand'%t.type, t)
    elif t.type == 'RPAREN':
        raise CnocException('CNOC error: Too many right parenthesis', t)
    raise CnocException('CNOC error: Unexpected error at %s'%t, t)

import ply.yacc as yacc
compiler = yacc.yacc()

def match(expression, content):
    node = compiler.parse(expression)
    return node.run(content)
