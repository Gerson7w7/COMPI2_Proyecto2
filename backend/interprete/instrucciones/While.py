from ..extra.Retorno import RetornoExpresion
from ..expresiones.Expresion import Expresion
from ..extra.Tipos import TipoDato, TipoTransferencia
from .Instruccion import Instruccion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class While(Instruccion):
    def __init__(self, condicion:Expresion, bloque: Instruccion, linea: int, columna: int):
        super().__init__(linea, columna)
        self.condicion = condicion;
        self.bloque = bloque;
        self.temp:str = '';

    def ejecutar(self, console: Console, scope: Scope):
        '''
        Linicio:
            <código de condición>
        condicion.trueEtq:
            <código del bloque>
            goto Linicio;
        condicion.falseEtq:
        Lsalida:
        '''
        retorno:RetornoExpresion = None;
        Linicio:str = self.generador.newEtq();
        Lsalida:str = self.generador.newEtq();
        console.continues.append(Linicio);
        console.breaks.append(Lsalida);
        self.generador.addEtq(Linicio);
        # primero ejecutamos la condición
        self.condicion.generador = self.generador;
        valCondicion:RetornoExpresion = self.condicion.ejecutar(console, scope);
        # verificando de que se trate de un boolean
        if (valCondicion.tipo != TipoDato.BOOLEAN):
            # error tiene que se bool
            _error = _Error(f'Se esperaba un bool como condición pero se obtuvo {valCondicion.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        self.generador.addEtq(valCondicion.trueEtq);
        self.bloque.generador = self.generador;
        val:RetornoExpresion = self.bloque.ejecutar(console, scope, 'While');
        if (val != None):
            if (self.temp == ''):
                self.temp = self.generador.newTemp();
            self.generador.addOperacion(self.temp, val.valor, '', '');
            retorno = RetornoExpresion(self.temp, val.tipo, True);
        self.generador.addGoto(Linicio);
        self.generador.addEtq(valCondicion.falseEtq);
        self.generador.addEtq(Lsalida);
        return retorno;