from ..extra.Retorno import RetornoExpresion
from .Expresion import Expresion
from ..extra.Tipos import TipoDato, TipoRelacional
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class Relacional(Expresion):
    def __init__(self, izquierda:Expresion, derecha:Expresion, tipo:TipoRelacional, linea, columna):
        super().__init__(linea, columna);
        self.izquierda = izquierda
        self.derecha = derecha
        self.tipo: TipoRelacional = tipo

    def ejecutar(self, console: Console, scope: Scope):
        # ejecutando las expresiones
        self.izquierda.generador = self.generador;
        val1:RetornoExpresion = self.izquierda.ejecutar(console, scope);
        self.derecha.generador = self.generador;
        val2:RetornoExpresion = self.derecha.ejecutar(console, scope);
        esStr = False;
        if (val1.tipo == TipoDato.STRING or val1.tipo == TipoDato.STR):
            if (val2.tipo == TipoDato.STRING or val2.tipo == TipoDato.STR):
                val1.valor = self.getTotalChars(val1.valor);
                val2.valor = self.getTotalChars(val2.valor);
                esStr = True;
        # primero comprobamos que sea el mismo tipo de dato de ambos lados
        if (val1.tipo == val2.tipo or esStr):
            # comprobamos que el tipo de dato se pueda operar
            if (val1.tipo == TipoDato.INT64 or val1.tipo == TipoDato.FLOAT64 or esStr):
                # operamos los valores
                return self.Operando(val1.valor, val2.valor, scope);
        # ERROR tienen que ser del mismo tipo
        _error = _Error(f'Solo se puede comparar a nivel relacional si las dos expresiones son del mismo tipo', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);
    
    def Operando(self, val1, val2, scope:Scope):
        Ltrue:str = self.generador.newEtq();
        Lfalse:str = self.generador.newEtq();
        if (self.tipo == TipoRelacional.IGUALDAD):
            '''
            if (val1.valor == val2.valor) goto Ltrue;
            goto Lfalse;
            '''
            self.generador.addComentario('RELACIONAL (==)');
            self.generador.addIf(val1, val2, '==', Ltrue);
            self.generador.addGoto(Lfalse);
            retorno = RetornoExpresion('', TipoDato.BOOLEAN, False);
            retorno.trueEtq = Ltrue;
            retorno.falseEtq = Lfalse;
            return retorno;
        elif (self.tipo == TipoRelacional.DESIGUALDAD):
            '''
            if (val1.valor != val2.valor) goto Ltrue;
            goto Lfalse;
            '''
            self.generador.addComentario('RELACIONAL (!=)');
            self.generador.addIf(val1, val2, '!=', Ltrue);
            self.generador.addGoto(Lfalse);
            retorno = RetornoExpresion('', TipoDato.BOOLEAN, False);
            retorno.trueEtq = Ltrue;
            retorno.falseEtq = Lfalse;
            return retorno;
        elif (self.tipo == TipoRelacional.MENOR_IGUAL):
            '''
            if (val1.valor <= val2.valor) goto Ltrue;
            goto Lfalse;
            '''
            self.generador.addComentario('RELACIONAL (<=)');
            self.generador.addIf(val1, val2, '<=', Ltrue);
            self.generador.addGoto(Lfalse);
            retorno = RetornoExpresion('', TipoDato.BOOLEAN, False);
            retorno.trueEtq = Ltrue;
            retorno.falseEtq = Lfalse;
            return retorno;
        elif (self.tipo == TipoRelacional.MAYOR_IGUAL):
            '''
            if (val1.valor >= val2.valor) goto Ltrue;
            goto Lfalse;
            '''
            self.generador.addComentario('RELACIONAL (>=)');
            self.generador.addIf(val1, val2, '>=', Ltrue);
            self.generador.addGoto(Lfalse);
            retorno = RetornoExpresion('', TipoDato.BOOLEAN, False);
            retorno.trueEtq = Ltrue;
            retorno.falseEtq = Lfalse;
            return retorno;
        elif (self.tipo == TipoRelacional.MENOR):
            '''
            if (val1.valor < val2.valor) goto Ltrue;
            goto Lfalse;
            '''
            self.generador.addComentario('RELACIONAL (<)');
            self.generador.addIf(val1, val2, '<', Ltrue);
            self.generador.addGoto(Lfalse);
            retorno = RetornoExpresion('', TipoDato.BOOLEAN, False);
            retorno.trueEtq = Ltrue;
            retorno.falseEtq = Lfalse;
            return retorno;
        elif (self.tipo == TipoRelacional.MAYOR):
            '''
            if (val1.valor > val2.valor) goto Ltrue;
            goto Lfalse;
            '''
            self.generador.addComentario('RELACIONAL (>)');
            self.generador.addIf(val1, val2, '>', Ltrue);
            self.generador.addGoto(Lfalse);
            retorno = RetornoExpresion('', TipoDato.BOOLEAN, False);
            retorno.trueEtq = Ltrue;
            retorno.falseEtq = Lfalse;
            return retorno;
        # ERROR no se ha podido operar
        _error = _Error(f'No se ha podido efectuar la operacion {self.tipo} con {val1.valor} y {val2.valor}', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);

    def getTotalChars(self, valor) -> str:
        '''
        temp = 0;
        Lloop:
            tempChar = HEAP[valor];
            if (tempChar == -1) goto Lsalida;
            temp = temp + tempChar;
            valor = valor + 1;
            goto Lloop;
        Lsalida:
        '''
        temp:str = self.generador.newTemp();
        Lloop:str = self.generador.newEtq();
        tempChar:str = self.generador.newTemp();
        Lsalida:str = self.generador.newEtq();
        self.generador.addComentario('SUMA DE LOS CARACTERES');
        self.generador.addOperacion(temp, '0', '', '');
        self.generador.addEtq(Lloop);
        self.generador.getHeap(tempChar, valor);
        self.generador.addIf(tempChar, '-1', '==', Lsalida);
        self.generador.addOperacion(temp, temp, tempChar, '+');
        self.generador.addOperacion(valor, valor, '1', '+');
        self.generador.addGoto(Lloop);
        self.generador.addEtq(Lsalida);
        return temp;
