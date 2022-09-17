from ..extra.Tipos import TipoDato
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from ..extra.Retorno import RetornoExpresion
from datetime import datetime
import math
import copy

class Abs(Expresion):
    def __init__(self, expresion,  linea: int, columna: int):
        super().__init__(linea, columna)
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        val = self.expresion.ejecutar(console, scope);
        # verificamos que sea un tipo de dato numérico
        if (val.tipo == TipoDato.INT64 or val.tipo == TipoDato.FLOAT64):
            return RetornoExpresion(abs(val.valor), val.tipo, None);
        # error, solo se aceptan datos numéricos
        _error = _Error(f'Solo se puede obtener el valor absoluto de un número, no de un {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);

class Sqrt(Expresion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        val = self.expresion.ejecutar(console, scope);
        # verificamos que sea un tipo de dato numérico
        if (val.tipo == TipoDato.INT64 or val.tipo == TipoDato.FLOAT64):
            if (val.valor < 0):
                # error, no existe raiz de numeros negativos 
                _error = _Error(f'No existe la raiz cuadrada de numeros negativos', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
            return RetornoExpresion(math.sqrt(val.valor), val.tipo, None);
        # error, solo se aceptan datos numéricos
        _error = _Error(f'Solo se puede obtener la raíz cuadrada de un número, no de un {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);

# sirve tanto par to_string() como para to_owned() xd
class ToString(Expresion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        val = self.expresion.ejecutar(console, scope);
        # verificamos que sea un tipo de dato str o string
        if (val.tipo == TipoDato.STR or val.tipo == TipoDato.STRING):
            return RetornoExpresion(val.valor, TipoDato.STRING, None);
        # error, solo se aceptan datos string
        _error = _Error(f'Solo se puede convertir a un string un &str, no de un {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);

class Clone(Expresion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        # retorna lo que sea que venga, ya que solo es una copia
        return copy.deepcopy(self.expresion.ejecutar(console, scope));

class Chars(Expresion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        # ejecutamos la expresión
        val = self.expresion.ejecutar(console, scope);
        if (val.tipo != TipoDato.STRING and val.tipo != TipoDato.STR):
            # ERROR. Solo se puede convertir a una lista de caracteres si se trata de un string
            _error = _Error(f'Solo se puede convertir a una lista de caracteres si se trata de un string o &str, no de un {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now())
            raise Exception(_error);
        # pasamos la cadena a una lista
        listaChar:list = []
        for c in val.valor:
            listaChar.append(c);
        return RetornoExpresion(listaChar, val.tipo, None);
