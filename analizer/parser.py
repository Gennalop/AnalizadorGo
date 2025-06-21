import ply.yacc as yacc
from lexer import tokens
from logger import create_log_file 


#Christopher Villon





#Genesis Lopez




#Austin Estrella

# Expresiones Aritmeticas
precedence = (
    ('left', 'PLUS', 'MINUS'),         
    ('left', 'TIMES', 'DIVIDE', 'MOD'), 
    ('right', 'UMINUS'),                
)

def p_expression_binary(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_unary_minus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('neg', p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_value(p):
    'expression : value'
    p[0] = p[1]

def p_value_number(p):
    'value : NUMBER'
    p[0] = ('number', p[1])

def p_value_identifier(p):
    'value : IDENTIFIER'
    p[0] = ('var', p[1])








# Error rule for syntax errors
def p_error(p):
     print(f"Syntax error at line {p.lineno}")

# Build the parser and test
parser = yacc.yacc()


log_file = create_log_file("gitUser") #CAMBIAR A NOMBRE DE SU USUARIO GIT 

with open("testing_algorithms/algorithm#.go", "r", encoding="utf-8") as f:  #PRUEBEN CON SU ALGORITMO
    data = f.read()

parser.input(data)

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
