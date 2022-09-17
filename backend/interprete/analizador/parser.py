# ejemplos: https://www.dabeaz.com/ply/ply.html#ply_nn33
from interprete.ply.yacc import yacc
from interprete.analizador import lexer

from ..expresiones.Aritmetica import Aritmetica
from ..extra.Tipos import TipoAritmetica, TipoDato, TipoLogico, TipoNativo, TipoRelacional, TipoTransferencia
from ..extra.Ast import Ast
from ..instrucciones.Declaracion import Declaracion, Asignacion
from ..expresiones.Literal import Literal
from interprete.instrucciones.Imprimir import Imprimir
from interprete.expresiones.Relacional import Relacional
from ..expresiones.Logico import Logico
from ..expresiones.Acceso import Acceso, AccesoArreglo, AccesoStruct
from interprete.instrucciones.Bloque import Bloque
from interprete.instrucciones.IfElse import IfElse
from interprete.instrucciones.Match import Case, Match
from ..instrucciones.Transferencia import Transferencia
from ..instrucciones.Loop import Loop
from ..expresiones.FuncionesNativas import Abs, Clone, Sqrt, ToString, Chars
from ..instrucciones.While import While
from ..expresiones.Casteo import Casteo
from ..instrucciones.Arreglo import AsignacionArreglo, Dimension, Arreglo, WithCapacity
from ..expresiones.Expresion import Expresion
from interprete.instrucciones.FuncionesVector import Push, Insert, Remove, Contains, Longitud, Capacity
from interprete.instrucciones.Instruccion import Instruccion
from ..instrucciones.ForIn import ForIn
from ..instrucciones.Funcion import Funcion
from ..instrucciones.LlamadaFuncion import LlamadaFuncion, Puntero
from ..instrucciones.Struct import AsignacionStruct, InstanciaStruct, Struct, ExpresionesStruct

tokens = lexer.tokens;

# precedencia de operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL', 'DESIGUALDAD', 'IGUALDAD'),
    ('left', 'RESTA', 'SUMA'),
    ('left', 'MODULO'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('left', 'AS'),
    ('left', 'PUNTO'),
    ('right', 'NOT'),
    ('right', 'UMENOS'),
)

def p_inicio(p):
    """
    inicio : ejecutables
    """
    p[0] = Ast(p[1])

def p_ejecutables(p):
    """
    ejecutables : ejecutables ejecutable
        | ejecutable
    """
    if (len(p) == 3):
        p[1].append(p[2]); p[0] = p[1];
    else:
        p[0] = [p[1]];

def p_ejecutable(p):
    """
    ejecutable : funcion
        | struct
    """
    p[0] = p[1];

def p_funcion(p):
    """
    funcion : FN IDENTIFICADOR PARENTESIS_ABRE parametros PARENTESIS_CIERRA retorno_fn bloque
    """
    p[0] = Funcion(p[2], p[4], p[6], p[7], p.lineno(1), p.lexpos(1));

def p_struct(p):
    """
    struct : STRUCT IDENTIFICADOR bloque_struct
    """
    p[0] = Struct(p[2], p[3], p.lineno(1), p.lexpos(1));

def p_bloque_struct(p):
    """
    bloque_struct : LLAVE_ABRE parametros LLAVE_CIERRA
        | LLAVE_ABRE LLAVE_CIERRA
    """
    if (len(p) == 4):
        p[0] = p[2];
    else:
        p[0] = [];

def p_parametros(p):
    """
    parametros : parametros COMA parametro
        | parametro
    """
    if (len(p) == 4):
        p[1].append(p[3]); p[0] = p[1];
    elif (p[1] == None):
        p[0] = p[1];
    else:
        p[0] = [p[1]];

def p_parametro(p):
    """
    parametro : IDENTIFICADOR DOS_PUNTOS referencia declaracion_tipo
        | empty
    """
    if (len(p) == 2):
        p[0] = p[1];
    elif (isinstance(p[4], Dimension)):
        if (len(p[4].dimensiones) == 0):
            p[0] = Arreglo(True, p[1], p[4], [], True, None, p.lineno(1), p.lexpos(1));
        else:
            p[0] = Arreglo(True, p[1], p[4], [], False, None, p.lineno(1), p.lexpos(1));
    else:
        p[0] = Declaracion(True, p[1], p[4], None, p.lineno(1), p.lexpos(1));

