from .Instruccion import Instruccion
from ..extra.Tipos import TipoTransferencia
from ..extra.Scope import Scope
from ..extra.Console import Console
from ..extra.Retorno import RetornoExpresion
from ..expresiones.Expresion import Expresion
from ..extra.Console import _Error
from datetime import datetime

class Transferencia(Instruccion):
    def __init__(self, retorno:Expresion, tipo:TipoTransferencia, linea: int, columna: int):
        super().__init__(linea, columna)
        self.retorno = retorno;
        self.tipo = tipo;

    def ejecutar(self, console: Console, scope: Scope):
        if (self.tipo == TipoTransferencia.BREAK):
            '''
            <código de retorno (si viniera)>
            goto Lsalida;
            '''
            # retorno de la expresion
            val:RetornoExpresion = None;
            if (self.retorno != None):
                self.retorno.generador = self.generador;
                val = self.retorno.ejecutar(console, scope);
                self.generador.addComentario('-1');
            if (len(console.breaks) != 0):
                self.generador.addGoto(console.breaks.pop());
                if (val != None): return val;
            else:
                _error = _Error(f'No se esperaba la sentencia BREAK', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
        elif (self.tipo == TipoTransferencia.CONTINUE):
            '''
            goto Linicio;
            '''
            if (len(console.continues) != 0):
                self.generador.addGoto(console.continues.pop());
            else:
                _error = _Error(f'No se esperaba la sentencia CONTINUE', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
        elif (self.tipo == TipoTransferencia.RETURN):
            '''
            <código de retorno>
            temp = SP + pos;
            STACK[pos] = val.valor;
            '''
            val:RetornoExpresion = self.retorno.ejecutar(console, scope);
            pos:int = scope.setValor('retorno', val, self.linea, self.columna);
            temp:str= self.generador.newTemp();
            self.generador.addOperacion(temp, 'SP', pos, '+');
            self.generador.setStack(temp, val.valor);