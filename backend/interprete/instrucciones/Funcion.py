from ..extra.Simbolo import AtributosArreglo
from .Declaracion import Declaracion
from ..extra.Tipos import TipoDato
from .DeclaracionArreglo import Dimension
from .Instruccion import Instruccion
from ..extra.Scope import Scope
from ..extra.Console import Console

class Funcion(Instruccion):
    def __init__(self, id:str, parametros:list, retorno_fn:TipoDato or Dimension, bloque:Instruccion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.parametros = parametros;
        self.retorno_fn = retorno_fn;
        self.bloque = bloque;
        self.newScope:Scope = None;

    def ejecutar(self, console: Console, scope: Scope):
        '''
        void self.id() {
            <código de parametros>
            <código de valBloque>
            return;
        }
        '''
        self.generador.newFuncion(self.id);
        self.bloque.generador = self.generador;
        self.bloque.ejecutar(console, self.newScope, self.newScope.ambito);
        self.generador.cerrarFuncion();

    def guardarFn(self, console:Console, scope:Scope):
        self.newScope = Scope(scope.getGlobal(), f'Funcion {self.id}');
        if (self.parametros != None):
            for param in self.parametros:
                tipoDato:TipoDato;
                tipoSimbolo:str;
                atrArr = None;
                esRef = False;
                if (isinstance(param, Declaracion)):
                    tipoDato = param.tipo;
                    tipoSimbolo = 'Paso por valor';
                else:
                    tipoDato = param.dimension.tipo;
                    tipoSimbolo = 'Paso por referencia';
                    esRef = True;
                    atrArr = AtributosArreglo(param.dimension.esVector, 1);
                self.newScope.crearVariable(None, param.id, tipoSimbolo, tipoDato, True, atrArr, self.linea, self.columna, console, esRef);
                
        if (self.retorno_fn != None):
            tipoRetorno:TipoDato;
            if (isinstance(self.retorno_fn, Dimension)):
                tipoRetorno = self.retorno_fn.tipo;
            else:
                tipoRetorno = self.retorno_fn;
            self.newScope.crearVariable(None, 'retorno', 'Retorno', tipoRetorno, True, None, self.linea, self.columna, console);
        scope.guardarFuncion(self.id, self, self.linea, self.columna);