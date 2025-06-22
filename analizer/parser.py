import ply.yacc as yacc
from lexer import tokens
from logger import create_log_file 

#Christopher Villon





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
def p_statement_if(p):
    '''if_statement : IF LPAREN condition RPAREN block
                 | IF LPAREN condition RPAREN block ELSE block'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])  
    else:
        p[0] = ('if-else', p[3], p[5], p[7])

def p_function_call(p):
    'function_call : IDENTIFIER LPAREN args RPAREN'
    p[0] = ('call', p[1], p[3])


def p_args_multiple(p):         #argumentos
    'args : args COMMA expression'
    p[0] = p[1] + [p[3]]

def p_args_single(p):
    'args : expression'
    p[0] = [p[1]]

def p_args_empty(p):
    'args : '
    p[0] = []


def p_block(p):                 #para bloquedes de codigo
    '''block : LBRACE statements RBRACE'''
    p[0] = p[2]

def p_block_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    'statements : statement'
    p[0] = [p[1]]



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

with open("testing_algorithms/algorithm#.go", "r", encoding="utf-8") as f:  #PRUEBEN CON SU ALGORITMO
    data = f.read()

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

