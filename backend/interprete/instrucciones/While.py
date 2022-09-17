from ..extra.Tipos import TipoDato, TipoTransferencia
from .Instruccion import Instruccion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class While(Instruccion):
    def __init__(self, condicion, bloque: Instruccion, linea: int, columna: int):
        super().__init__(linea, columna)
        self.condicion = condicion;
        self.bloque = bloque;

    def ejecutar(self, console: Console, scope: Scope):
        # primero ejecutamos la condición
        valCondicion = self.condicion.ejecutar(console, scope);
        # verificando de que se trate de un boolean
        if (valCondicion.tipo != TipoDato.BOOLEAN):
            # error tiene que se bool
            _error = _Error(f'Se esperaba un bool como condición pero se obtuvo {valCondicion.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        while(valCondicion.valor):
            # ejecutamos las instrucciones dentro del loop
            val = self.bloque.ejecutar(console, scope, 'While');
            # si es una instruccion de transferencia se analiza
            if (val != None):
                # break
                if (val.retorno == TipoTransferencia.BREAK):
                    if (val.valor != None):
                        # error no se puede retornar un valor en un while
                        _error = _Error(f'No se puede retornar un valor con un break en un while', scope.ambito, self.linea, self.columna, datetime.now());
                        raise Exception(_error);
                    break;
                # return
                elif (val.retorno == TipoTransferencia.RETURN):
                    return val;
                # continua
                elif (val.retorno == TipoTransferencia.CONTINUE):
                    continue;
            # ejecutamos otra vez la condición
            valCondicion = self.condicion.ejecutar(console, scope);
            if (valCondicion.tipo != TipoDato.BOOLEAN): 
                # error tiene que se bool 
                _error = _Error(f'Se esperaba un bool como condición pero se obtuvo {valCondicion.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);