import pprint
import ply.yacc as yacc
from lexer import tokens, lexer
from logger import create_log_file 

def p_program(p):
    'program : declaration_list'
    p[0] = ('program', p[1])

##Cambiar esta parte

def p_declaration_list_single(p):
    'declaration_list : declaration'
    p[0] = [p[1]]

def p_declaration_list_multiple(p):
    'declaration_list : declaration_list declaration'
    p[0] = p[1] + [p[2]]

def p_declaration(p):
    '''declaration : struct_definition
                   | print_statement
                   | for_statement
                   '''
    p[0] = p[1]

#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#Christopher Villon)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''

def p_sentencia(p):
    '''sentencia : assignment
                 | input
                 | llamarFuncion
                 | print_statement
                 | struct_definition
                 | for_statement
                 | package
                 | import
                 | switch
                 | map'''

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
    '''llamarFuncion : IDENTIFIER LPAREN argument_list_opt RPAREN'''

#def p_argumentos_opt(p):
#    '''argumentos_opt : argumentos
#                      | empty'''

#def p_argumentos(p):
#    '''argumentos : expression
#                  | argumentos COMMA expression'''

def p_argumentos(p):
    '''argumentos : expression
                  | expression COMMA argumentos'''
    
def p_expression_comparacion(p):
    'expression : expression comparador expression'

def p_boolean_expression(p):
    '''expression : expression operadorLogico expression'''
    
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

def p_switch_statement(p):
    '''switch : SWITCH expression LBRACE caseBlocks RBRACE'''

def p_caseBlocks(p):
    '''caseBlocks : caseBlock
                   | caseBlock caseBlocks'''

def p_caseBlock(p):
    '''caseBlock : CASE expression COLON sentencias
                  | DEFAULT COLON sentencias'''
    
def p_short_map(p):
    '''map : IDENTIFIER DECLARE_ASSIGN mapLiteral'''

def p_map(p):
    '''map : VAR IDENTIFIER ASSIGN mapLiteral'''

def p_map_literal(p):
    '''mapLiteral : MAP LBRACKET DATATYPE RBRACKET DATATYPE LBRACE mapEntries RBRACE'''

def p_map_entries(p):
    '''mapEntries : mapEntry
                   | mapEntry COMMA mapEntries'''

def p_map_entry(p):
    '''mapEntry : value_key COLON value_key'''
    
def p_value_key(p):
    '''value_key : expression
                | STRING'''



def p_package(p):
    '''package : PACKAGE MAIN'''

def p_import(p):
    '''import : IMPORT STRING'''

#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#Genesis Lopez))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

#IMPRESION============================================================================

##print_statement
def p_print_statement(p):
    'print_statement : IDENTIFIER DOT IDENTIFIER LPAREN argument_list_opt RPAREN'
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

#METHODS==============================================================================

##method_definition VERIFICARRRR
def p_method_definition(p):
    'method_definition : FUNC LPAREN IDENTIFIER IDENTIFIER RPAREN IDENTIFIER LPAREN arguments RPAREN block'
    p[0] = ('method', {
        'receiver_name': p[2],
        'receiver_type': p[3],
        'method_name': p[5],
        'params': p[7],
        'body': p[9]
    })

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
#Austin Estrella))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
    
# Expresiones Aritmeticas
precedence = (
    ('left', 'OR'),                      # ||
    ('left', 'AND'),                     # &&  
    ('nonassoc', 'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE'), # ==, !=, >, <, >=, <=
    ('left', 'PLUS', 'MINUS'),         
    ('left', 'TIMES', 'DIVIDE', 'MOD'), 
    ('right', 'UMINUS'),                # -x
)

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])
def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = ('ident', p[1])
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

def p_expression_binary(p):
    '''expression : expression operator expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_operator(p):
    '''operator : PLUS
                | MINUS
                | TIMES
                | DIVIDE
                | MOD'''

def p_expression_unary_minus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('neg', p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

#def p_expression_value(p):
#    'expression : value'
#    p[0] = p[1]

def p_value_number(p):
    'value : NUMBER'
    p[0] = ("number",p[1])

def p_value_identifier(p):
    'value : IDENTIFIER'
    p[0] = ("vari", p[1])

#Estructura if
def p_if_statement(p):
    '''if_statement : IF expression block
                    | IF expression block ELSE block'''
    if len(p) == 4:
        p[0] = ('if', p[2], p[3], None)
    else:
        p[0] = ('if_else', p[2], p[3], p[5])

def p_block(p):
    '''block : LBRACE sentencias RBRACE'''
    p[0] = ('block', p[2])


#funciones de orden superior
def p_function_literal(p):
    'function_literal : FUNC LPAREN parameters RPAREN return_type block'
    p[0] = ('func_literal', p[3], p[5], p[6])

def p_parameters(p):
    '''parameters : parameters COMMA parameter
                  | parameter
                  | empty'''
    if len(p) == 2 and p[1] is None:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_parameter(p):
    '''parameter : IDENTIFIER DATATYPE
                 | IDENTIFIER FUNC LPAREN parameters RPAREN DATATYPE'''
    if len(p) == 3:
        p[0] = ('param', p[1], p[2])
    else:
        p[0] = ('param_func', p[1], p[4], p[6])

def p_return_type(p):
    '''return_type : DATATYPE
                   | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None


def p_empty(p):
    'empty :'
    p[0] = None



#Estructura de datos: Slice
def p_slice_declaration(p):
    'slice_declaration : VAR IDENTIFIER LBRACKET RBRACKET DATATYPE'
    p[0] = ('slice_decl', p[2], p[5]) 

def p_slice_declare_assign(p):
    'declare_assign : IDENTIFIER DECLARE_ASSIGN slice_literal'
    p[0] = ('declare_slice', p[1], p[3])

def p_slice_literal(p):
    'slice_literal : LBRACKET RBRACKET DATATYPE LBRACE elements RBRACE'
    p[0] = ('slice_lit', p[3], p[5]) 

def p_elements_multiple(p):
    'elements : elements COMMA expression'
    p[0] = p[1] + [p[3]]

def p_elements_single(p):
    'elements : expression'
    p[0] = [p[1]]



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

'''
log_file = create_log_file("ChrVillon")  # Cambia por tu nombre real o el de GitHub

with open("testing_algorithms/algorithm3.go", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Analizando archivo .go línea por línea...\n")

for lineno, line in enumerate(lines, start=1):
    line = line.strip()
    if not line or line.startswith('//'):  # Saltar líneas vacías o comentarios
        continue

    lexer.lineno = lineno  

    try:
        result = parser.parse(line)
        log_file.write(f"[OK] Línea {lineno}: {line}\n")

    except Exception as e:
        log_file.write(f"[ERROR] Línea {lineno}: {line} -> {str(e)}\n")

parser.parse(data)

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)

#log_file.close(
parser.input(data)
'''
log_file.close()