def p_referencia(p):
    """
    referencia : AMPERSON MUT
        | empty
    """

def p_retorno_fn(p):
    """
    retorno_fn : FLECHA_GUION declaracion_tipo
        | empty
    """
    if (len(p) == 2):
        p[0] = p[1];
    else:    
        p[0] = p[2];

# lista de instrucciones
def p_instrucciones(p):
    """
    instrucciones : instrucciones instruccion 
        | instruccion
    """
    if (len(p) == 3):
        p[1].append(p[2]); p[0] = p[1];
    else:
        p[0] = [p[1]];

# declaracion de variables
def p_instruccion(p):
    """
    instruccion : declaracion PUNTO_COMA
        | imprimir PUNTO_COMA
        | asignacion PUNTO_COMA
        | if
        | match
        | expresion
        | loop
        | while
        | for_in
        | funciones_vector PUNTO_COMA
        | llamada_funcion PUNTO_COMA
        | BREAK retorno PUNTO_COMA
        | CONTINUE PUNTO_COMA
        | RETURN retorno PUNTO_COMA
    """
    if (p[1] == 'break'):
        p[0] = Transferencia(p[2], TipoTransferencia.BREAK, p.lineno(1), p.lexpos(1));
    elif(p[1] == 'continue'):
        p[0] = Transferencia(None, TipoTransferencia.CONTINUE, p.lineno(1), p.lexpos(1));
    elif(p[1] == 'return'):
        p[0] = Transferencia(p[2], TipoTransferencia.RETURN, p.lineno(1), p.lexpos(1));
    else:
        p[0] = p[1];
    
def p_retorno(p):
    """
    retorno : expresion
        | empty
    """
    p[0] = p[1];

def p_declaracion(p):
    """
    declaracion : LET MUT IDENTIFICADOR DOS_PUNTOS declaracion_tipo igualacion
        | LET MUT IDENTIFICADOR igualacion
        | LET IDENTIFICADOR DOS_PUNTOS declaracion_tipo igualacion
        | LET IDENTIFICADOR igualacion
    """
    if (len(p) == 7):
        if (isinstance(p[6], Expresion) or isinstance(p[6], Instruccion)):
            p[0] = Declaracion(True, p[3], p[5], p[6], p.lineno(1), p.lexpos(1));
        elif(isinstance(p[6], tuple) == True or (isinstance(p[6], Dimension) and p[6].esVector == False)):
            p[0] = Arreglo(True, p[3], p[5], p[6], False, None, p.lineno(1), p.lexpos(1));
        elif(isinstance(p[6], list) == True or (isinstance(p[6], Dimension) and p[6].esVector == True)):
            p[0] = Arreglo(True, p[3], p[5], p[6], True, None, p.lineno(1), p.lexpos(1));
        elif(p[6] == 'new'):
            p[0] = Arreglo(True, p[3], p[5], [], True, None, p.lineno(1), p.lexpos(1));
        elif(isinstance(p[6], WithCapacity)):
            p[0] = Arreglo(True, p[3], p[5], [], True, p[6].capacidad, p.lineno(1), p.lexpos(1));
        elif (isinstance(p[6], ExpresionesStruct)):
            p[0] = InstanciaStruct(True, p[3], p[5], p[6], p.lineno(1), p.lexpos(1));
    elif (len(p) == 5):
        if (isinstance(p[4], Expresion) or isinstance(p[4], Instruccion)):
            p[0] = Declaracion(True, p[3], None, p[4], p.lineno(1), p.lexpos(1));
        elif(isinstance(p[4], tuple) == True or (isinstance(p[4], Dimension) and p[4].esVector == False)):
            p[0] = Arreglo(True, p[3], None, p[4], False, None, p.lineno(1), p.lexpos(1));
        elif(isinstance(p[4], list) == True or (isinstance(p[4], Dimension) and p[4].esVector == True)):
            p[0] = Arreglo(True, p[3], None, p[4], True, None, p.lineno(1), p.lexpos(1));
        elif(p[4] == 'new'):
            p[0] = Arreglo(True, p[3], None, [], True, None, p.lineno(1), p.lexpos(1));
        elif(isinstance(p[4], WithCapacity)):
            p[0] = Arreglo(True, p[3], None, [], True, p[4].capacidad, p.lineno(1), p.lexpos(1));
        elif (isinstance(p[4], ExpresionesStruct)):
            p[0] = InstanciaStruct(True, p[3], None, p[4], p.lineno(1), p.lexpos(1));
    elif (len(p) == 6):
        if (isinstance(p[5], Expresion) or isinstance(p[5], Instruccion)):
            p[0] = Declaracion(False, p[2], p[4], p[5], p.lineno(1), p.lexpos(1));
        elif(isinstance(p[5], tuple) == True or (isinstance(p[5], Dimension) and p[5].esVector == False)):
            p[0] = Arreglo(False, p[2], p[4], p[5], False, None, p.lineno(1), p.lexpos(1));
        elif(isinstance(p[5], list) == True or (isinstance(p[5], Dimension) and p[5].esVector == True)):
            p[0] = Arreglo(False, p[2], p[4], p[5], True, None, p.lineno(1), p.lexpos(1));
        elif(p[5] == 'new'):
            p[0] = Arreglo(False, p[2], p[4], [], True, None, p.lineno(1), p.lexpos(1));
        elif(isinstance(p[5], WithCapacity)):
            p[0] = Arreglo(False, p[2], p[4], [], True, p[5].capacidad, p.lineno(1), p.lexpos(1));
        elif (isinstance(p[5], ExpresionesStruct)):
            p[0] = InstanciaStruct(True, p[2], p[4], p[5], p.lineno(1), p.lexpos(1));
    else:
        if (isinstance(p[3], Expresion) or isinstance(p[3], Instruccion)):
            p[0] = Declaracion(False, p[2], None, p[3], p.lineno(1), p.lexpos(1));
        elif(isinstance(p[3], tuple) == True or (isinstance(p[3], Dimension) and p[3].esVector == False)):
            p[0] = Arreglo(False, p[2], None, p[3], False, None, p.lineno(1), p.lexpos(1));
        elif(isinstance(p[3], list) == True or (isinstance(p[3], Dimension) and p[3].esVector == True)):
            p[0] = Arreglo(False, p[2], None, p[3], True, None, p.lineno(1), p.lexpos(1));
        elif(p[3] == 'new'):
            p[0] = Arreglo(False, p[2], None, [], True, None, p.lineno(1), p.lexpos(1));
        elif(isinstance(p[3], WithCapacity)):
            p[0] = Arreglo(False, p[2], None, [], True, p[3].capacidad, p.lineno(1), p.lexpos(1));
        elif (isinstance(p[3], ExpresionesStruct)):
            p[0] = InstanciaStruct(True, p[5], None, p[3], p.lineno(1), p.lexpos(1));

