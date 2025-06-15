import ply.lex as lex
from logger import create_log_file 

# 1. Palabras Reservadas (Integrante 2)
reserved = {
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
    'map' : 'MAP'
}

# 2. Lista de tokens (todos coordinan aquí)
tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE',
    'AND', 'OR',
    'ASSIGN',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',
    'COMMA', 'SEMICOLON',
    'DOT', 'COLON',
    'IDENTIFIER','MOD',
] + list(reserved.values())

# 3. Reglas para variables y tipo de datos (Integrante 1)
go_types = {
    'int', 'int8', 'int16', 'int32', 'int64',        
    'float32', 'float64',                            
    'string',                                        
    'bool',                                          
    'rune',                                                                  
}

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in go_types:
        t.type = 'TYPE'
    else:
        t.type = 'IDENTIFIER'
    return t

def t_INVALID_IDENTIFIER(t):
    r'[0-9][a-zA-Z0-9_]*|[a-zA-Z0-9_]*[\s\-\!\@\#\$\^\&\*\(\)]+[a-zA-Z0-9_]*'
    message = f"[ERROR] Invalid identifier: '{t.value}' at line {t.lineno}\n"
    log_file.write(message)
    print(message.strip())
    t.lexer.skip(len(t.value))

# 4. Reglas para operadores (Integrante 2)
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

# 5. Reglas para comentarios y delimitadores (Integrante 3)
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

# 6. Reglas comunes (Integrante 3)
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    message = f"[ERROR] Unexpected character '{t.value[0]}' at line {t.lineno}\n"
    log_file.write(message)
    print("Illegal character '%s'" % t.value[0]) 
    t.lexer.skip(1)


# Build the lexer and test----------------------------------------------------------
lexer = lex.lex()

log_file = create_log_file("gituser") #CAMBIAR A NOMBRE DE SU USUARIO GIT 

#data = 
"""
func main() {

	// Comentario de una línea
	/*
	Comentario de múltiples líneas
	Este programa evalúa varias estructuras de Go.
	*/
}""" #TEXTO A PROBAR

with open("testing_algorithms/algorithm2.go", "r", encoding="utf-8") as f:
    data = f.read()

lexer.input(data)
  
while True:
    tok = lexer.token()
    if not tok:
        break
    message = f"[LEXTOKEN] {tok.type} -> '{tok.value}' (line {tok.lineno}, pos {tok.lexpos})\n"
    log_file.write(message)
    print(tok)

log_file.close()