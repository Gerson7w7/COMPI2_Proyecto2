from ..extra.Retorno import RetornoExpresion
from interprete.extra.Tipos import TipoDato
from .Instruccion import Instruccion
from ..expresiones.Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class IfElse(Instruccion):
    def __init__(self, condicion: Expresion, bloque:Instruccion, bloqueElse:Instruccion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.condicion = condicion;
        self.bloque = bloque;
        self.bloqueElse = bloqueElse;
        self.Lsalida = '';
        self.temp = '';

    def ejecutar(self, console: Console, scope: Scope):
        # obtenemos el valor de la condición
        self.generador.addComentario('IF-ELSE');
        self.condicion.generador = self.generador;
        valCondicion:RetornoExpresion = self.condicion.ejecutar(console, scope);
        # sino es un boolean la condición, entonces es un error
        if (valCondicion.tipo != TipoDato.BOOLEAN):
            # error condicion debe de ser booleano
            _error = _Error(f'La condición debería ser de tipo bool, pero se obtuvo {valCondicion.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # verificamos si es true o false
        '''
        valCondicion.trueEtq:
            <bloque de código>
            goto Lsalida;
        valCondicion.falseEtq:
            <bloque de código>
        goto Lsalida:
        '''
        generarSalida:bool = False;
        esIfElse:bool = False;
        esRetorno:bool = False;
        if (self.Lsalida == ''):
            self.Lsalida = self.generador.newEtq();
            # este temp nos ayudará a regresar la expresión que se quiera
            self.temp = self.generador.newTemp();
            generarSalida = True;
        if (self.bloqueElse != None and isinstance(self.bloqueElse, IfElse)):
            self.bloqueElse.Lsalida = self.Lsalida;
            self.bloqueElse.temp = self.temp;
            esIfElse = True;
        self.generador.addEtq(valCondicion.trueEtq);
        self.bloque.generador = self.generador;
        valIf:RetornoExpresion = self.bloque.ejecutar(console, scope, 'If');
        if (valIf != None):
            esRetorno = True;
            esBreak = self.generador.cambiarCodigo(f'{self.temp} = {valIf.valor};');
            if (not esBreak):
                self.generador.addOperacion(self.temp, valIf.valor, '', '');
        self.generador.addGoto(self.Lsalida);
        self.generador.addEtq(valCondicion.falseEtq);
        valElse:RetornoExpresion = None;
        if (self.bloqueElse != None):
            self.bloqueElse.generador = self.generador;
            if (esIfElse):
                valElse = self.bloqueElse.ejecutar(console, scope);
                if (valElse != None):
                    esRetorno = True;
                    esBreak = self.generador.cambiarCodigo(f'{self.temp} = {valElse.valor};');
                    if (not esBreak):
                        self.temp = valElse.valor;
            else:
                valElse = self.bloqueElse.ejecutar(console, scope, 'Else');
                if (valElse != None):
                    esRetorno = True;
                    esBreak = self.generador.cambiarCodigo(f'{self.temp} = {valElse.valor};');
                    if (not esBreak):
                        self.generador.addOperacion(self.temp, valElse.valor, '', '');
        if (generarSalida):
            self.generador.addEtq(self.Lsalida);
        if (esRetorno):
            tipo = valIf.tipo if(valIf != None) else valElse.tipo;
            return RetornoExpresion(self.temp, tipo, True);
