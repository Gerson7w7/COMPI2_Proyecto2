from .Instruccion import Instruccion
from ..extra.Tipos import TipoTransferencia
from ..extra.Scope import Scope
from ..extra.Console import Console
from ..extra.Retorno import RetornoExpresion

class Transferencia(Instruccion):
    def __init__(self, retorno, tipo:TipoTransferencia, linea: int, columna: int):
        super().__init__(linea, columna)
        self.retorno = retorno;
        self.tipo = tipo;

    def ejecutar(self, console: Console, scope: Scope):
        val = None if (self.retorno == None) else self.retorno.ejecutar(console, scope);
        if (val == None):
            return RetornoExpresion(None, None, self.tipo);
        return RetornoExpresion(val.valor, val.tipo, self.tipo);