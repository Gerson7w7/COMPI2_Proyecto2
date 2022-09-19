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
        if (self.tipo == TipoDato.STRING or self.tipo == TipoDato.STR):
            '''
            tn = HP;
            HEAP[HP] = 15;
            HP = HP + 1;
            ...
            HEAP[HP] = -1;
            HP = HP + 1; 
            '''
            newTemp = self.generador.newTemp();
            # añadimos tn = H;
            self.generador.addOperacion(newTemp, 'HP', '', '');
            # recorremos el string
            for c in self.valor:
                self.generador.setHeap('HP', str(ord(c)));
                self.generador.ptrNextHeap();
            self.generador.setHeap('HP', '-1');
            self.generador.ptrNextHeap();
            return RetornoExpresion(newTemp, TipoDato.STR, True);
        elif (self.tipo == TipoDato.BOOLEAN):
            '''
            TRUE:
            goto exp.EV;
            FALSE:
            goto exp.EF; 
            '''
            # creamos la etiqueta para true o false
            etq = self.generador.newEtq();
            if(self.valor == 'true'):
                retorno = RetornoExpresion('1', TipoDato.BOOLEAN, False);
                retorno.trueEtq = etq;
                self.generador.addGoto(retorno.trueEtq);
                return retorno;
            retorno = RetornoExpresion('0', TipoDato.BOOLEAN, False);
            retorno.falseEtq = etq;
            self.generador.addGoto(retorno.falseEtq);
            return retorno;
        else:
            return RetornoExpresion(str(self.valor), self.tipo, False);