# clase para manejar los entornos, ambitos, env o scopes
from .TablaSimbolo import TablaSimbolo
from .Tipos import TipoDato 
from .Simbolo import Simbolo, AtributosArreglo
from .Console import _Error, Console
from datetime import datetime

class Scope:
    def __init__(self, padre, ambito:str):
        self.padre = padre;
        self.ambito = ambito;
        self.variables = {};
        self.funciones = {};
        self.structs = {};
        self.size:int = 0;
        # pasamos donde empieza el nuevo ambito
        if(self.padre != None): self.size = self.padre.size;
    
    # función para crear una variable
    def crearVariable(self, valor:str, id: str, tipoSimbolo:str, tipoDato: TipoDato, mut:bool, atrArr:AtributosArreglo, linea: int, columna: int, console:Console) -> int:
        scope: Scope = self;
        ambito:str = scope.ambito;
        while(scope != None):
            # verificamos que no se haya declarado antes la misma variable
            if(scope.variables.get(id)):
                # ERROR: la variable ya ha sido declarada
                _error = _Error(f'La variable {id} ya ha sido declarada', ambito, linea, columna, datetime.now())
                raise Exception(_error);
            scope = scope.padre;
        # procedemos a crear la variable
        posicion:int = self.size;
        self.size += 1;
        self.variables[id] = Simbolo(valor, id, tipoDato, mut, atrArr, posicion);
        # lo guardamos en la tabla de simbolos para nuestro reporte de símbolos
        _tipoDato = str(tipoDato.name) if (isinstance(tipoDato, TipoDato)) else tipoDato;
        console.appendSimbolo(TablaSimbolo(id, tipoSimbolo, _tipoDato, ambito, linea, columna));
        return posicion;

    # función para obtener el valor de una variable
    def getValor(self, id:str, linea:int, columna:int) -> Simbolo:
        scope: Scope = self;
        ambito:str = scope.ambito;
        while(scope != None):
            if (scope.variables.get(id) != None):
                return scope.variables.get(id);
            scope = scope.padre;
        # error: no se ha encontrado la variable
        _error = _Error(f'No se ha encontrado la variable {id}', ambito, linea, columna, datetime.now())
        raise Exception(_error);

    # función para obtener el scopeo más general, el global
    def getGlobal(self):
        scope:Scope = self;
        while(scope.padre != None):
            scope = scope.padre;
        return scope;

    def setValor(self, id:str, valor, linea:int, columna:int) -> int:
        scope: Scope = self;
        ambito:str = scope.ambito;
        while(scope != None):
            if (scope.variables.get(id) != None):
                val:Simbolo = scope.variables.get(id);
                if (val.tipo == None or val.tipo == valor.tipo):
                    if (val.mut):
                        scope.variables.update({id : Simbolo(valor.valor, id, valor.tipo, True, val.atrArr, val.posicion)});
                        return val.posicion;
                    else:
                        # error, variable no mutable
                        _error = _Error(f'La variable {id} no es mutable', ambito, linea, columna, datetime.now())
                        raise Exception(_error);
                else:
                    # error tipos incopatibles
                    _error = _Error(f'Una variable de tipo {val.tipo.name} no puede almacenar una expresión de tipo {valor.tipo.name}', ambito, linea, columna, datetime.now())
                    raise Exception(_error);
            scope = scope.padre;

    def guardarFuncion(self, id:str, fn, tipo_retorno:TipoDato, linea:int, columna:int):
        scope: Scope = self;
        ambito:str = scope.ambito;
        while(scope != None):
            # verificamos que no se haya declarado antes la misma funcion
            if(scope.funciones.get(id)):
                # ERROR: la funcion ya ha sido declarada
                _error = _Error(f'La función {id} ya ha sido declarado', ambito, linea, columna, datetime.now())
                raise Exception(_error);
            scope = scope.padre;
        # procedemos a guardar la funcion
        self.funciones[id] = fn;

    def getFuncion(self, id:str, linea:int, columna:int):
        scope: Scope = self;
        ambito:str = scope.ambito;
        while(scope != None):
            if (scope.funciones.get(id) != None):
                return scope.funciones.get(id);
            scope = scope.padre;
        # error: no se ha encontrado la variable
        _error = _Error(f'No se ha encontrado la función {id}', ambito, linea, columna, datetime.now())
        raise Exception(_error);

    def guardarStruct(self, id:str, struct, linea:int, columna:int):
        scope: Scope = self;
        ambito:str = scope.ambito;
        while(scope != None):
            # verificamos que no se haya declarado antes la misma funcion
            if(scope.structs.get(id)):
                # ERROR: El struct ya ha sido declarada
                _error = _Error(f'El struct {id} ya ha sido declarado', ambito, linea, columna, datetime.now())
                raise Exception(_error);
            scope = scope.padre;
        # procedemos a guardar la funcion
        self.structs[id] = struct;

    def getStruct(self, id:str, linea:int, columna:int):
        scope: Scope = self;
        ambito:str = scope.ambito;
        while(scope != None):
            if (scope.structs.get(id) != None):
                return scope.structs.get(id);
            scope = scope.padre;
        # error: no se ha encontrado la variable
        _error = _Error(f'No se ha encontrado el struct {id}', ambito, linea, columna, datetime.now())
        raise Exception(_error);