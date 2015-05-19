#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ply.lex as lex

tokens = (
    'WHILE', 'THEN', 'ENTITY', 'END', 'NAME', 'FLOAT', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'DDOT', 'SEMICOLON',
    'L_OR_EQ','NONEQUALS', 'G_OR_EQ', 'CONNECT', 'GREATER', 'LESSER', 'COMMA',
    'LPAREN', 'RPAREN', 'DOWNTO', 'TO', 'LIBRARY',
    'IN', 'OUT', 'USE', 'IS', 'ARCHITECTURE', 'BEGIN', 'MAP', 'PORT',
    'COMPONENT', 'COMMENT', 'STRING', 'PROCESS', "LENOP", "HIGH", "LOW"
    )

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_DDOT = r':'
t_LENOP = "'"
t_SEMICOLON = r';' 
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_NONEQUALS = r'/='
t_GREATER = r'>'
t_LESSER = r'<'
t_L_OR_EQ = r'<='
t_G_OR_EQ = r'>='
t_CONNECT = r'=>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_FLOAT = r'[0-9]*\.[0-9]*'
t_NUMBER = r'\d+'
t_COMMA = r','
t_HIGH = r"'1'"
t_LOW = r"'0'"

def t_COMMENT(t):
    r'--.*'

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_LIBRARY(t):
    r'(?i)LIBRARY(?!\S)'
    return t

def t_PROCESS(t):
    r'(?i)PROCESS(?!\S)'
    return t

def t_IN(t):
    r'(?i)IN(?!\S)'
    return t

def t_OUT(t):
    r'(?i)OUT(?!\S)'
    return t

def t_USE(t):
    r'(?i)USE(?!\S)'
    return t

def t_ENTITY(t):
    r'(?i)ENTITY(?!\S)'
    return t

def t_IS(t):
    r'(?i)IS(?!\S)'
    return t

def t_ARCHITECTURE(t):
    r'(?i)ARCHITECTURE(?!\S)'
    return t

def t_BEGIN(t):
    r'(?i)BEGIN(?!\S)'
    return t

def t_MAP(t):
    r'(?i)MAP(?!\S)'
    return t

def t_PORT(t):
    r'(?i)PORT(?!\S)'
    return t

def t_COMPONENT(t):
    r'(?i)COMPONENT(?!\S)'
    return t

def t_DOWNTO(t):
    r'(?i)DOWNTO(?!\S)'
    return t

def t_TO(t):
    r'(?i)TO(?!\S)'
    return t

def t_WHILE(t):
    r'(?i)WHILE(?!\S)'
    return t

def t_THEN(t):
    r'(?i)THEN(?!\S)'
    return t

def t_END(t):
    r'(?i)END(?!\S)'
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
    
VHDL_Lex_parser = lex.lex()