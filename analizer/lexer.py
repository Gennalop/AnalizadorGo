import ply.lex as lex
from logger import create_log_file 

# 1. Palabras Reservadas (Integrante 2)


# 2. Lista de tokens (todos coordinan aquí)
tokens = ()


# 3. Reglas para variables y tipo de datos (Integrante 1)


# 4. Reglas para operadores (Integrante 2)


# 5. Reglas para comentarios y delimitadores (Integrante 3)


# 6. Reglas comunes (Integrante 3)
def t_error(t):
    message = f"[ERROR] Unexpected character '{t.value[0]}' at line {t.lineno}\n"
    log_file.write(message)
    print("Illegal character '%s'" % t.value[0]) 
    t.lexer.skip(1)


# Build the lexer and test----------------------------------------------------------
lexer = lex.lex()

log_file = create_log_file("gitUser") #CAMBIAR A NOMBRE DE SU USUARIO GIT 

data = '' #TEXTO A PROBAR
lexer.input(data)
  
while True:
    tok = lexer.token()
    if not tok:
        break
    message = f"[LEXTOKEN] {tok.type} -> '{tok.value}' (line {tok.lineno}, column {tok.col}, pos {tok.lexpos})\n"
    log_file.write(message)
    print(tok)

log_file.close()