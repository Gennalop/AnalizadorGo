import pprint
import ply.yacc as yacc
from lexer import tokens
from logger import create_log_file 

def p_program(p):
    'program : declaration_list'
    p[0] = ('program', p[1])

def p_declaration_list_single(p):
    'declaration_list : declaration'
    p[0] = [p[1]]

def p_declaration_list_multiple(p):
    'declaration_list : declaration_list declaration'
    p[0] = p[1] + [p[2]]

def p_declaration(p):
    '''declaration : struct_definition
                   | print_statement'''
    p[0] = p[1]

#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#E1 ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''

def p_sentencia(p):
    '''sentencia : assignment
                 | input
                 | llamarFuncion
                 | print_statement'''

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
    '''condicion_compleja : condicion operadorLogico condicion
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

#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#E2))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

#IMPRESION============================================================================

##print_statement
def p_print_statement(p):
    'print_statement : IDENTIFIER DOT IDENTIFIER LPAREN argumentos_opt RPAREN'
    if p[1] == 'fmt' and p[3] in ('Print', 'Println', 'Printf'):
        p[0] = ('print', p[3], p[5])
    else:
        print("Error: no es una impresión válida")

#STRUCT===============================================================================

##struct_definition
def p_struct_definition(p):
    'struct_definition : TYPE IDENTIFIER STRUCT LBRACE struct_fields RBRACE'
    p[0] = ('struct', p[2], p[5])

##struct_field
def p_struct_field(p):
    'struct_field : IDENTIFIER DATATYPE'
    p[0] = (p[1], p[2])

##struct_fields
def p_struct_fields_single(p):
    'struct_fields : struct_field'
    p[0] = [p[1]]
def p_struct_fields_multiple(p):
    'struct_fields : struct_fields struct_field'
    p[0] = p[1] + [p[2]]

#FOR==================================================================================

##for_statement
def p_for_statement_classis(p):
    'for_statement : FOR shortAssignment SEMICOLON condicion SEMICOLON expression block'
    p[0] = ("FOR_CLASSIC", p[2], p[4], p[6], p[7])

def p_for_statement_condition(p):
    'for_statement : FOR condicion block'
    p[0] = ("FOR_CONDITION", p[2], p[3])

def p_for_statement_infinite(p):
    'for_statement : FOR block'
    p[0] = ("FOR_INFINITE", p[2])

def p_block(p):
    'block : LBRACE sentencias RBRACE'
    p[0] = ('block', p[2])

def p_block_empty(p):
    '''block : LBRACE RBRACE'''
    p[0] = ('block', [])

#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#E3))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
    
# Expresiones Aritmeticas
precedence = (
    ('left', 'PLUS', 'MINUS'),         
    ('left', 'TIMES', 'DIVIDE', 'MOD'), 
    ('right', 'UMINUS'),                
)

def p_expression_binary(p):
    '''expression_binary : expression PLUS expression
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

#def p_value_number(p):
#    'value : NUMBER'
#    p[0] = ('number', p[1])

#def p_value_identifier(p):
#    'value : IDENTIFIER'
#    p[0] = ('var', p[1])

def p_value_identifier(p):
    'value : IDENTIFIER'
    p[0] = ('ident', p[1])
def p_value_number(p):
    'value : NUMBER'
    p[0] = ('number', p[1])
def p_value_rune(p):
    'value : RUNE'
    p[0] = ('rune', p[1])
def p_value_string(p):
    'value : STRING'
    p[0] = ('string', p[1])
def p_value_raw_string(p):
    'value : RAW_STRING'
    p[0] = ('raw_string', p[1])
def p_value_boolean(p):
    '''value : TRUE
             | FALSE'''
    p[0] = ('bool', True if p[1] == 'true' else False)
def p_value_nil(p):
    'value : NIL'
    p[0] = ('nil', None)

# Error rule for syntax errors
def p_error(p):
    if p:
        message = f"[SYNTAX ERROR] Unexpected token '{p.value}' at line {p.lineno}, pos {p.lexpos}\n"
    else:
        message = "[SYNTAX ERROR] Unexpected end of input\n"
    
    print(message.strip())
    log_file.write(message)

log_file = create_log_file("gennalop") #CAMBIAR A NOMBRE DE SU USUARIO GIT 

# Build the parser
parser = yacc.yacc()

with open("testing_algorithms/p.go", "r", encoding="utf-8") as f:  #PRUEBEN CON SU ALGORITMO
    data = f.read()

result = parser.parse(data)

if result is not None:
    log_file.write("[PARSE RESULT]\n")
    pprint.pprint(result, stream=log_file, indent=2)

log_file.close()
