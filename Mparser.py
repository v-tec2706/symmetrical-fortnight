#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens


precedence = (
   ('nonassoc', 'IF'),
   ('nonassoc', 'ELSE'),
   ('right', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
   ('nonassoc', 'LEEQ', 'GREQ', 'NOTEQ', 'EQ'),
   ("left", 'DOTADD', 'DOTSUB'),
   ("left", 'DOTMUL', 'DOTDIV'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')"
              .format(p.lineno, scanner.find_column(p.lexer.lexdata, p),
                      p.type, p.value))
    else:
        print("Unexpected end of input")


def p_start(p):
    """start : expression
             | start expression"""

def p_expression(p):
    """expression : initialization
                  | assign"""

# initialization
def p_init_num_str(p):
    """initialization : ID '=' number ';'
                      | ID '=' STRING ';'"""

def p_init_operation(p):
    """initialization : ID '=' operation ';'"""

def p_operation_sum(p):
    """operation : var '+' var
                 | var '-' var"""


def p_operation_dot_sum(p):
    """operation : var DOTADD var
                 | var DOTSUB var
                 | var DOTMUL var
                 | var DOTDIV var"""


def p_operation_mul(p):
    """operation : var '*' var
                 | var '/' var"""


def p_var(p):
    """var : number
           | ID """

def p_unary_op(p):
    """operation : '-' var
                 | var "\'" """

def p_init_funct(p):
    """initialization : ID '=' special_func ';'"""

def p_spec_fun(p):
    """special_func : ZEROS '(' INTNUM ')'
                    | ONES '(' INTNUM ')'
                    | EYE '(' INTNUM ')'"""


def p_init_elems(p):
    """initialization : ID '=' matrix ';'
                      | exact_pos '=' number ';'"""

def p_exact_pos(p):
    """exact_pos : ID '[' INTNUM ',' INTNUM ']' """


def p_number(p):
    """number : INTNUM
              | FLOATNUM"""


def p_matrix(p):
    """matrix : '[' elements ']'
              | '[' matrix ']'"""


def p_element(p):
    """elements : number ',' elements
                | number ';' elements
                | number
                | empty"""

def p_assign(p):
    """assign : ID ADDASSIGN var ';'
              | ID SUBASSIGN var ';'
              | ID MULASSIGN var ';'
              | ID DIVASSIGN var ';'"""


def p_condition(p):
    """condition : var '<' var
                 | var '>' var
                 | var EQ var
                 | var LEEQ var
                 | var GREQ var
                 | var NOTEQ var"""
def p_empty(p):
    'empty :'
    pass

parser = yacc.yacc()

