from ..extra.Tipos import TipoTransferencia
from .Instruccion import Instruccion
from ..extra.Console import Console
from ..extra.Scope import Scope

class Loop(Instruccion):
    def __init__(self, bloque: Instruccion, linea: int, columna: int):
        super().__init__(linea, columna)
        self.bloque = bloque;

    def ejecutar(self, console: Console, scope: Scope):
        while(True):
            # ejecutamos las instrucciones dentro del loop
            val = self.bloque.ejecutar(console, scope, 'Loop');
            # si es una instruccion de transferencia se analiza
            if (val != None):
                # break
                if (val.retorno == TipoTransferencia.BREAK):
                    if (val.valor != None):
                        return val;
                    break;
                # return
                elif (val.retorno == TipoTransferencia.RETURN):
                    return val;
                # continua
                elif (val.retorno == TipoTransferencia.CONTINUE):
                    continue;