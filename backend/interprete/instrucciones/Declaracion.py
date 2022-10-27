from ..expresiones.Literal import Literal
from ..expresiones.Expresion import Expresion
from ..extra.Tipos import TipoDato
from .Instruccion import Instruccion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from ..extra.Retorno import RetornoExpresion
from datetime import datetime

class Declaracion(Instruccion):
    def __init__(self, mut:bool, id: str, tipo: TipoDato, valor: Expresion, linea: int, columna: int):
        super().__init__(linea, columna)
        self.mut = mut; 
        self.id = id;
        self.tipo = tipo;
        self.valor = valor;
        self.tipoSimbolo = 'Variable';
        self.regActual:int = None;

    def ejecutar(self, console: Console, scope: Scope):
        val:RetornoExpresion;
        if (self.valor == None):
            self.valor = self.valorDefault(self.tipo);
        elif (isinstance(self.valor, RetornoExpresion)):
            val = self.valor;
        else:
            self.valor.generador = self.generador;
            val = self.valor.ejecutar(console, scope);
        # asegurandonos de que sea el mismo tipo de dato para crear la variable
        if (self.tipo != None and val.tipo != self.tipo):
            # error, diferentes tipos de datos
            _error = _Error(f'Tipos incompatibles. Se esperaba un tipo de dato {self.tipo.name} y se encontró {val.tipo}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        posicion:int = scope.crearVariable(val.valor, self.id, self.tipoSimbolo, val.tipo, self.mut, val.atrArr, self.linea, self.columna, console, val.esRef);
        posicion = posicion + self.regActual if (self.regActual != None) else posicion;
        temp:str= self.generador.newTemp();
        self.generador.addOperacion(temp, 'SP', posicion, '+');
        if (val.tipo == TipoDato.BOOLEAN):
            '''
            temp = SP + pos;
            val.EV:
                STACK[temp] = 1;
                goto Salida;
            val.EF:
                STACK[temp] = 0;
            Lsalida:
            '''
            lSalida = self.generador.newEtq();
            self.generador.addEtq(val.trueEtq);
            self.generador.setStack(temp, '1');
            self.generador.addGoto(lSalida);
            self.generador.addEtq(val.falseEtq);
            self.generador.setStack(temp, '0');
            self.generador.addEtq(lSalida);
        else:
            '''
            temp = SP + pos;
            STACK[temp] = val.valor
            '''
            self.generador.setStack(temp, val.valor);

    def valorDefault(self, _tipo:TipoDato):
        if (_tipo == TipoDato.INT64):
            return Literal('0', TipoDato.INT64, self.linea, self.columna);
        elif (_tipo == TipoDato.FLOAT64):
            return Literal('0.0', TipoDato.FLOAT64, self.linea, self.columna);
        elif (_tipo == TipoDato.BOOLEAN):
            return Literal('0', TipoDato.BOOLEAN, self.linea, self.columna);
        elif (_tipo == TipoDato.CHAR):
            return Literal('a', TipoDato.CHAR, self.linea, self.columna);
        elif (_tipo == TipoDato.STRING):
            return Literal('a', TipoDato.STRING, self.linea, self.columna);
        elif (_tipo == TipoDato.STR):
            return Literal('a', TipoDato.STR, self.linea, self.columna);

class Asignacion(Instruccion):
    def __init__(self, id:str, expresion:Expresion, linea: int, columna: int):
        super().__init__(linea, columna)
        self.id = id;
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        val:RetornoExpresion;
        self.expresion.generador = self.generador;
        val = self.expresion.ejecutar(console, scope);
        posicion:int = scope.setValor(self.id, val, self.linea, self.columna);
        temp:str= self.generador.newTemp();
        self.generador.addOperacion(temp, 'SP', posicion, '+');
        if (val.tipo == TipoDato.BOOLEAN):
            '''
            temp = SP + pos;
            val.EV:
                STACK[temp] = 1;
                goto Salida;
            val.EF:
                STACK[temp] = 0;
            Lsalida:
            '''
            lSalida = self.generador.newEtq();
            self.generador.addEtq(val.trueEtq);
            self.generador.setStack(temp, '1');
            self.generador.addGoto(lSalida);
            self.generador.addEtq(val.falseEtq);
            self.generador.setStack(temp, '0');
            self.generador.addEtq(lSalida);
        else:
            '''
            temp = SP + pos;
            STACK[temp] = val.valor;
            '''
            self.generador.setStack(temp, val.valor);