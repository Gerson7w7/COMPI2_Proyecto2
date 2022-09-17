from ..extra.Retorno import RetornoExpresion
from .Expresion import Expresion
from ..extra.Tipos import TipoDato, TipoRelacional
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class Relacional(Expresion):
    def __init__(self, izquierda, derecha, tipo:TipoRelacional, linea, columna):
        super().__init__(linea, columna)
        self.izquierda = izquierda
        self.derecha = derecha
        self.tipo: TipoRelacional = tipo

    def ejecutar(self, console: Console, scope: Scope):
        # ejecutando las expresiones
        val1 = self.izquierda.ejecutar(console, scope);
        val2 = self.derecha.ejecutar(console, scope);
        esStr = False;
        if (val1.tipo == TipoDato.STRING or val1.tipo == TipoDato.STR):
            if (val2.tipo == TipoDato.STRING or val2.tipo == TipoDato.STR):
                esStr = True;
        # primero comprobamos que sea el mismo tipo de dato de ambos lados
        if (val1.tipo == val2.tipo or esStr):
            # comprobamos que el tipo de dato se pueda operar
            if (val1.tipo == TipoDato.INT64 or val1.tipo == TipoDato.FLOAT64 or esStr):
                # operamos los valores
                return self.Operando(val1, val2, scope);
        # ERROR tienen que ser del mismo tipo
        _error = _Error(f'Solo se puede comparar a nivel relacional si las dos expresiones son del mismo tipo', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);
    
    def Operando(self, val1, val2, scope:Scope):
        if (self.tipo == TipoRelacional.IGUALDAD):
            print("igualdad : " + str(val1.valor == val2.valor));
            return RetornoExpresion(val1.valor == val2.valor, TipoDato.BOOLEAN, None);
        elif (self.tipo == TipoRelacional.DESIGUALDAD):
            print("desigualdad : " + str(val1.valor !=val2.valor));
            return RetornoExpresion(val1.valor != val2.valor, TipoDato.BOOLEAN, None);
        elif (self.tipo == TipoRelacional.MENOR_IGUAL):
            print("menorigual : " + str(val1.valor <=val2.valor));
            return RetornoExpresion(val1.valor <= val2.valor, TipoDato.BOOLEAN, None);
        elif (self.tipo == TipoRelacional.MAYOR_IGUAL):
            print("mayorigual : " + str(val1.valor >=val2.valor));
            return RetornoExpresion(val1.valor >= val2.valor, TipoDato.BOOLEAN, None);
        elif (self.tipo == TipoRelacional.MENOR):
            print("menor : " + str(val1.valor < val2.valor));
            return RetornoExpresion(val1.valor < val2.valor, TipoDato.BOOLEAN, None);
        elif (self.tipo == TipoRelacional.MAYOR):
            print("mayor : " + str(val1.valor > val2.valor));
            return RetornoExpresion(val1.valor > val2.valor, TipoDato.BOOLEAN, None);
        # ERROR no se ha podido operar
        _error = _Error(f'No se ha podido efectuar la operacion {self.tipo} con {val1.valor} y {val2.valor}', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);