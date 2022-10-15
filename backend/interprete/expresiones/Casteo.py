from ..extra.Tipos import TipoDato
from .Expresion import Expresion
from ..extra.Scope import Scope
from ..extra.Console import Console, _Error
from ..extra.Retorno import RetornoExpresion
from datetime import datetime

class Casteo(Expresion):
    def __init__(self, expresion:Expresion, tipo:str, linea, columna):
        super().__init__(linea, columna);
        self.expresion = expresion;
        self.tipo = tipo;

    def ejecutar(self, console: Console, scope: Scope):
        # recuperamos la expresion
        self.expresion.generador = self.generador;
        val:RetornoExpresion = self.expresion.ejecutar(console, scope);
        if (self.tipo == TipoDato.INT64):
            val.tipo = TipoDato.INT64;
            return val;
        elif (self.tipo == TipoDato.FLOAT64):
            val.tipo == TipoDato.FLOAT64;
            return val;
        elif (self.tipo == TipoDato.BOOLEAN):
            '''
            if (val.valor == 1) goto Ltrue;
            goto Lfalse;
            '''
            val.tipo = TipoDato.BOOLEAN;
            val.trueEtq:str = self.generador.newEtq();
            val.falseEtq:str = self.generador.newEtq();
            self.generador.addIf(val.valor, '1', '==', val.trueEtq);
            self.generador.addGoto(val.falseEtq);
            return val;
        elif (self.tipo == TipoDato.CHAR):
            val.tipo = TipoDato.CHAR;
            return val;
        elif (self.tipo == TipoDato.STRING):
            val.tipo = TipoDato.STRING;
            return val;
        elif (self.tipo == TipoDato.STR):
            val.tipo = TipoDato.STR;
            return val;