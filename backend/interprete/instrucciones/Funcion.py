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
        self.yaActivo:bool = False;
        self.sePuedeEjecutar:bool = False;

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

    def guardarFn(self, scope):
        scope.guardarFuncion(self.id, self, self.linea, self.columna);