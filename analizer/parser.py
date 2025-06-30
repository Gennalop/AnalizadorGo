import pprint
import ply.yacc as yacc
from lexer import tokens, lexer
from logger import create_log_file 

tabla_simbolos = {
    "variables": {}, 
    "tipos": {
        "string-funciones": ["len", "to_uppercase", "to_lowercase", "to_str"],
        "int-funciones": ["abs", "sqrt"],
    },
    "funciones": {},
    "structs": {},  
}

def p_program(p):
    '''program : package import_list declaration_list
               | package declaration_list
               | declaration_list
               | package''' 
    if len(p) == 2:
        p[0] = ('program', p[1])
    elif len(p) == 3:
        p[0] = ('program', p[1], p[2])
    else:
        p[0] = ('program', p[1], p[2], p[3])

def p_package(p):
    '''package : PACKAGE MAIN'''

##Cambiar esta parte

def p_arguments(p):
    '''arguments : expression
                 | expression COMMA arguments'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


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
                   | const_declaration
                   | function
                   | method_definition
                   | function_literal
                   | import'''
    p[0] = p[1]

#Para manejar las constantes
def p_const_declaration(p):
    'const_declaration : CONST IDENTIFIER ASSIGN expression'
    p[0] = ('const_decl', p[2], p[4])

def p_import_list_single(p):
    'import_list : import'
    p[0] = [p[1]]

def p_import_list_multiple(p):
    'import_list : import_list import'
    p[0] = p[1] + [p[2]]

