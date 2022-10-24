from .Declaracion import Declaracion
from ..extra.Tipos import TipoDato
from ..extra.Simbolo import AtributosArreglo
from ..extra.Retorno import RetornoExpresion
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
        self.retorno:RetornoExpresion = None;

    def ejecutar(self, console: Console, scope: Scope):
        if (self.id != 'main'):
            '''
            void self.id() {
                <código de parametros>
                <código de valBloque>
                return;
            }
            '''
            self.newScope = Scope(scope, f'Función {self.id}');
            self.generador.newFuncion(self.id);
            for param in self.parametros:
                if (isinstance(param, Declaracion)):
                    self.newScope.crearVariable(None, param.id, 'Parametro por valor', param.tipo, True, None, self.linea, self.columna, console);
                else:
                    self.newScope.crearVariable(None, param.id, 'Parametro por referencia', param.dimension.tipo, True, param.atrArr, self.linea, self.columna, console);
            if (self.retorno_fn != None):
                tipoRetorno:TipoDato;
                if (isinstance(self.retorno_fn, Dimension)):
                    tipoRetorno = self.retorno_fn.tipo;
                else:
                    tipoRetorno = self.retorno_fn;
                self.newScope.crearVariable(None, 'retorno', 'valor de retorno', tipoRetorno, True, None, self.linea, self.columna, console);
            
            self.bloque.generador = self.generador;
            self.retorno = self.bloque.ejecutar(console, self.newScope, self.newScope.ambito);
            self.generador.cerrarFuncion();
        scope.guardarFuncion(self.id, self, self.linea, self.columna);

    def tipoRetorno(self):
        if (self.retorno_fn == None):
            return None;
        elif (isinstance(self.retorno_fn, Dimension)):
            retorno = RetornoExpresion(self.generador.newTemp(), self.retorno_fn.tipo, True);
            retorno.atrArr = AtributosArreglo(self.retorno_fn.esVector, self.retorno_fn.with_capacity);
            return retorno;
        else:
            retorno = RetornoExpresion(self.generador.newTemp(), self.retorno_fn, True);
            return retorno;