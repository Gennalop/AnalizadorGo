import ply.lex as lex
from .logger import create_log_file

errors = []

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
    'main' : 'MAIN'
}

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
    'STRING', 'STRING_UNCLOSED', 'RAW_STRING',
    'DECLARE_ASSIGN',
    'AMPERSAND',
] + list(reserved.values())

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
    print("Error: String not properly closed")
    global errors
    col = calcular_columna(t.lexer.lexdata, t.lexpos)
    errors.append(TokenInfo(t.value, t.type, t.lineno, col, category="error"))
    #return t
    #t.lexer.skip(len(t.value))

def t_RAW_STRING(t):
    r'\`[^`]*\`'
    return t

def t_RUNE(t): 
    r"\'([^\\'\n]|(\\.))\'"
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = ('float64', float(t.value))
    else:
        t.value = ('int', int(t.value))
    return t

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

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    global errors
    col = calcular_columna(t.lexer.lexdata, t.lexpos)
    errors.append(TokenInfo(t.value[0], "ILLEGAL_CHARACTER", t.lineno, col, category="error"))
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
# Build the lexer and test----------------------------------------------------------

class TokenInfo:
    def __init__(self, lexema, tipo, linea, columna, category="token"):
        self.lexema = lexema
        self.tipo = tipo
        self.linea = linea
        self.columna = columna
        self.category = category

def calcular_columna(input_text, lexpos):
    last_newline = input_text.rfind('\n', 0, lexpos)
    if last_newline < 0:
        columna = lexpos + 1
    else:
        columna = lexpos - last_newline
    return columna

def lexer_analyze(code):
    global errors
    lexer.lineno = 1
    errors = []
    lexer.input(code)
    tokens = []
    while True:
        t = lexer.token()
        if not t:
            break
        col = calcular_columna(code, t.lexpos)
        tokens.append(TokenInfo(t.value, t.type, t.lineno, col, category="token"))
    return tokens, errors

if __name__ == "__main__":
    lexer = lex.lex()
    log_file = create_log_file("gitUser")
    with open("testing_algorithms/algorithm#.go", "r", encoding="utf-8") as f:
        data = f.read()

    #tokens, _ = analizar_lexico(data)
    #for token in tokens:
    #    message = f"[LEXTOKEN] {token.tipo} -> '{token.lexema}' (line {token.linea}, pos {token.columna})\n"
    #    log_file.write(message)
    #    print(token.tipo, token.lexema, token.linea, token.columna)

    log_file.close()
