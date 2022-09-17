import copy

from .Arreglo import Dimension
from ..extra.Tipos import TipoDato
from ..extra.Simbolo import Simbolo
from .Instruccion import Instruccion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from ..extra.Retorno import RetornoExpresion
from datetime import datetime

class Push(Instruccion):
    def __init__(self, id, expresion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        # ejecutando la expresión
        val = self.expresion.ejecutar(console, scope);
        # obtenemos el vector
        vector:Simbolo = self.id.ejecutar(console, scope);
        if (vector.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función push', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (not vector.esVector):
            # ERROR. Los arreglos no contiene la función push
            _error = _Error(f'Los arreglos {vector.id} no contiene la función push', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (vector.tipo == None):
            vector.tipo = val.tipo;
        if (val.tipo != vector.tipo):
            if (isinstance(vector.tipo, Dimension) and val.tipo != self.devolverTipo(vector.tipo.tipo)):
                # ERROR. Tipos incompatibles
                print(str(val.tipo) +"!="+ str(vector.tipo))
                _error = _Error(f'Tipos incompatibles. No se puede almacenar una expresión {val.tipo.name} en una variable de tipo {vector.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
        vector.valor.append(val.valor);
        # ahora revisaremos si se trata de un vector con un tamaño definido
        if (vector.with_capacity != None):
            if (vector.with_capacity < len(vector.valor) + 1):
                vector.with_capacity = vector.with_capacity * 2;
        scope.setValor(self.id.id, vector, self.linea, self.columna);

    def devolverTipo(self, tipo:str):
        if (tipo == 'i64' or tipo == 'usize'):
            return TipoDato.INT64
        elif (tipo == 'f64'):
            return TipoDato.FLOAT64
        elif (tipo == 'bool'):
            return TipoDato.BOOLEAN
        elif (tipo == 'char'):
            return TipoDato.CHAR
        elif (tipo == 'String'):
            return TipoDato.STRING
        elif (tipo == 'str'):
            return TipoDato.STR
        else:
            return tipo;

class Insert(Instruccion):
    def __init__(self, id:str, exp1, exp2, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.exp1 = exp1;
        self.exp2 = exp2;
    
    def ejecutar(self, console: Console, scope: Scope):
        # ejecutando las expresiones
        val1 = self.exp1.ejecutar(console, scope);
        val2 = self.exp2.ejecutar(console, scope);
        # obtenemos el vector
        vector:Simbolo = self.id.ejecutar(console, scope);
        if (vector.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función Insert', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (not vector.esVector):
            # ERROR. Los arreglos no contiene la función insert
            _error = _Error(f'Los arreglos {vector.id} no contiene la función insert', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (val2.tipo != vector.tipo):
            # ERROR. Tipos incompatibles
            _error = _Error(f'Tipos incompatibles. No se puede almacenar una expresión {val2.tipo.name} en una variable de tipo {vector.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (val1.tipo != TipoDato.INT64):
            # ERROR. No se puede acceder al indice val1.tipo.
            _error = _Error(f'No se puede acceder al indice {val1.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        vector.valor.insert(val1.valor, val2.valor);
        # ahora revisaremos si se trata de un vector con un tamaño definido
        if (vector.with_capacity != None):
            if (vector.with_capacity < len(vector.valor)):
                vector.with_capacity = vector.with_capacity * 2;
        scope.setValor(self.id.id, vector, self.linea, self.columna);

class Remove(Instruccion):
    def __init__(self, id:str, exp, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.exp = exp;

    def ejecutar(self, console: Console, scope: Scope):
        # indice del elemento a eliminar
        val = self.exp.ejecutar(console, scope);
        # obtenemos el vector
        vector:Simbolo = self.id.ejecutar(console, scope);
        if (vector.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función remove', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (not vector.esVector):
            # ERROR. Los arreglos no contiene la función remove
            _error = _Error(f'Los arreglos {vector.id} no contiene la función remove', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (val.tipo != TipoDato.INT64):
            # ERROR. Tipos incompatibles
            _error = _Error(f'Se esperaba una posición de tipo i64 pero se obtuvo un tipo {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # primero obtenemos el elemento que se va a eliminar
        valorRetorno = vector.valor[val.valor];
        # ahora eliminamos el elemento
        vector.valor.remove(valorRetorno);
        # revisaremos si se trata de un vector con un tamaño definido
        if (vector.with_capacity != None):
            if (vector.with_capacity < len(vector.valor)):
                vector.with_capacity = vector.with_capacity * 2;
        scope.setValor(self.id.id, vector, self.linea, self.columna);
        return RetornoExpresion(valorRetorno, vector.tipo, None);

class Contains(Instruccion):
    def __init__(self, id:str, exp, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.exp = exp;
    
    def ejecutar(self, console: Console, scope: Scope):
        # expresion del elemento a buscar
        val = self.exp.ejecutar(console, scope);
        # obtenemos el vector
        vector:Simbolo = self.id.ejecutar(console, scope);
        if (vector.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función contains', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (not vector.esVector):
            # ERROR. Los arreglos no contiene la función contains
            _error = _Error(f'Los arreglos {vector.id} no contiene la función contains', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (val.tipo != vector.tipo):
            # ERROR. Tipos incompatibles
            _error = _Error(f'Tipos incompatibles. No se puede almacenar una expresión {val.tipo.name} en una variable de tipo {vector.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # revisamos si existe el elemento en la lista
        if (val.valor in vector.valor):
            return RetornoExpresion(True, TipoDato.BOOLEAN, None);
        return RetornoExpresion(False, TipoDato.BOOLEAN, None);

class Longitud(Instruccion):
    def __init__(self, id:str, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;

    def ejecutar(self, console: Console, scope: Scope):
        # obtenemos el vector
        vector:Simbolo = self.id.ejecutar(console, scope);
        if (isinstance(vector, RetornoExpresion)):
            # ERROR. No es un vector
            _error = _Error(f'La expresión no es un vector, no contiene la función len', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (vector.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función len', scope.ambito, self.linea, self.columna, datetime.now());
            print(_error.descripcion)
            print("vall:: " + str(vector.valor))
            raise Exception(_error);
        # retornamos la longitud de la lista
        return RetornoExpresion(len(vector.valor), TipoDato.INT64, None);

class Capacity(Instruccion):
    def __init__(self, id:str, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;

    def ejecutar(self, console: Console, scope: Scope):
        # obtenemos el vector
        vector:Simbolo = self.id.ejecutar(console, scope);
        if (vector.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función capacity', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (not vector.esVector):
            # ERROR. Los arreglos no contiene la función capacity
            _error = _Error(f'Los arreglos {vector.id} no contiene la función capacity', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # retornamos la capacidad de la lista
        if (vector.with_capacity != None):
            return RetornoExpresion(vector.with_capacity, TipoDato.INT64, None);
        return RetornoExpresion(len(vector.valor) + 1, TipoDato.INT64, None);