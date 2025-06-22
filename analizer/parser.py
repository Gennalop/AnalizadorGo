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

#IMPRESION
#======================================================================================
##print_statement
def p_print_statement(p):
    'print_statement : IDENTIFIER DOT IDENTIFIER LPAREN argument_list_opt RPAREN'
    if p[1] == 'fmt' and p[3] in ('Print', 'Println', 'Printf'):
        p[0] = ('print', p[3], p[5])
    else:
        print("Error: no es una impresión válida")

##argument_list
def p_argument_list_single(p):
    'argument_list : expression'
    p[0] = [p[1]]
def p_argument_list_multiple(p):
    'argument_list : argument_list COMMA expression'
    p[0] = p[1] + [p[3]]

##argument_list_opt
def p_argument_list_opt_some(p):
    'argument_list_opt : argument_list'
    p[0] = p[1]
def p_argument_list_opt_empty(p):
    'argument_list_opt : '
    p[0] = []

##expression
def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = ('ident', p[1])
def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])
def p_expression_rune(p):
    'expression : RUNE'
    p[0] = ('rune', p[1])
def p_expression_string(p):
    'expression : STRING'
    p[0] = ('string', p[1])
def p_expression_raw_string(p):
    'expression : RAW_STRING'
    p[0] = ('raw_string', p[1])
def p_expression_boolean(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = ('bool', True if p[1] == 'true' else False)
def p_expression_nil(p):
    'expression : NIL'
    p[0] = ('nil', None)


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
#ESTRUCTURAS DE DATOS
#======================================================================================

#Struct -------------------------------------------------------------------------------

##struct_definition



#ESTRUCTURAS DE CONTROL
#======================================================================================

#For ----------------------------------------------------------------------------------

##for_statement
def p_for_statement_classis(p):
    'for_statement : FOR assignment SEMICOLON condition SEMICOLON expression block'
    p[0] = ("FOR_CLASSIC", p[2], p[4], p[6], p[7])

def p_for_statement_condition(p):
    'for_statement : FOR condition block'
    p[0] = ("FOR_CONDITION", p[2], p[3])

def p_for_statement_infinite(p):
    'for_statement : FOR block'
    p[0] = ("FOR_INFINITE", p[2])

#block
def p_block(p):
    'block : LBRACE statement_list RBRACE'
    p[0] = p[2]

def p_statement_list_single(p):
    'statement_list : statement'
    p[0] = [p[1]]

def p_statement_list_multiple(p):
    'statement_list : statement statement_list'
    p[0] = [p[1]] + p[2]

# Aquí puedes agregar más tipos de statement (e.g., for_statement, if_statement, return, etc.)
def p_statement(p):
    '''statement : assignment SEMICOLON
                 | for_statement
                 | if_statement'''
    p[0] = p[1]






def p_for_statement(p):
    '''for_statement : FOR condition LBRACE block RBRACE
                     | FOR for_clause block'''
    p[0] = ('for', p[2], p[3])

def p_simple_condition(p):
    'simple_condition : expression'
    p[0] = p[1]

def p_for_clause(p):
    'for_clause : statement SEMICOLON expression SEMICOLON statement'
    p[0] = ('for_clause', p[1], p[3], p[5])


def p_statement_list_single(p):
    'statement_list : statement'
    p[0] = [p[1]]

def p_statement_list_multiple(p):
    'statement_list : statement_list statement'
    p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : print_statement
                 | for_statement
                 | assign_statement'''
    p[0] = p[1]


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