def p_declaracion_tipo(p):
    """
    declaracion_tipo : type
        | type_arreglo
        | type_vector
    """
    p[0] = p[1];

def p_type(p):
    """
    type : I64
        | F64
        | BOOL  
        | CHAR
        | STRING
        | IDENTIFICADOR 
        | USIZE
        | AMPERSON STR
    """
    # POSIBLE EFE POR EL IDENTIFICADOR
    if (len(p) == 2):
        p[0] = p[1];
    elif (len(p) == 3):
        p[0] = p[2];

def p_type_arreglo(p):
    """
    type_arreglo : CORCHETE_ABRE type_arreglo PUNTO_COMA ENTERO CORCHETE_CIERRA
        | type 
    """
    if (len(p) == 2):
        p[0] = Dimension(p[1], [], False);
    else:
        p[2].dimensiones.append(p[4]); p[0] = p[2];

def p_type_vector(p):
    """
    type_vector : VEC_OBJ MENOR declaracion_tipo MAYOR
    """
    p[0] = Dimension(p[3], [], True);

def p_igualacion(p):
    """
    igualacion : IGUALACION expresion
        | IGUALACION CORCHETE_ABRE lista_arreglo CORCHETE_CIERRA
        | IGUALACION declaracion_vector
        | IGUALACION instancia_struct
    """
    if (len(p) == 3):
        # expresion o vector
        p[0] = p[2];
    else:
        # arreglo
        if (isinstance(p[3], list) == True):
            p[0] = tuple(p[3]);
        else:
            p[0] = p[3];

def p_instancia_struct(p):
    """
    instancia_struct : IDENTIFICADOR LLAVE_ABRE args_struct LLAVE_CIERRA
    """
    p[0] = ExpresionesStruct(p[1], p[3]);