#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#Christopher Villon)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

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
                 | map
                 | if_statement
                 | return_statement'''

def p_input(p):
    '''input : IDENTIFIER DOT IDENTIFIER LPAREN AMPERSAND IDENTIFIER RPAREN'''

def p_var_declaration(p):
    '''varDeclaration : VAR IDENTIFIER DATATYPE'''


##Genesis. Aplicando regla semantica para verficacion de tipo
def p_assignment(p):
    '''assignment : IDENTIFIER DECLARE_ASSIGN expression
                  | VAR IDENTIFIER DATATYPE ASSIGN expression
                  | VAR IDENTIFIER DATATYPE ASSIGN llamarFuncion'''
    if len(p) == 4:
        nombre = p[1]
        expr = p[3]
        tipo_expr = expr[0] if isinstance(expr, tuple) else 'unknown'
        tabla_simbolos["variables"][nombre] = tipo_expr
        p[0] = ('assign_decl', nombre, expr)
    elif len(p) == 6:
        nombre = p[2]
        tipo_declarado = p[3]
        valor = p[5]
        tipo_expr = valor[0] if isinstance(valor, tuple) else 'unknown'
        if tipo_expr != tipo_declarado:
            raise SyntaxError(f"Error semántico: Se declaró '{nombre}' como '{tipo_declarado}' pero se asignó valor tipo '{tipo_expr}'")
        tabla_simbolos["variables"][nombre] = tipo_declarado
        p[0] = ('var_assign', nombre, tipo_declarado, valor)

def p_reasignacion(p):
    'assignment : IDENTIFIER ASSIGN expression'
    nombre = p[1]
    expr = p[3]
    tipo_expr = expr[0] if isinstance(expr, tuple) else 'unknown'
    if nombre not in tabla_simbolos["variables"]:
        raise SyntaxError(f"Error: variable '{nombre}' no declarada")
    tipo_esperado = tabla_simbolos["variables"][nombre]
    if tipo_expr != tipo_esperado:
        raise SyntaxError(f"Error semántico: variable '{nombre}' es de tipo '{tipo_esperado}' pero se intenta asignar valor tipo '{tipo_expr}'")
    p[0] = ('reasignacion', nombre, expr)

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

#Aus 
def p_expression_comparacion(p):
    'expression : expression comparador expression'
    left = p[1]
    right = p[3]

    # Extraer tipos base
    left_type = left[0]
    right_type = right[0]

    # Permitir comparaciones solo entre números, strings o bool entre sí
    allowed = [
        ('number', 'number'),
        ('string', 'string'),
        ('rune', 'rune'),
        ('bool', 'bool'),
    ]

    if (left_type, right_type) not in allowed:
        raise SyntaxError(f"Comparison between incompatible types: {left_type} y {right_type}")

    p[0] = ('comparison', p[2], left, right)


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
    left = p[1]
    right = p[3]
    tipo_izq = left[0]
    tipo_der = right[0]
    if tipo_izq != tipo_der:
        raise SyntaxError(f"Error semántico: No se puede comparar '{tipo_izq}' con '{tipo_der}'")
    op = p[2]
    if op in ('==', '!='):
        p[0] = ('bool', ('cmp', op, left, right))
        return
    tipos_ordenables = ['number', 'string', 'rune']
    if tipo_izq not in tipos_ordenables:
        raise SyntaxError(f"Error semántico: El operador '{op}' no es válido para tipo '{tipo_izq}'")
    p[0] = ('bool', ('cmp', op, left, right))

def p_condicion_compleja(p):
    '''condicion_compleja : condicion operadorLogico condicion
                          | condicion operadorLogico condicion_compleja'''
    izquierda = p[1]
    derecha = p[3]
    op = p[2]
    tipo_izq = izquierda[0] if isinstance(izquierda, tuple) else 'unknown'
    tipo_der = derecha[0] if isinstance(derecha, tuple) else 'unknown'
    if tipo_izq != 'bool' or tipo_der != 'bool':
        raise SyntaxError(f"Error semántico: El operador lógico '{op}' solo se aplica a valores booleanos")
    p[0] = ('bool', ('logic', op, izquierda, derecha))

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
#Aus
def p_switch_statement(p):
    '''switch : SWITCH expression LBRACE caseBlocks RBRACE'''
    expr = p[2]
    if expr[0] == 'nil':
        raise SyntaxError("Switch expression cannot be nil")
    p[0] = ('switch', expr, p[4])

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
    '''function : FUNC IDENTIFIER LPAREN params_opt RPAREN return_type block'''
    p[0] = ('function', p[2], p[4], p[6], p[7])

def p_function_with_return(p):
    '''function : FUNC IDENTIFIER LPAREN params_opt RPAREN return_type LBRACE sentencias RETURN expression RBRACE'''

def p_function_main(p):
    '''function : FUNC MAIN LPAREN params_opt RPAREN block'''

def p_return_statement(p):
    'return_statement : RETURN expression'

def p_params_opt(p):
    '''params_opt : params
                      | empty'''
    
def p_params(p):
    '''params : param
                  | param COMMA params'''
    
def p_param(p):
    '''param : IDENTIFIER type_name'''

def p_type_name(p):
    '''type_name : DATATYPE
                 | IDENTIFIER'''



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
        raise SyntaxError(f"Impresión no válida: {p[1]}.{p[3]}")

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

def p_identifier_list_single(p):
    'identifier_list : IDENTIFIER'
    p[0] = [p[1]]

def p_identifier_list_multiple(p):
    'identifier_list : IDENTIFIER COMMA identifier_list'
    p[0] = [p[1]] + p[3]

def p_short_assignment(p):
    'shortAssignment : identifier_list DECLARE_ASSIGN expression'
    p[0] = ('short_assign', p[1], p[3])

#Aus
def p_for_statement_condition(p):
    'for_statement : FOR condicion block'
    cond = p[2]
    cond_type = cond[0]

    if cond_type not in ('comparison', 'bool'):
        raise SyntaxError(f"The condition of for must be boolean or a comparison, not '{cond_type}'")

    p[0] = ("FOR_CONDITION", cond, p[3])

def p_for_statement_infinite(p):
    'for_statement : FOR block'
    p[0] = ("FOR_INFINITE", p[2])

def p_for_range_clause(p):
    'for_range_clause : shortAssignment RANGE expression'
    p[0] = ('for_range', p[1], p[3])

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


##Genesis. Regla para compatibilidad de tipos
def p_expression_binary(p):
    '''expression : expression operator expression'''
    left = p[1]
    right = p[3]
    op = p[2]
    tipo_izq = left[0] if isinstance(left, tuple) else 'unknown'
    tipo_der = right[0] if isinstance(right, tuple) else 'unknown'
    if tipo_izq == 'number' and tipo_der == 'number':
        p[0] = ('number', ('binop', op, left, right))
    elif op == '+' and tipo_izq == tipo_der == 'string':
        p[0] = ('string', ('binop', op, left, right))
    else:
        raise SyntaxError(f"Error semántico: No se puede usar el operador '{op}' entre '{tipo_izq}' y '{tipo_der}'")
    
def p_expression_field_access(p):
    'expression : expression DOT IDENTIFIER'
    p[0] = ('field_access', p[1], p[3])

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

#Aus
#Estructura if
def p_if_statement(p):
    '''if_statement : IF condicion_compleja block
                    | IF condicion_compleja block ELSE block'''
    cond = p[2]
    cond_type = cond[0]

    if cond_type not in ('comparison', 'bool'):
        raise SyntaxError(f"The condition of if must be boolean or a comparison, not '{cond_type}'")

    if len(p) == 4:
        p[0] = ('if', cond, p[3], None)
    else:
        p[0] = ('if_else', cond, p[3], p[5])

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



#Estructura de datos: Slice
def p_slice_declaration(p):
    'slice_declaration : VAR IDENTIFIER LBRACKET RBRACKET type_name'
    p[0] = ('slice_decl', p[2], p[5]) 

def p_slice_declare_assign(p):
    'declare_assign : IDENTIFIER DECLARE_ASSIGN slice_literal'
    p[0] = ('declare_slice', p[1], p[3])

def p_slice_literal(p):
    'slice_literal : LBRACKET RBRACKET type_name LBRACE elements RBRACE'
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

# Build the parser
parser = yacc.yacc()

log_file = create_log_file("gennalop")  # Cambia por tu nombre real o el de GitHub

with open("testing_algorithms/algorithm1.go", "r", encoding="utf-8") as f:
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
'''
log_file.close()
