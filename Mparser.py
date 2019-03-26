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
             | blockOfExpressions
             | start blockOfExpressions
             | start expression"""


def p_expression(p):
    """expression : initialization
                  | assign
                  | construction
                  | simple_func
                  """


def p_simple_func(p):
    """simple_func : PRINT to_print ';'
                   | return ';'
                   | CONTINUE ';'
                   | BREAK ';'"""

def p_return(p):
    """return : RETURN comparison"""


def p_toPrint(p):
    """to_print : content
                | content ',' to_print
    """

def p_content(p):
    """content : STRING
               | var
    """

def p_condition(p):
    """condition : comparison '<' comparison
                 | comparison '>' comparison
                 | comparison EQ comparison
                 | comparison LEEQ comparison
                 | comparison GREQ comparison
                 | comparison NOTEQ comparison"""

def p_comparison(p):
    """comparison : var
                  | operation"""


def p_construction(p):
    """construction : ifConstr
                    | whileConstr
                    | forConstr"""


def p_whileConstr(p):
    """whileConstr : WHILE '(' condition ')' blockOfExpressions
    """

def p_ifConstr(p):
     """ifConstr : singleIf
                 | singleIf else
                 | singleIf elseIfs
                 """


def p_elseIfs(p):
    """elseIfs : ELSE IF '(' condition ')' blockOfExpressions
               | ELSE IF '(' condition ')' blockOfExpressions elseIfs
               | ELSE IF '(' condition ')' blockOfExpressions else
    """

def p_else(p):
    """else : ELSE blockOfExpressions"""

def p_singleIf(p):
    """singleIf : IF '(' condition ')' blockOfExpressions"""


def p_for(p):
    """forConstr : FOR ID '=' var ':' var blockOfExpressions"""

def p_var(p):
    """var : number
           | ID"""


def p_blockOfExpressions(p):
    """blockOfExpressions : expression
                          | '{' expressions '}'"""


def p_expressions(p):
    """expressions : expression
                   | expression expressions"""


def p_init_num_str(p):
    """initialization : ID '=' number ';'
                      | ID '=' STRING ';'"""



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

def p_init_operation(p):
    """initialization : ID '=' operation ';'"""



def p_operation(p):
    """operation : var '+' var
                 | var '-' var
                 | var '*' var
                 | var '/' var
    """

def p_unary_op(p):
    """operation : '-' var
                 | var "\'" """



def p_dot_operation(p):
    """operation : var DOTADD var
                 | var DOTSUB var
                 | var DOTMUL var
                 | var DOTDIV var
    """

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

def p_empty(p):
    'empty :'
    pass


parser = yacc.yacc()

