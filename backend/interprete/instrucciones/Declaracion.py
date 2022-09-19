from ..expresiones.Expresion import Expresion
from ..extra.Simbolo import Simbolo
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
        self.valor.generador = self.generador;
        val:RetornoExpresion = self.valor.ejecutar(console, scope);
        # asegurandonos de que sea el mismo tipo de dato para crear la variable
        if (self.tipo != None and val.tipo != self.tipo):
            # error, diferentes tipos de datos
            _error = _Error(f'Tipos incompatibles. Se esperaba un tipo de dato {self.tipo.name} y se encontró {val.tipo}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error); 
        posicion:int = scope.crearVariable(self.id, 'Variable', val.tipo, self.mut, None, self.linea, self.columna, console); 
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
            self.generador.setStack(posicion, val.valor);
            self.generador.addGoto(lSalida);
            self.generador.addEtq(val.trueEtq);
            self.generador.setStack(posicion, val.valor);
            self.generador.addEtq(lSalida);
        else:
            '''
            STACK[pos] = val.valor
            '''
            self.generador.setStack(posicion, val.valor);
    
    def valorDefault(_tipo:TipoDato):
        if (_tipo == TipoDato.INT64):
            return RetornoExpresion(0, TipoDato.INT64, None);
        elif (_tipo == TipoDato.FLOAT64):
            return RetornoExpresion(0.0, TipoDato.FLOAT64, None);
        elif (_tipo == TipoDato.BOOLEAN):
            return RetornoExpresion(False, TipoDato.BOOLEAN, None);
        elif (_tipo == TipoDato.CHAR):
            return RetornoExpresion('\0', TipoDato.CHAR, None);
        elif (_tipo == TipoDato.STRING):
            return RetornoExpresion('', TipoDato.STRING, None);
        elif (_tipo == TipoDato.STR):
            return RetornoExpresion('', TipoDato.STR, None);

class Asignacion(Instruccion):
    def __init__(self, id:str, expresion, linea: int, columna: int):
        super().__init__(linea, columna)
        self.id = id;
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        if (isinstance(self.expresion, RetornoExpresion) or isinstance(self.expresion, Simbolo)):
            val = self.expresion;
        else:
            val = self.expresion.ejecutar(console, scope);
        scope.setValor(self.id, val, self.linea, self.columna);