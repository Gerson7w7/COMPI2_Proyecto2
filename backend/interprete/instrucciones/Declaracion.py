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

    def ejecutar(self, console: Console, scope: Scope):
        if (self.valor == None):
            self.valor = self.valorDefault(self.tipo);
        self.valor.generador = self.generador;
        val:RetornoExpresion = self.valor.ejecutar(console, scope);
        # asegurandonos de que sea el mismo tipo de dato para crear la variable
        if (self.tipo != None and val.tipo != self.tipo):
            # error, diferentes tipos de datos
            _error = _Error(f'Tipos incompatibles. Se esperaba un tipo de dato {self.tipo.name} y se encontró {val.tipo}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        posicion:int = scope.crearVariable(val.valor, self.id, 'Variable', val.tipo, self.mut, val.atrArr, self.linea, self.columna, console);
        if (val.tipo == TipoDato.BOOLEAN):
            '''
            val.EV:
                STACK[pos] = 1;
                goto Salida;
            val.EF:
                STACK[pos] = 0;
            Lsalida:
            '''
            lSalida = self.generador.newEtq();
            self.generador.addEtq(val.trueEtq);
            self.generador.setStack(posicion, '1');
            self.generador.addGoto(lSalida);
            self.generador.addEtq(val.falseEtq);
            self.generador.setStack(posicion, '0');
            self.generador.addEtq(lSalida);
        else:
            '''
            STACK[pos] = val.valor
            '''
            self.generador.setStack(posicion, val.valor);

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
        if (isinstance(self.expresion, RetornoExpresion)):
            val = self.expresion;
        else:
            self.expresion.generador = self.generador;
            val = self.expresion.ejecutar(console, scope);
        posicion:int = scope.setValor(self.id, val, self.linea, self.columna);
        if (val.tipo == TipoDato.BOOLEAN):
            '''
            val.EV:
                STACK[pos] = 1;
                goto Salida;
            val.EF:
                STACK[pos] = 0;
            Lsalida:
            '''
            lSalida = self.generador.newEtq();
            self.generador.addEtq(val.trueEtq);
            self.generador.setStack(posicion, '1');
            self.generador.addGoto(lSalida);
            self.generador.addEtq(val.falseEtq);
            self.generador.setStack(posicion, '0');
            self.generador.addEtq(lSalida);
        else:
            '''
            STACK[pos] = val.valor
            '''
            self.generador.setStack(posicion, val.valor);