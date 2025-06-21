import ply.yacc as yacc
from lexer import tokens
from logger import create_log_file 

#impresión

#ingreso de datos por teclado

#expresiones aritméticas con uno o más operadores

#condiciones con uno o más conectores lógicos

#asignación de variables con todos los tipos, expresiones/condicionales

#estructuras de datos

#estructuras de control

#definición de funciones

#definición de clases, propiedades, métodos

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)





with open("testing_algorithms/algorithm1.go", "r", encoding="utf-8") as f:  #PRUEBEN CON SU ALGORITMO
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