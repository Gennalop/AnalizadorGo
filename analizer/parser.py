import ply.yacc as yacc
from lexer import tokens, lexer
from logger import create_log_file 

#Christopher Villon
def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''

def p_sentencia(p):
    '''sentencia : assignment
                 | input
                 | llamarFuncion
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
    '''llamarFuncion : IDENTIFIER LPAREN argumentos_opt RPAREN'''

def p_argumentos_opt(p):
    '''argumentos_opt : argumentos
                      | empty'''

def p_argumentos(p):
    '''argumentos : expression
                  | expression COMMA argumentos'''
    
def p_expression_comparacion(p):
    'expression : expression comparador expression'

def p_boolean_expression(p):
    '''expression : expression operadorLogico expression'''

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



#Genesis Lopez




#Austin Estrella

# Expresiones Aritmeticas
precedence = (
    ('left', 'OR'),                      # ||
    ('left', 'AND'),                     # &&  
    ('nonassoc', 'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE'), # ==, !=, >, <, >=, <=
    ('left', 'PLUS', 'MINUS'),         
    ('left', 'TIMES', 'DIVIDE', 'MOD'), 
    ('right', 'UMINUS'),                # -x
)

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

def p_expression_value(p):
    'expression : value'
    p[0] = p[1]

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
        message = f"Syntax Error at line {p.lineno}\n"
    print(message)
    #log_file.write(message)




# Build the parser and test
parser = yacc.yacc()

'''
log_file = create_log_file("gitUser") #CAMBIAR A NOMBRE DE SU USUARIO GIT 
=======

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
'''
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

log_file.close()

