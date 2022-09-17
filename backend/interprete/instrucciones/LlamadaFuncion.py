from ..extra.Simbolo import Simbolo
from .Funcion import Funcion
from .Instruccion import Instruccion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from ..extra.Retorno import RetornoExpresion
from datetime import datetime

class LlamadaFuncion(Instruccion):
    def __init__(self, id:str, argumentos:list, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.argumentos = argumentos;
    
    def ejecutar(self, console: Console, scope: Scope):
        newScope = Scope(scope.getGlobal(), 'Funcion');
        # obtenemos la función 
        funcion:Funcion = scope.getFuncion(self.id, self.linea, self.columna);
        # verificando si la cantidad de argumentos son == a la cantidad de parámetros de la función
        if (len(self.argumentos) != len(funcion.parametros)):
            # ERROR. Se esperaban x parametros y se encontraron x argumentos
            _error = _Error(f'Se esperaban {len(funcion.parametros)} parametros y se encontraron {len(self.argumentos)} argumentos', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        for i in range(len(self.argumentos)):
            if (isinstance(self.argumentos[i], Puntero)):
                val = self.argumentos[i].expresion.ejecutar(console, scope);
            else:
                val = self.argumentos[i].ejecutar(console, scope);
            # verificando el tipo correcto del argumento
            funcion.tipoArgumentos(val.tipo, i, console, scope);
            # obtenemos el id del parametro correspondiente
            idParam = funcion.parametros[i].id;
            if (isinstance(self.argumentos[i], Puntero)):
                idReferencia = self.argumentos[i].expresion.id;
                referencia = Referencia(scope, idReferencia, val);
                newScope.crearVariable(idParam, val.valor, 'Dirección de memoria', val.tipo, True, val.esVector, val.with_capacity, referencia, self.linea, self.columna, console);
            else:
                if (isinstance(val, RetornoExpresion)):
                    newScope.crearVariable(idParam, val.valor, 'Variable', val.tipo, True, None, None, None, self.linea, self.columna, console);
                elif (isinstance(val, Simbolo)):
                    newScope.crearVariable(idParam, val.valor, 'Variable', val.tipo, True, val.esVector, val.with_capacity, val.referencia, self.linea, self.columna, console);
                else:
                    newScope.crearVariable(idParam, val.valor, 'Variable', val.tipo, True, None, None, val.referencia, self.linea, self.columna, console);
        # ejecutando las instrucciones de la función 
        valBloque = funcion.bloque.ejecutar(console, newScope, 'Funcion');
        # verificando el retorno de la función
        if (valBloque != None):
            funcion.tipoRetorno(valBloque.tipo, scope);
        else:
            funcion.tipoRetorno(None, scope);
        return valBloque;

class Referencia:
    def __init__(self, scope:Scope, id:str, val):
        self.scope = scope;
        self.id = id;
        self.val = val;

class Puntero:
    def __init__(self, expresion):
        self.expresion = expresion;