def p_args_struct(p):
    """
    args_struct : args_struct COMA arg_struct
        | arg_struct
    """
    if (len(p) == 4):
        p[1].append(p[3]); p[0] = p[1];
    else:
        p[0] = [p[1]];

def p_arg_struct(p):
    """
    arg_struct : IDENTIFICADOR DOS_PUNTOS expresion
    """
    p[0] = Declaracion(True, p[1], None, p[3], p.lineno(1), p.lexpos(1));

def p_declaracion_vector(p):
    """
    declaracion_vector : VEC NOT CORCHETE_ABRE lista_vector CORCHETE_CIERRA
        | VEC_OBJ DOS_PUNTOS DOS_PUNTOS NEW PARENTESIS_ABRE PARENTESIS_CIERRA
        | VEC_OBJ DOS_PUNTOS DOS_PUNTOS WITH_CAPACITY PARENTESIS_ABRE expresion PARENTESIS_CIERRA
    """
    if (len(p) == 8):
        p[0] = WithCapacity(True, p[6]);
    else:
        if (isinstance(p[4], Dimension)):
            p[4].esVector = True;
        p[0] = p[4];

def p_lista_arreglo(p):
    """
    lista_arreglo : lista_arreglo COMA CORCHETE_ABRE lista_arreglo CORCHETE_CIERRA
        | CORCHETE_ABRE lista_arreglo CORCHETE_CIERRA
        | expresiones_arreglo   
    """
    if (len(p) == 6):
        p[1].append(p[4]); p[0] = p[1];
    elif (len(p) == 4):
        p[0] = [p[2]];
    else:
        p[0] = p[1];

def p_lista_vector(p):
    """
    lista_vector : lista_vector COMA VEC NOT CORCHETE_ABRE lista_vector CORCHETE_CIERRA
        | VEC NOT CORCHETE_ABRE lista_vector CORCHETE_CIERRA
        | expresiones_arreglo   
    """
    if (len(p) == 8):
        p[1].append(p[6]); p[0] = p[1];
    elif (len(p) == 6):
        p[0] = [p[4]];
    else:
        p[0] = p[1];

def p_expresiones_arreglo(p):
    """
    expresiones_arreglo : expresiones
        | expresion PUNTO_COMA ENTERO
    """
    if (len(p) == 2):
        p[0] = p[1];
    else:
        p[0] = Dimension(p[1], [p[3]], False);

# unidad aritmética
def p_expresion_aritmetica(p):
    """
    expresion : RESTA expresion %prec UMENOS
        | potencia PARENTESIS_ABRE expresion COMA expresion PARENTESIS_CIERRA
        | expresion SUMA expresion
        | expresion RESTA expresion
        | expresion MULTIPLICACION expresion
        | expresion DIVISION expresion
        | expresion MODULO expresion
    """
    if (len(p) == 3):
        # numero negativo
        p[0] = Aritmetica(p[2], Literal('-1', p[2].tipo, p.lineno(1), p.lexpos(1)), TipoAritmetica.MULTIPLICACION, p.lineno(1), p.lexpos(1));
    elif (p[1] == 'i64'):
        p[0] = Aritmetica(p[3], p[5], TipoAritmetica.POTENCIA_i64, p.lineno(1), p.lexpos(1));
    elif (p[1] == 'f64'):
        p[0] = Aritmetica(p[3], p[5], TipoAritmetica.POTENCIA_f64, p.lineno(1), p.lexpos(1));
    elif (p[2] == '+'):
        p[0] = Aritmetica(p[1], p[3], TipoAritmetica.SUMA, p.lineno(1), p.lexpos(1));
    elif (p[2] == '-'):
        p[0] = Aritmetica(p[1], p[3], TipoAritmetica.RESTA, p.lineno(1), p.lexpos(1));
    elif (p[2] == '*'):
        p[0] = Aritmetica(p[1], p[3], TipoAritmetica.MULTIPLICACION, p.lineno(1), p.lexpos(1));
    elif (p[2] == '/'):
        p[0] = Aritmetica(p[1], p[3], TipoAritmetica.DIVISION, p.lineno(1), p.lexpos(1));
    elif (p[2] == '%'):
        p[0] = Aritmetica(p[1], p[3], TipoAritmetica.MODULO, p.lineno(1), p.lexpos(1));

def p_potencia(p):
    """
    potencia : I64 DOS_PUNTOS DOS_PUNTOS POTENCIA_i64
        | F64 DOS_PUNTOS DOS_PUNTOS POTENCIA_f64
    """
    p[0] = p[1];

