import ply.yacc as yacc
from lexer import tokens, lexer
from logger import create_log_file 

#Christopher Villon
def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''

def p_sentencia(p):
    '''sentencia : assignment
                | varDeclaration
                | input
                | llamarFuncion
                | package
                | import
                | switch
                | map
                | function'''

def p_input(p):
    '''input : IDENTIFIER DOT IDENTIFIER LPAREN AMPERSAND IDENTIFIER RPAREN'''

def p_var_declaration(p):
    '''varDeclaration : VAR IDENTIFIER DATATYPE'''

def p_short_assignment(p):
    '''assignment : IDENTIFIER DECLARE_ASSIGN expression'''

def p_assignment_simple(p):
    '''assigment : VAR IDENTIFIER DATATYPE ASSIGN expression'''

def p_assingment_funcion(p):
    '''assignment : VAR IDENTIFIER DATATYPE ASSIGN llamarFuncion'''

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
    
def p_function(p):
    '''function : FUNC IDENTIFIER LPAREN params_opt RPAREN DATATYPE LBRACE sentencias RETURN expression RBRACE'''

def p_params_opt(p):
    '''params_opt : params
                      | empty'''
    
def p_params(p):
    '''params : param
                  | param COMMA params'''
    
def p_param(p):
    '''param : IDENTIFIER DATATYPE'''




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


#condicion con uno o mas comparadores logicos
def p_condition_comparison(p):
    '''condition : expression comparetor expression'''
    p[0] = ('compare', p[2], p[1], p[3])

def p_comparetor(p):
    '''comparetor : EQ
                | NEQ
                | GT
                | LT
                | GE
                | LE'''

def p_condition_logical(p):
    '''condition : condition AND condition
                 | condition OR condition'''
    p[0] = ('logical', p[2], p[1], p[3])

def p_condition_group(p):
    'condition : LPAREN condition RPAREN'
    p[0] = p[2]


#Estructura de control if


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
        raise SyntaxError(f"Syntax error at line {p.lineno}: unexpected '{p.value}'")
    else:
        raise SyntaxError("Syntax error at EOF")



# Build the parser and test
parser = yacc.yacc()

log_file = create_log_file("ChrVillon")  # Cambia por tu nombre real o el de GitHub

with open("testing_algorithms/algorithm3.go", "r", encoding="utf-8") as f:
    lines = f.readlines()

block = ""
open_braces = 0

for lineno, line in enumerate(lines, start=1):
    stripped = line.strip()
    if not stripped or stripped.startswith('//'):
        continue

    block += line
    open_braces += line.count('{')
    open_braces -= line.count('}')

    if open_braces == 0 and block.strip():
        lexer.lineno = lineno
        try:
            result = parser.parse(block)
            log_file.write(f"[OK] Bloque terminado en línea {lineno}: {block.strip()}\n")
        except Exception as e:
            log_file.write(f"[ERROR] Bloque terminado en línea {lineno}: {block.strip()} -> {str(e)}\n")
        block = ""
'''
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

log_file.close()
'''

