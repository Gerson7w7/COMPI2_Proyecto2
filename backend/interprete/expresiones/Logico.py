from interprete.extra.Retorno import RetornoExpresion
from interprete.extra.Tipos import TipoDato
from interprete.extra.Tipos import TipoLogico
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class Logico(Expresion):
    def __init__(self, izquierda, derecha, tipo:TipoLogico, linea, columna):
        super().__init__(linea, columna)
        self.izquierda = izquierda;
        self.derecha = derecha;
        self.tipo = tipo;

    def ejecutar(self, console: Console, scope: Scope):
        # ejecutando los valores
        val1 = self.izquierda.ejecutar(console, scope);
        val2 = self.derecha.ejecutar(console,scope) if (self.derecha != None) else None;

        # verificando si se trata de NOT
        if (val2 != None):
            if (val1.tipo == TipoDato.BOOLEAN and val2.tipo == TipoDato.BOOLEAN):
                # OR
                if (self.tipo == TipoLogico.OR):
                    print("or: " + str(val1.valor or val2.valor))
                    return RetornoExpresion(val1.valor or val2.valor, TipoDato.BOOLEAN, None);
                # AND
                print("and: " + str(val1.valor and val2.valor))
                return RetornoExpresion(val1.valor and val2.valor, TipoDato.BOOLEAN, None);
            # error solo se acepta bools
            _error = _Error(f'Solo se puede comparar a nivel lógico tipos booleanos', scope.ambito, self.linea, self.columna, datetime.now())
            raise Exception(_error);
        else:
            # NOT
            if (val1.tipo == TipoDato.BOOLEAN):
                print("not: " + str(not val1.valor))
                return RetornoExpresion(not val1.valor, TipoDato.BOOLEAN, None);
            # ERROR solo se aceptan bools
            _error = _Error(f'Solo se puede comparar a nivel lógico tipos booleanos', scope.ambito, self.linea, self.columna, datetime.now())
            raise Exception(_error);