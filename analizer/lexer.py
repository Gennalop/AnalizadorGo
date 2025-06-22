import ply.lex as lex
from logger import create_log_file 

## Reparticion del Trabajo

# 1. Palabras Reservadas 

reserved = {
    'true': 'TRUE',
    'false': 'FALSE',
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'func' : 'FUNC',
    'var' : 'VAR',
    'return' : 'RETURN',
    'switch' : 'SWITCH',
    'case' : 'CASE',
    'default' : 'DEFAULT',
    'type' : 'TYPE',
    'struct' : 'STRUCT',
    'map' : 'MAP',
    'package' : 'PACKAGE',
    'import' : 'IMPORT',
    'nil': 'NIL',
    'continue' : 'CONTINUE',
    'defer' : 'DEFER',
    'break' : 'BREAK',
    'const' : 'CONST',
    'go' : 'GO',
    'select' : 'SELECT',
    'interface' : 'INTERFACE',
    'range' : 'RANGE',
    'fallthrough' : 'FALLTHROUGH',
}

# 2. Lista de tokens (todos coordinan aquí)

tokens = [
    'NUMBER',
    'RUNE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE',
    'AND', 'OR',
    'ASSIGN',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',
    'COMMA', 'SEMICOLON',
    'DOT', 'COLON',
    'IDENTIFIER',
    'DATATYPE',
    'STRING', 'STRING_UNCLOSE',
    'RAW_STRING',
    'DECLARE_ASSIGN',
    'AMPERSAND',
] + list(reserved.values())

# 3. Reglas para variables y tipo de datos 

go_types = {
    'int', 'int8', 'int16', 'int32', 'int64',        
    'float32', 'float64',                            
    'string',                                        
    'bool',                                          
    'rune',                                                                  
}

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    elif t.value in go_types:
        t.type = 'DATATYPE'
    else:
        t.type = 'IDENTIFIER'
    return t

def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    return t

def t_STRING_UNCLOSED(t):
    r'"[^"\n]*'
    print("Error: cadena sin cerrar correctamente")
    t.lexer.skip(len(t.value))

def t_RAW_STRING(t):
    r'\`[^`]*\`'
    return t

#En Go, las comillas simples ('...') se utilizan principalmente para representar caracteres individuales, conocidos como runas
def t_RUNE(t): 
    r"\'([^\\'\n]|(\\.))\'"
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t


# 4. Reglas para operadores 

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD     = r'%'

t_EQ      = r'=='
t_NEQ     = r'!='
t_GT      = r'>'
t_LT      = r'<'
t_GE      = r'>='
t_LE      = r'<='

t_AND     = r'&&'
t_OR      = r'\|\|'

t_ASSIGN  = r'='
t_DECLARE_ASSIGN = r':='

# 5. Reglas para comentarios y delimitadores 

t_AMPERSAND = r'&'

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COMMA     = r',' 
t_SEMICOLON = r';' 
t_DOT       = r'\.' #no es delimitador, sino un operador de acceso
t_COLON     = r':'

def t_COMMENT_UNILINE(t):
    r'//[^\n]*'
    pass

def t_COMMENT_MULTILINE(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

# 6. Reglas comunes 

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0]) 
    t.lexer.skip(1)


# Build the lexer and test----------------------------------------------------------


lexer = lex.lex()
