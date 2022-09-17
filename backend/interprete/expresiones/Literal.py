from .Expresion import Expresion
from ..extra.Tipos import TipoDato
from ..extra.Console import Console
from ..extra.Scope import Scope
from ..extra.Retorno import RetornoExpresion

class Literal(Expresion):
    def __init__(self, valor, tipo: TipoDato, linea: int, columna: int):
        super().__init__(linea, columna)
        self.valor = valor;
        self.tipo = tipo;
    
    def ejecutar(self, console: Console, scope: Scope):
        if (self.tipo == TipoDato.INT64):
            return RetornoExpresion(str(self.valor), TipoDato.INT64, None, False);
        elif (self.tipo == TipoDato.FLOAT64):
            return RetornoExpresion(str(self.valor), TipoDato.FLOAT64, None, False);
        elif (self.tipo == TipoDato.BOOLEAN):
            return RetornoExpresion(str(self.valor), TipoDato.BOOLEAN, None, False);
        elif (self.tipo == TipoDato.CHAR):
            return RetornoExpresion(str(self.valor), TipoDato.CHAR, None, False);
        elif (self.tipo == TipoDato.STRING or self.tipo == TipoDato.STR):
            newTemp = self.generador.newTemp();
            # añadimos tn = H;
            self.generador.addOperacion(newTemp, 'H', '', '');
            # recorremos el string
            for c in self.valor:
                self.generador.setHeap('H', str(ord(c)));
                self.generador.ptrNextHeap();
            self.generador.setHeap('H', '-1');
            self.generador.ptrNextHeap();
            return RetornoExpresion(newTemp, TipoDato.STR, None, True);
        # sino error sintactico