# unidad relacional
def p_expresion_relacional(p):
    """
    expresion : expresion IGUALDAD expresion
        | expresion DESIGUALDAD expresion
        | expresion MENOR_IGUAL expresion
        | expresion MAYOR_IGUAL expresion
        | expresion MENOR expresion
        | expresion MAYOR expresion
    """
    if (p[2] == '=='):
        p[0] = Relacional(p[1], p[3], TipoRelacional.IGUALDAD, p.lineno(1), p.lexpos(1));
    elif (p[2] == '!='):
        p[0] = Relacional(p[1], p[3], TipoRelacional.DESIGUALDAD, p.lineno(1), p.lexpos(1));
    elif (p[2] == '<='):
        p[0] = Relacional(p[1], p[3], TipoRelacional.MENOR_IGUAL, p.lineno(1), p.lexpos(1));
    elif (p[2] == '>='):
        p[0] = Relacional(p[1], p[3], TipoRelacional.MAYOR_IGUAL, p.lineno(1), p.lexpos(1));
    elif (p[2] == '<'):
        p[0] = Relacional(p[1], p[3], TipoRelacional.MENOR, p.lineno(1), p.lexpos(1));
    elif (p[2] == '>'):
        p[0] = Relacional(p[1], p[3], TipoRelacional.MAYOR, p.lineno(1), p.lexpos(1));

# unidad lógica
def p_expresion_logica(p):
    """
    expresion : NOT expresion
        | expresion OR expresion
        | expresion AND expresion
    """
    if (len(p) == 3):
        p[0] = Logico(p[2], None, TipoLogico.NOT, p.lineno(1), p.lexpos(1))
    elif (p[2] == '||'):
        print(str(p[1]) + " || " + str(p[3]))
        p[0] = Logico(p[1], p[3], TipoLogico.OR, p.lineno(1), p.lexpos(1))
    elif (p[2] == '&&'):
        print(str(p[1]) + " && " + str(p[3]))
        p[0] = Logico(p[1], p[3], TipoLogico.AND, p.lineno(1), p.lexpos(1))

def p_expresion_terminales(p):
    """
    expresion : ENTERO
        | DECIMAL   
        | TRUE
        | FALSE
        | CARACTER
    """
    # terminales
    if (type(p[1]) == int):
        # enteros
        p[0] = Literal(p[1], TipoDato.INT64, p.lineno(1), p.lexpos(1));
    elif (type(p[1]) == float):
        # decimales
        p[0] = Literal(p[1], TipoDato.FLOAT64, p.lineno(1), p.lexpos(1));
    elif (p[1] == 'true' or p[1] == 'false'):
        # bools
        boolean = True if (p[1] == 'true') else False;
        p[0] = Literal(boolean, TipoDato.BOOLEAN, p.lineno(1), p.lexpos(1));
    else:
        # chars
        p[0] = Literal(p[1], TipoDato.CHAR, p.lineno(1), p.lexpos(1));

def p_expresion_strings(p):
    """
    expresion : CADENA
    """
    # strings
    p[0] = Literal(p[1], TipoDato.STRING, p.lineno(1), p.lexpos(1));

def p_expresion_identificador(p):
    """
    expresion : IDENTIFICADOR
        | IDENTIFICADOR indice_arreglo
        | expresion PUNTO IDENTIFICADOR
    """
    if (len(p) == 2):
        p[0] = Acceso(p[1], p.lineno(1), p.lexpos(1));
    elif (len(p) == 3):
        p[0] = AccesoArreglo(p[1], p[2], p.lineno(1), p.lexpos(1));
    else:
        p[0] = AccesoStruct(p[1], p[3], p.lineno(1), p.lexpos(1));

def p_indice_arreglo(p):
    """
    indice_arreglo : indice_arreglo CORCHETE_ABRE expresion CORCHETE_CIERRA
    | CORCHETE_ABRE expresion CORCHETE_CIERRA
    """
    if (len(p) == 5):
        p[1].append(p[3]); p[0] = p[1];
    else:
        p[0] = [p[2]];

def p_expresion_inst(p):
    """
    expresion : if
        | match
        | imprimir
        | asignacion
        | loop
        | funciones_vector
        | llamada_funcion 
    """
    p[0] = p[1];

