from ..extra.Tipos import TipoDato
from .Expresion import Expresion
from ..extra.Scope import Scope
from ..extra.Console import Console, _Error
from ..extra.Retorno import RetornoExpresion
from datetime import datetime

class Casteo(Expresion):
    def __init__(self, expresion, tipo:str, linea, columna):
        super().__init__(linea, columna);
        self.expresion = expresion;
        self.tipo = tipo;

    def ejecutar(self, console: Console, scope: Scope):
        # recuperamos la expresion
        val = self.expresion.ejecutar(console, scope);
        if (self.tipo == 'i64' or self.tipo == 'usize'):
            return RetornoExpresion(int(val.valor), TipoDato.INT64, None);
        elif (self.tipo == 'f64'):
            try:
                return RetornoExpresion(float(val.valor), TipoDato.FLOAT64, None);
            except:
                # ERROR. no se puede convertir en bool
                _error = _Error(f'La expresión {val.valor} no se puede convertir a float', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
        elif (self.tipo == 'bool'):
            try:
                return RetornoExpresion(bool(val.valor), TipoDato.BOOLEAN, None);   
            except:
                # ERROR. no se puede convertir en bool
                _error = _Error(f'La expresión {val.valor} no se puede convertir a bool', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
        elif (self.tipo == 'char'):
            if (len(val.valor) == 1):
                return RetornoExpresion(str(val.valor), TipoDato.CHAR, None);
            # ERROR. no se puede convertir en char
            _error = _Error(f'La expresión {val.valor} no se puede convertir a char', scope.ambito, self.linea, self.columna, datetime.now())
            raise Exception(_error);
        elif (self.tipo == 'string'):
            return RetornoExpresion(str(val.valor), TipoDato.STRING, None);
        elif (self.tipo == 'str'):
            return RetornoExpresion(str(val.valor), TipoDato.STR, None);