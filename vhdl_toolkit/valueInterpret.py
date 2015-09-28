from python_toolkit.arrayQuery import where
import re


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
    def resolveWidth(context, typeStr):
        if typeStr == 'std_logic':
            return 1
        else:
            m = re.match("std_logic_vector\s*\((.*)downto(.*)\)", typeStr, re.IGNORECASE)
            if not m:
                raise Exception("ValueInterpreter can not resolve width from type string '%s'" % typeStr)
            return int(ValueInterpreter().resolve(context, m.group(1).lower())) - int(ValueInterpreter().resolve(context, m.group(2).lower())) + 1
    
    @staticmethod
    def contextFromGenerics(entity):
        context = {}
        for g in where(entity.generics, lambda x : isinstance(x.defaultVal, int)):
            context[g.name.lower()] = int(g.defaultVal)
        return context
    
    @staticmethod
    def resolveInt(entity, strExpr):
        context = ValueInterpreter.contextFromGenerics(entity) 
        return int(ValueInterpreter().resolve(context, strExpr.lower()))