def p_expresion_nativas(p):
    """
    expresion : expresion PUNTO funcion_nativa PARENTESIS_ABRE PARENTESIS_CIERRA
    """
    if(p[3] == TipoNativo.ABS):
        p[0] = Abs(p[1], p.lineno(1), p.lexpos(1));
    elif(p[3] == TipoNativo.SQRT):
        p[0] = Sqrt(p[1], p.lineno(1), p.lexpos(1));
    elif(p[3] == TipoNativo.TO_STRING or p[3] == TipoNativo.TO_OWNED):
        p[0] = ToString(p[1], p.lineno(1), p.lexpos(1));
    elif(p[3] == TipoNativo.CLONE):
        p[0] = Clone(p[1], p.lineno(1), p.lexpos(1));
    elif(p[3] == TipoNativo.CHARS):
        p[0] = Chars(p[1], p.lineno(1), p.lexpos(1));

def p_funcion_nativa(p):
    """
    funcion_nativa : ABS
        | SQRT
        | TO_STRING
        | CLONE
        | TO_OWNED
        | CHARS
    """
    if (p[1] == 'abs'):
        p[0] = TipoNativo.ABS;
    elif (p[1] == 'sqrt'):
        p[0] = TipoNativo.SQRT;
    elif (p[1] == 'to_string'):
        p[0] = TipoNativo.TO_STRING;
    elif (p[1] == 'clone'):
        p[0] = TipoNativo.CLONE;
    elif (p[1] == 'to_owned'):
        p[0] = TipoNativo.TO_OWNED;
    elif (p[1] == 'chars'):
        p[0] = TipoNativo.CHARS;

def p_expresion_varios(p):
    """
    expresion : PARENTESIS_ABRE expresion PARENTESIS_CIERRA
        | expresion AS type
    """
    if (p[1] == '(' and p[3] == ')'):
        p[0] = p[2];
    else:
        p[0] = Casteo(p[1], p[3], p.lineno(1), p.lexpos(1));

# impresión en consola (println)
def p_imprimir(p):
    """
    imprimir : tipo_impresion NOT PARENTESIS_ABRE CADENA COMA expresiones PARENTESIS_CIERRA
        | tipo_impresion NOT PARENTESIS_ABRE CADENA PARENTESIS_CIERRA
    """
    if (len(p) == 8):
        p[0] = Imprimir(p[1], p[4], p[6], p.lineno(1), p.lexpos(1));
    else:
        p[0] = Imprimir(p[1], p[4], None, p.lineno(1), p.lexpos(1));

def p_tipo_impresion(p):
    """
    tipo_impresion : PRINTLN
        | PRINT
    """
    if (p[1] == 'println'):
        p[0] = True;
    else:
        p[0] = False;

# expresiones para el println
def p_expresiones(p):
    """
    expresiones : expresiones COMA tipo_expresion
        | tipo_expresion
    """
    if (len(p) == 4):
        p[1].append(p[3]); p[0] = p[1];
    else:
        p[0] = [p[1]];

def p_tipo_expresion(p):
    """
    tipo_expresion : AMPERSON MUT expresion
        | expresion
    """
    if (len(p) == 4):
        p[0] = Puntero(p[3]);
    else:
        p[0] = p[1];

def p_asignacion(p):
    """
    asignacion : IDENTIFICADOR igualacion
        | IDENTIFICADOR indice_arreglo igualacion
        | expresion PUNTO IDENTIFICADOR igualacion
    """
    if (len(p) == 3):
        p[0] = Asignacion(p[1], p[2], p.lineno(1), p.lexpos(1));
    elif (len(p) == 5):
        p[0] = AsignacionStruct(p[1], p[3], p[4], p.lineno(1), p.lexpos(1));
    else:
        p[0] = AsignacionArreglo(p[1], p[2], p[3], p.lineno(1), p.lexpos(1));

def p_if(p):
    """
    if : IF expresion bloque else
    """
    p[0] = IfElse(p[2], p[3], p[4], p.lineno(1), p.lexpos(1));

def p_else(p):
    """
    else : ELSE bloque
        | ELSE if
        | empty
    """
    if (len(p) == 3):
        p[0] = p[2];
    else:
        p[0] = p[1];

