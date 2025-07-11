import pprint
import ply.yacc as yacc
from .lexer import tokens, lexer
from .logger import create_log_file 

semantic_errors = []
parser_errors = []

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
    'program : statement_list'
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : assignment
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
                 | function
                 | method_definition
                 | function_literal'''
    p[0] = p[1]

def p_package(p):
    '''package : PACKAGE MAIN
               | PACKAGE IDENTIFIER'''
    p[0] = ('package', p[2])

def p_import(p): #Extender para casos: m "math" ; . "math" ; _ "math"
    '''import : IMPORT STRING
              | IMPORT LPAREN import_list RPAREN'''
    if len(p) == 3:
        p[0] = ('import_single', p[2])
    else:
        p[0] = ('import_multiple', p[3])

def p_import_list(p):
    '''import_list : STRING
                   | import_list STRING'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_arguments(p):
    '''arguments : expression
                  | arguments COMMA expression
                  | '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

#Para manejar las constantes
def p_const_declaration(p):
    'const_declaration : CONST IDENTIFIER ASSIGN expression'
    p[0] = ('const_decl', p[2], p[4])

#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#Christopher Villon)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

def p_input(p):
    '''input : IDENTIFIER DOT IDENTIFIER LPAREN AMPERSAND IDENTIFIER RPAREN'''

def p_var_declaration(p):
    '''var_declaration : VAR IDENTIFIER DATATYPE'''
    var_name = p[2]
    var_type = p[3]
    if var_name in tabla_simbolos['variables']:
        semantic_error(f"Variable '{var_name}' already declared.", p)
        #print(f"Variable '{var_name}' already declared.")
    tabla_simbolos['variables'][var_name] = var_type
    p[0] = ('var_decl', var_name, var_type)


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
            #semantic_error(f"Error semántico: Se declaró '{nombre}' como '{tipo_declarado}' pero se asignó valor tipo '{tipo_expr}'")
            semantic_error(f"'{nombre}' was declared as '{tipo_declarado}' but was assigned value type '{tipo_expr}.", p)
        tabla_simbolos["variables"][nombre] = tipo_declarado
        p[0] = ('var_assign', nombre, tipo_declarado, valor)

def p_reasignacion(p):
    'assignment : IDENTIFIER ASSIGN expression'
    nombre = p[1]
    expr = p[3]
    tipo_expr = expr[0] if isinstance(expr, tuple) else 'unknown'
    if nombre not in tabla_simbolos["variables"]:
        semantic_error(f"Variable '{nombre}' no declarada.", p)
    tipo_esperado = tabla_simbolos["variables"][nombre]
    if tipo_expr != tipo_esperado:
        semantic_error(f"Variable '{nombre}' es de tipo '{tipo_esperado}' pero se intenta asignar valor tipo '{tipo_expr}'.", p)
    p[0] = ('reasignacion', nombre, expr)

def p_llamar_funcion(p):
    '''llamarFuncion : IDENTIFIER LPAREN argument_list_opt RPAREN'''

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
        semantic_error(f"No se puede comparar '{tipo_izq}' con '{tipo_der}'.", p)
    op = p[2]
    if op in ('==', '!='):
        p[0] = ('bool', ('cmp', op, left, right))
        return
    tipos_ordenables = ['number', 'string', 'rune']
    if tipo_izq not in tipos_ordenables:
        semantic_error(f"El operador '{op}' no es válido para tipo '{tipo_izq}'.", p)
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
        semantic_error(f"El operador lógico '{op}' solo se aplica a valores booleanos.", p)
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
    '''caseBlock : CASE expression COLON statement_list
                  | DEFAULT COLON statement_list'''
    
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
    '''function : FUNC IDENTIFIER LPAREN params_opt RPAREN return_type LBRACE statement_list RETURN expression RBRACE'''
    func_name = p[2]
    return_types = p[6]
    tabla_simbolos['functions'][func_name] = {
        'return_types': return_types,  
        'params': p[4]
    }
    p[0] = ('function_with_return', func_name, p[4], return_types, p[8])

def p_function_main(p):
    '''function : FUNC MAIN LPAREN params_opt RPAREN block'''

def p_return_statement(p):
    'return_statement : RETURN expression'
    function_name = p[-2]  
    returned_values = p[2]

    if function_name in tabla_simbolos['functions']:
        expected_types = tabla_simbolos['functions'][function_name]['return_types']
        if len(returned_values) != len(expected_types):
            raise TypeError(f"Function {function_name} expects {len(expected_types)} return values, but got {len(returned_values)}.")

        for idx, value in enumerate(returned_values):
            if value[0] != expected_types[idx]:
                raise TypeError(f"Expected return type {expected_types[idx]} for value {idx + 1}, but got {value[0]}.")
    else:
        raise NameError(f"Function {function_name} is not defined.")
    
    p[0] = ('return', returned_values)

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
    'block : LBRACE statement_list RBRACE'
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
    tipo, valor = p[1]
    p[0] = (tipo, valor)  # tipo será 'int' o 'float64'

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    var_name = p[1]
    if var_name not in tabla_simbolos['variables']:
        semantic_error(f"Variable '{var_name}' is not defined.", p)
    else:
        var_type = tabla_simbolos['variables'][var_name]
    p[0] = ('ident', var_name)

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
        semantic_error(f"No se puede usar el operador '{op}' entre '{tipo_izq}' y '{tipo_der}'.", p)
    
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
        #raise SyntaxError(f"The condition of if must be boolean or a comparison, not '{cond_type}'")
        semantic_error(f"The condition of if must be boolean or a comparison, not '{cond_type}.", p)

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
        p[0] = [p[1]]  
    elif len(p) == 3:
        p[0] = [p[1]] + p[2] 
    else:
        p[0] = []



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
        parser_errors.append(f"[SYNTAX ERROR] Unexpected '{p.value}' at line {p.lineno}")
        raise SyntaxError(f"[SYNTAX ERROR] Unexpected '{p.value}' at line {p.lineno}")
    else:
        parser_errors.append("[SYNTAX ERROR] Unexpected EOF")
        raise SyntaxError("[SYNTAX ERROR] Unexpected EOF")

def semantic_error(m, p):
    print("[SEMANTIC ERROR]", m)
    semantic_errors.append(f"[SEMANTIC ERROR] {m} Line {p.lineno(1)}")
    #log_file.write(f"[SEMANTIC ERROR] {message}\n")

parser = yacc.yacc()

def parser_analyze(code):
    global parser_errors
    global semantic_errors
    lexer.lineno = 1
    parser_errors = []
    semantic_errors = []
    #parser = yacc.yacc()
    try:
        results = []
        resultado = parser.parse(code)
        results.append("[OK] Parsing completed successfully.")
        #results.append(str(resultado))
        tree_str = tree_to_str(resultado)
        results.append(tree_str)
        return "\n".join(str(r) for r in results)
    except Exception as e:
        return "\n".join(str(e) for e in parser_errors)

def tree_to_str(node, indent="", last=True):
    if node is None:
        return "(empty tree)"
    lines = []
    prefix = indent + ("└── " if last else "├── ")
    if isinstance(node, tuple):
        lines.append(prefix + str(node[0]))
        indent += "    " if last else "│   "
        for i, child in enumerate(node[1:]):
            child_str = tree_to_str(child, indent, i == len(node[1:]) - 1)
            lines.append(child_str)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            child_str = tree_to_str(item, indent, i == len(node) - 1)
            lines.append(child_str)
    else:
        lines.append(prefix + str(node))    
    return "\n".join(lines)

def semantic_analyse():
    if semantic_errors:
        return "\n".join(semantic_errors)
    return "No semantic errors detected"

'''
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
#log_file.close()
