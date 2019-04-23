import ply.lex as lex

#list of reserved words
reserved = {
    'if': 'IF',
    'for': 'FOR',
  #  'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

# List of token names
tokens = [
    'ID',
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'LEEQ',
    'GREQ',
    'NOTEQ',
    'EQ',
    'INTNUM',
    'FLOATNUM',
    'STRING',

] + list(reserved.values())

t_DOTADD = '.\+'
t_DOTSUB = '.-'
t_DOTMUL = '.\*'
t_DOTDIV = './'
t_ADDASSIGN = '\+='
t_SUBASSIGN = '-='
t_MULASSIGN = '\*='
t_DIVASSIGN = '/='
t_LEEQ = '<='
t_GREQ = '>='
t_NOTEQ = '!='
t_EQ = '=='

#literals
literals = "<>=+-*/()[]{}:',;"

# Regular expression rules
def t_STRING(t):
    r'".*?"'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_FLOATNUM(t):
    r'\d*\.\d+ | \d+\.'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return  t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore  = ' \t'


def t_error(t):
    print("(%d) Illegal character '%s'." % (t.lineno, t.value[0]))
    t.lexer.skip(1)


def t_COMMENT(t):
    r'\#.*'
    pass


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Build the lexer
lexer = lex.lex()
