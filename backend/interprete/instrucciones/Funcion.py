from ..extra.Tipos import TipoDato
from .Arreglo import Arreglo, Dimension
from .Instruccion import Instruccion
from ..extra.Scope import Scope
from ..extra.Console import Console, _Error
from datetime import datetime

class Funcion(Instruccion):
    def __init__(self, id:str, parametros:list, retorno_fn, bloque:Instruccion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.parametros = parametros;
        self.retorno_fn = retorno_fn;
        self.bloque = bloque;

    def ejecutar(self, console: Console, scope: Scope):
        if (isinstance(self.retorno_fn, Dimension)):
            scope.guardarFuncion(self.id, self, self.retorno_fn.tipo, self.linea, self.columna);
        else:
            scope.guardarFuncion(self.id, self, self.retorno_fn, self.linea, self.columna);

    def tipoArgumentos(self, argTipo, i:int, console:Console, scope:Scope):
        if (isinstance(self.parametros[i], Arreglo)):
            if (argTipo != self.devolverTipo(self.parametros[i].dimension.tipo)):
                # ERROR. Tipos incompatibles. se esperaba un str(paramTipo) y se encontró un str(argTipo) 
                _error = _Error(f'Argumento incompatible. se esperaba un {self.devolverTipo(self.parametros[i].dimension.tipo).name} y se encontró un {argTipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
        else:
            if (argTipo != self.devolverTipo(self.parametros[i].tipo)):
                # ERROR. Tipos incompatibles. se esperaba un str(paramTipo) y se encontró un str(argTipo) 
                _error = _Error(f'Argumento incompatible. se esperaba un {self.devolverTipo(self.parametros[i].tipo).name} y se encontró un {argTipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);

    def tipoRetorno(self, returnTipo, scope:Scope):
        if (self.retorno_fn == None):
            if (returnTipo != None):
                # ERROR. No se puede retornar una expresión en un método.
                _error = _Error(f'No se puede retornar una expresión en un método', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
        elif (isinstance(self.retorno_fn, Dimension)):
            tipo = self.devolverTipo(self.retorno_fn.tipo);
            if (returnTipo == None):
                # ERROR. Se esperaba que se retornara str(tipo) y no se devolvió nada.
                _error = _Error(f'Se esperaba que se retornara {tipo} y no se devolvió nada', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
            if (returnTipo != tipo):
                # ERROR. Tipos incompatibles. se esperaba un str(paramTipo) y se encontró un str(argTipo) 
                _error = _Error(f'Retorno incompatible. Se esperaba un {tipo} y se encontró un {returnTipo}', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
        else:
            tipo = self.devolverTipo(self.retorno_fn);
            if (returnTipo == None):
                # ERROR. Se esperaba que se retornara str(tipo) y no se devolvió nada.
                _error = _Error(f'Se esperaba que se retornara {tipo} y no se devolvió nada', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
            if (returnTipo != tipo):
                # ERROR. Tipos incompatibles. se esperaba un str(paramTipo) y se encontró un str(argTipo) 
                _error = _Error(f'Retorno incompatible. se esperaba un {tipo} y se encontró un {returnTipo}', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);

    def devolverTipo(self, tipo:str):
        if (tipo == 'i64' or tipo == 'usize'):
            return TipoDato.INT64;
        elif (tipo == 'f64'):
            return TipoDato.FLOAT64;
        elif (tipo == 'char'):
            return TipoDato.CHAR;
        elif (tipo == 'str'):
            return TipoDato.STR;
        elif (tipo == 'String'):
            return TipoDato.STRING;
        elif (tipo == 'bool'):
            return TipoDato.BOOLEAN;
        else:
            return tipo;