def p_bloque(p):
    """
    bloque : LLAVE_ABRE instrucciones LLAVE_CIERRA
        | LLAVE_ABRE LLAVE_CIERRA
    """
    if (len(p) == 4):
        p[0] = Bloque(p[2], p.lineno(1), p.lexpos(1));
    else:
        p[0] = Bloque([], p.lineno(1), p.lexpos(1));

def p_match(p):
    """
    match : MATCH expresion LLAVE_ABRE case_list LLAVE_CIERRA
    """
    p[0] = Match(p[2], p[4], p.lineno(1), p.lexpos(1));

def p_case_list(p):
    """
    case_list : case_list case
        | case
    """
    if (len(p) == 3):
        p[1].append(p[2]); p[0] = p[1];
    else:
        p[0] = [p[1]];   

def p_case(p):
    """
    case : coincidencias FLECHA_IGUAL cuerpo_match
    """
    p[0] = Case(p[1], p[3], p.lineno(1), p.lexpos(1));

def p_coincidencias(p):
    """
    coincidencias : coincidencias BARRA expresion
        | expresion
        | GUION_BAJO
    """
    if (len(p) == 4):
        p[1].append(p[3]); p[0] = p[1];
    else:
        p[0] = [p[1]];  

def p_cuerpo_match(p):
    """
    cuerpo_match : expresion COMA
        | bloque
    """
    p[0] = p[1];

def p_loop(p):
    """
    loop : LOOP bloque
    """
    p[0] = Loop(p[2], p.lineno(1), p.lexpos(1));

def p_while(p):
    """
    while : WHILE expresion bloque
    """
    p[0] = While(p[2], p[3], p.lineno(1), p.lexpos(1));

def p_for_in(p):
    """
    for_in : FOR IDENTIFICADOR IN iterables bloque
    """
    p[0] = ForIn(p[2], p[4], p[5], p.lineno(1), p.lexpos(1));

def p_iterables(p):
    """
    iterables : expresion PUNTO PUNTO expresion
        | expresion
        | CORCHETE_ABRE lista_arreglo CORCHETE_CIERRA
    """
    if (len(p) == 2):
        p[0] = p[1];
    elif (len(p) == 5):
        lista = []; lista.append(p[1]); lista.append(p[4]); p[0] = lista;
    else:
        p[0] = p[2];

def p_funciones_vector(p):
    """
    funciones_vector : expresion PUNTO PUSH PARENTESIS_ABRE expresion PARENTESIS_CIERRA
        | expresion PUNTO INSERT PARENTESIS_ABRE expresion COMA expresion PARENTESIS_CIERRA
        | expresion PUNTO REMOVE PARENTESIS_ABRE expresion PARENTESIS_CIERRA
        | expresion PUNTO CONTAINS PARENTESIS_ABRE AMPERSON expresion PARENTESIS_CIERRA
        | expresion PUNTO LEN PARENTESIS_ABRE PARENTESIS_CIERRA
        | expresion PUNTO CAPACITY PARENTESIS_ABRE PARENTESIS_CIERRA
    """
    if (p[3] == 'push'):
        p[0] = Push(p[1], p[5], p.lineno(1), p.lexpos(1));
    elif (p[3] == 'insert'):
        p[0] = Insert(p[1], p[5], p[7], p.lineno(1), p.lexpos(1));
    elif (p[3] == 'remove'):
        p[0] = Remove(p[1], p[5], p.lineno(1), p.lexpos(1));
    elif (p[3] == 'contains'):
        p[0] = Contains(p[1], p[6], p.lineno(1), p.lexpos(1));
    elif (p[3] == 'len'):
        p[0] = Longitud(p[1], p.lineno(1), p.lexpos(1));
    elif (p[3] == 'capacity'):
        p[0] = Capacity(p[1], p.lineno(1), p.lexpos(1));

def p_llamada_funcion(p):
    """
    llamada_funcion : IDENTIFICADOR PARENTESIS_ABRE argumentos PARENTESIS_CIERRA
    """
    p[0] = LlamadaFuncion(p[1], p[3], p.lineno(1), p.lexpos(1));

def p_argumentos(p):
    """
    argumentos : expresiones
        | empty
    """
    p[0] = p[1];

def p_empty(p):
    """
    empty :
    """
    p[0] = None;

# error sintáctico
def p_error(p):
    raise Exception(f'Error de sintaxis {p.type}, linea: {p.lineno}, columna: {p.lexpos}');

# construyendo el parser (analizador sintáctico)
parser = yacc()