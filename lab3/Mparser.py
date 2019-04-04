#!/usr/bin/python

import scanner
import ply.yacc as yacc
import AST

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
    """start : blockOfExpressions
             | start blockOfExpressions
             """

    if len(p) == 2:
        p[0] = p[1]



def p_expression(p):
    """expression : initialization
                  | assign
                  | construction
                  | simple_func
                  """
    p[0] = p[1]


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
                    | ifConstr construction"""

def p_while_construction(p):
    """construction : whileConstr
                    | whileConstr construction"""

def p_for_construction(p):
    """construction :  forConstr
                    | forConstr construction
                    """


# def p_construction(p):
#     """construction : ifConstr
#                     | whileConstr
#                     | forConstr
#                     """


def p_whileConstr(p):
    """whileConstr : WHILE '(' condition ')' blockOfExpressions
    """


def p_ifConstr(p):
    """ifConstr : IF '(' condition ')' blockOfExpressions
                | IF '(' condition ')' blockOfExpressions ELSE blockOfExpressions
                | ELSE IF blockOfExpressions
                | ELSE blockOfExpressions
         """


# def p_ifConstr(p):
#     """ifConstr : singleIf
#                 | singleIf else
#                 | singleIf elseIfs
#                 """
#
#
# def p_elseIfs(p):
#      """elseIfs : ELSE IF '(' condition ')' blockOfExpressions
#                | ELSE IF '(' condition ')' blockOfExpressions elseIfs
#                | ELSE IF '(' condition ')' blockOfExpressions else
#     """
#
# def p_else(p):
#     """else : ELSE blockOfExpressions"""
#
# def p_singleIf(p):
#     """singleIf : IF '(' condition ')' blockOfExpressions %prec IF"""


def p_for(p):
    """forConstr : FOR ID '=' var ':' var blockOfExpressions"""

def p_var(p):
    """var : number
           | ID"""

    p[0] = p[1]


def p_blockOfExpressions(p):
    """blockOfExpressions : expression
                          | '{' expressions '}'"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST.Bracket(p[1], p[2], p[3])




def p_expressions(p):
    """expressions : expression
                   | expression expressions"""
    p[0] = p[1]


def p_init_num_str(p):
    """initialization : ID '=' number ';'
                      | ID '=' STRING ';'"""

    p[0] = AST.VarAssignment(p[1], p[3])

def p_init_funct(p):
    """initialization : ID '=' ZEROS '(' INTNUM ')' ';'
                    | ID '=' ONES '(' INTNUM ')' ';'
                    | ID '=' EYE '(' INTNUM ')' ';'"""

    p[0] = AST.assignSpec(p[1], p[3], p[5])


def p_init_elems(p):
    """initialization : ID '=' matrix ';'
                      | exact_pos '=' number ';'"""


def p_exact_pos(p):
    """exact_pos : ID '[' INTNUM ',' INTNUM ']' """
    p[0] = AST.ExactPos(p[1],p[3],p[5])


def p_number(p):
    """number : INTNUM
              | FLOATNUM"""
    p[0] = p[1]


def p_matrix(p):
    """matrix : '[' elements ']'
              | '[' matrix ']'"""

def p_init_operation(p):
    """initialization : ID '=' operation ';'"""
    p[0] = AST.OperationAssignment(p[1], p[3])


def p_operation(p):
    """operation : var '+' var
                 | var '-' var
                 | var '*' var
                 | var '/' var
    """
    p[0] = AST.TwoVarOperation(p[1], p[2], p[3])

def p_dot_operation(p):
    """operation : var DOTADD var
                 | var DOTSUB var
                 | var DOTMUL var
                 | var DOTDIV var
    """
    p[0] = AST.TwoVarOperation(p[1], p[2], p[3])


def p_unary_op(p):
    """operation : '-' var
                 | var "\'" """


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

    p[0] = AST.Assignment(p[1], p[2], p[3])

def p_empty(p):
    'empty :'
    pass


parser = yacc.yacc()
