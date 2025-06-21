import ply.yacc as yacc
from lexer import tokens
from logger import create_log_file 

#Christopher Villon
def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''

def p_sentencia(p):
    '''sentencia : assignment
                 | input
                 | llamarFuncion'''

def p_input(p):
    '''input : IDENTIFIER DOT IDENTIFIER LPAREN AMPERSAND IDENTIFIER RPAREN'''

def p_assignment(p):
    '''assignment : assigmentSimple
                  | assignmentFuncion
                  | shortAssignment'''

def p_short_assignment(p):
    '''shortAssignment : IDENTIFIER DECLARE_ASSIGN expression'''

def p_assignment_simple(p):
    '''assigmentSimple : VAR IDENTIFIER DATATYPE ASSIGN expression'''

def p_assingment_funcion(p):
    '''assignmentFuncion : VAR IDENTIFIER DATATYPE ASSIGN llamarFuncion'''

def p_llamar_funcion(p):
    '''llamarFuncion : IDENTIFIER LPAREN argumentos_opt RPAREN'''

def p_argumentos_opt(p):
    '''argumentos_opt : argumentos
                      | empty'''

def p_argumentos(p):
    '''argumentos : expression
                  | expression COMMA argumentos'''

def p_condicion(p):
    '''condicion : expression comparador expression'''

def p_condicion_compleja(p):
    '''condicion : condicion operadorLogico condicion
                 | condicion operadorLogico condicion_compleja'''

def p_operador_logico(p):
    '''operadorLogico : AND
                      | OR'''

def p_comparador(p):
    '''comparador : EQ
                  | NEQ
                  | GT
                  | LT
                  | GE
                  | LE'''

def p_empty(p):
    '''empty :'''
    pass





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
