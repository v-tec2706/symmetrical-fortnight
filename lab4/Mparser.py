#!/usr/bin/python

import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('right', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ('nonassoc', 'LEEQ', 'GREQ', 'NOTEQ', 'EQ'),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", 'DOTMUL', 'DOTDIV'),
    ('right', "\'"),
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

    if len(p) == 3:
        p[1].instrs.append(p[2])
        p[0] = p[1]
    else:
        p[0] = AST.Instructions(p[1])


def p_expression(p):
    """expression : initialization
                  | whileConstr
                  | ifConstr
                  | forConstr
                  | simple_func
                  | return
                  """
    p[0] = p[1]

def p_blockOfExpressions(p):
    """blockOfExpressions : expression
                          | '{' expressions '}'"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_expressions(p):
    """expressions : expression
                   | expression expressions"""
    p[0] = p[1]


def p_simple_func(p):
    """simple_func : PRINT to_print ';'
                   | CONTINUE ';'
                   | BREAK ';'"""

    if len(p) == 3:
        p[0] = AST.SimpleFun(p[1])
    else:
        p[0] = AST.Print(p[2])


def p_return(p):
    """return : RETURN exp ';'"""
    p[0] = AST.Return(p[2])


def p_toPrint(p):
    """to_print : var
                | content ',' to_print
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].content.append(p[3])
        p[0] = p[1]


def p_content(p):
     """content : var
     """
     p[0] = AST.Content(p[1])


def p_condition(p):
    """condition : exp '<' exp
                 | exp '>' exp
                 | exp EQ exp
                 | exp LEEQ exp
                 | exp GREQ exp
                 | exp NOTEQ exp"""
    p[0] = AST.Condition(p[1], p[2], p[3])


def p_whileConstr(p):
    """whileConstr : WHILE '(' condition ')' blockOfExpressions
    """
    p[0] = AST.IfWhile(p[1], p[3], p[5])


def p_ifConstr(p):
    """ifConstr : IF '(' condition ')' blockOfExpressions %prec IFX
                | IF '(' condition ')' blockOfExpressions ELSE blockOfExpressions
                | ELSE blockOfExpressions
         """
    if len(p) == 6:
        p[0] = AST.IfWhile(p[1], p[3], p[5])
    elif len(p) == 8:
        p[0] = AST.IfElse(p[3], p[5], p[7])
    else:
        p[0] = AST.Else(p[2])

def p_for(p):
    """forConstr : FOR ID '=' var ':' var blockOfExpressions"""
    p[0] = AST.For(p[2], p[4], p[6], p[7])

def p_var(p):
    """var : number
           | ID"""

    p[0] = AST.Var(p[1])

def p_element(p):
    """element  :  number
                | STRING """
    p[0] = p[1]

def p_init_num_str(p):
    """initialization : ID '=' element ';'
    """

    p[0] = AST.VarAssignment(p[1], p[3])

def p_init_funct(p):
    """initialization : ID '=' ZEROS '(' elements ')' ';'
                    | ID '=' ONES '(' elements ')' ';'
                    | ID '=' EYE '(' elements ')' ';'"""

    p[0] = AST.assignSpec(p[1], p[3], p[5])


def p_init_elems(p):
    """initialization : ID '=' '[' vectors ']' ';'
                      | ID '=' '[' elements ']' ';'
                      | exact_pos '=' number ';'"""
    if len(p) > 5:
        p[0] = AST.VectorAssignment(p[1], p[4])
    else:
        p[0] = AST.ExactPosVal(p[1], p[3])

def p_exact_pos(p):
    """exact_pos : ID '[' elements ']' """
    p[0] = AST.ExactPos(p[1], p[3])


def p_number(p):
    """number : INTNUM
              | FLOATNUM"""
    p[0] = p[1]


def p_vector(p):
    """vector  : '[' elements ']'
    """

    p[0] = AST.Vector(p[2])

def p_vectors(p):
    """vectors : vectors ',' vector
               | vector"""

    if len(p) == 2:
        p[0] = AST.Vectors(p[1])
    else:
        p[1].vectors.append(p[3])
        p[0] = AST.Vectors(p[1])


def p_init_operation(p):
    """initialization : ID '=' operation ';'
                      | ID ADDASSIGN operation ';'
                      | ID SUBASSIGN operation ';'
                      | ID MULASSIGN operation ';'
                      | ID DIVASSIGN operation ';'"""

    p[0] = AST.OperationAssignment(p[1], p[2], p[3])

def p_exp(p):
    """exp : var
           | operation
           | STRING"""
    p[0] = p[1]

def p_operation(p):
    """operation : exp '+' exp
                 | exp '-' exp
                 | exp '*' exp
                 | exp '/' exp
                 | exp DOTADD exp
                 | exp DOTSUB exp
                 | exp DOTMUL exp
                 | exp DOTDIV exp
                 | '-' exp
                 | exp "\'"

    """
    if len(p) == 4:
        p[0] = AST.TwoVarOperation(p[1], p[2], p[3])
    else:
        p[0] = AST.SingleVarOperation(p[1], p[2])


def p_elements(p):
    """elements : elements ',' element
                | element
    """

    if len(p) == 2:
        p[0] = AST.Elements(p[1])
    else:
        p[1].elements.append(p[3])
        p[0] = p[1]


parser = yacc.yacc()