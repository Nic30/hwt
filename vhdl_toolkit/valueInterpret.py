from python_toolkit.arrayQuery import where


class InterpreterErr(Exception):
    pass


tokens = (
    'NAME', 'NUMBER',
    )

literals = ['=', '+', '-', '*', '/', '(', ')']


result = None

# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

    
def t_error(t):
    raise InterpreterErr("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    global result
    result = p[1]

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        raise InterpreterErr("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        raise InterpreterErr("Syntax error at '%s'" % p.value)
    else:
        raise InterpreterErr("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc()

class  ValueInterpreter:
    def resolve(self, context, exprStr):
        global result
        global names
        names = context
        parser.parse(exprStr)
        return result

    @staticmethod
    def contextFromGenerics(entity):
        context = {}
        for g in where(entity.generics, lambda x : x.defaultVal.type == "NUMBER"):
            context[g.name.lower()] = int(g.defaultVal.value)
        return context
    
    @staticmethod
    def resolveInt(entity, strExpr):
        context = ValueInterpreter.contextFromGenerics(entity) 
        return int(ValueInterpreter().resolve(context, strExpr.lower()))
