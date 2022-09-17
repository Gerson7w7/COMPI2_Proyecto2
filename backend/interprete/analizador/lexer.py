# importamos la libería lex
from interprete.ply import lex

# palabras reservadas
reservadas = {
    'let': 'LET',
    'mut': 'MUT',
    'new': 'NEW',
    'as': 'AS',
    'mod': 'MOD',
    'pub': 'PUB',
    'i64': 'I64',
    'f64': 'F64',
    'bool': 'BOOL', 
    'true': 'TRUE', 
    'false': 'FALSE',
    'char': 'CHAR',
    'String': 'STRING',
    'str': 'STR',
    'usize': 'USIZE', 
    'vec': 'VEC',
    'Vec': 'VEC_OBJ',
    'struct': 'STRUCT',
    'powf': 'POTENCIA_f64',
    'pow': 'POTENCIA_i64',
    'println': 'PRINTLN', # impresión con salto de línea
    'print': 'PRINT', # impresión sin salto de línea
    'fn': 'FN',
    'abs': 'ABS', 
    'sqrt': 'SQRT', 
    'to_string': 'TO_STRING',
    'clone': 'CLONE',
    'to_owned': 'TO_OWNED',
    'chars': 'CHARS',
    'len': 'LEN', 
    'push': 'PUSH',
    'remove': 'REMOVE',
    'contains': 'CONTAINS',
    'insert': 'INSERT',
    'capacity': 'CAPACITY',
    'with_capacity': 'WITH_CAPACITY',
    'if': 'IF', 
    'else': 'ELSE',
    'match': 'MATCH', 
    'loop': 'LOOP',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    '_': 'GUION_BAJO',
}

# definimos los tokens de nuestro lenguaje
tokens = [
    'INTERROGACION', 'AMPERSON', # palabras reservadas
    'CORCHETE_ABRE', 'CORCHETE_CIERRA', 'PARENTESIS_ABRE', 'PARENTESIS_CIERRA', 'LLAVE_ABRE', 'LLAVE_CIERRA', # encapsulamiento
    'COMA', 'PUNTO_COMA', 'DOS_PUNTOS', 'PUNTO', #separaciones
    # tipos de datos
    'ENTERO', 'DECIMAL', # números
    'CARACTER', # chars
    'CADENA', # strings
    # operadores
    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'MODULO', # aritméticos
    'IGUALDAD', 'DESIGUALDAD', 'IGUALACION', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL', # relacionales
    'OR', 'AND', 'NOT', # lógicos
    # funciones
    'FLECHA_GUION', # funciones y métodos
    'FLECHA_IGUAL', 'BARRA', # match (similar al switch)
    # identificadores
    'IDENTIFICADOR',
] + list(reservadas.values())

# ignora los espacios y tabulaciones
t_ignore = ' \t'

def t_DECIMAL(t):
    r'\d+\.\d+';
    t.value = float(t.value);
    return t;

# tokens con expresiones regulares simples
t_INTERROGACION = r'\?';
t_CORCHETE_ABRE = r'\[';
t_CORCHETE_CIERRA = r'\]';
t_PARENTESIS_ABRE = r'\(';
t_PARENTESIS_CIERRA = r'\)';
t_LLAVE_ABRE = r'\{';
t_LLAVE_CIERRA = r'\}';
t_COMA = r',';
t_PUNTO_COMA = r';';
t_DOS_PUNTOS = r':';
t_FLECHA_GUION = r'->';
t_FLECHA_IGUAL = r'=>';
t_PUNTO = r'\.';
t_SUMA = r'\+';
t_RESTA = r'\-';
t_MULTIPLICACION = r'\*';
t_DIVISION = r'/';
t_MODULO = r'%';
t_IGUALDAD = r'==';
t_DESIGUALDAD = r'!=';
t_MENOR_IGUAL = r'<=';
t_MAYOR_IGUAL = r'>=';
t_MENOR = r'<';
t_MAYOR = r'>';
t_IGUALACION = r'=';
t_OR = r'\|\|';
t_AND = r'&&';
t_NOT = r'!';
t_AMPERSON = r'\&';
t_BARRA = r'\|';

# tokens con expresiones regulares más elaborados y con acciones de código
def t_ENTERO(t):
    r'\d+';
    t.value = int(t.value);
    return t;

def t_CARACTER(t):
    r'\'(\\)?.\'';
    t.value = t.value.replace('\'', '');
    return t;

def t_CADENA(t):
    r'\"[^\"]*\"';
    t.value = t.value.replace('\"', '');
    return t;

def t_IDENTIFICADOR(t):
    r'([a-zA-Z_])[a-zA-Z0-9_]*';
    t.type = reservadas.get(t.value, 'IDENTIFICADOR');
    return t;

# contamos las líneas del código
def t_nuevalinea(t):
    r'(\r\n)+|\n+';
    t.lexer.lineno += t.value.count(t.value);

# manejo de errores léxicos
def t_error(t):
    print(f'Caracter no reconocido {t.value[0]!r}. En la linea {t.lexer.lineno}')
    t.lexer.skip(1)

def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1;
    return (token.lexpos - line_start) + 1;

def t_comentario(t):
    r'//.*';
    pass;

def t_multicomentarios(t):
    r'[/][*][^*]*[*]+([^/*][^*]*[*]+)*[/]';
    pass;

# construímos el lexer (analizador léxico)
lex.lex();