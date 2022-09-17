from .Funcion import Funcion
from .Instruccion import Instruccion
from ..extra.Scope import Scope
from ..extra.Console import Console, _Error
from .LlamadaFuncion import Puntero, Referencia
from ..extra.Retorno import RetornoExpresion
from datetime import datetime

class Mod(Instruccion):
    def __init__(self, id:str, bloqueMod:Instruccion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.bloqueMod = bloqueMod;

    def ejecutar(self, console: Console, scope: Scope):
        scope.guardarMod(self.id, self, self.linea, self.columna);

class InstanciaMod(Instruccion):
    def __init__(self, accesos:list, linea: int, columna: int):
        super().__init__(linea, columna);
        self.accesos = accesos;

    def ejecutar(self, console: Console, scope: Scope):
        print("all accesos :: "+str(self.accesos))
        print("1 :: "+str(self.accesos[0].id))
        print("2 :: "+str(self.accesos[1].id))
        print("3 :: "+str(self.accesos[2].id))
        for i in range(len(self.accesos)):
            if (i + 1 != len(self.accesos)):
                newScope: Scope = Scope(scope.getGlobal(), 'Mod') if (i == 0) else Scope(newScope, 'Mod');
                # buscamos el mod
                mod: Mod = newScope.getMod(self.accesos[i].id, self.linea, self.columna);
                print("MDOOD:: " + str(mod.bloqueMod))
                if (mod != None): mod.bloqueMod.ejecutar(console, newScope);
            else:
                # si la última expresion, quiere decir que es la llamada a lafunción, solo ejecutamos
                # obtenemos la función 
                funcion:Funcion = newScope.getFuncion(self.id, self.linea, self.columna);
                # verificando si la cantidad de argumentos son == a la cantidad de parámetros de la función
                if (len(self.argumentos) != len(funcion.parametros)):
                    # ERROR. Se esperaban x parametros y se encontraron x argumentos
                    _error = _Error(f'Se esperaban {len(funcion.parametros)} parametros y se encontraron {len(self.argumentos)} argumentos', scope.ambito, self.linea, self.columna, datetime.now());
                    raise Exception(_error);
                newScope = Scope(newScope, 'Funcion');
                for i in range(len(self.argumentos)):
                    if (isinstance(self.argumentos[i], Puntero)):
                        val = self.argumentos[i].expresion.ejecutar(console, scope);
                    else:
                        val = self.argumentos[i].ejecutar(console, scope);
                    # verificando el tipo correcto del argumento
                    funcion.tipoArgumentos(val.tipo, i, console, scope);
                    # obtenemos el id del parametro correspondiente
                    idParam = funcion.parametros[i].id;
                    if (isinstance(self.argumentos[i], Puntero)):
                        idReferencia = self.argumentos[i].expresion.id;
                        referencia = Referencia(scope, idReferencia, val);
                        newScope.crearVariable(idParam, val.valor, 'Dirección de memoria', val.tipo, True, val.esVector, val.with_capacity, referencia, self.linea, self.columna, console);
                    else:
                        if (isinstance(val, RetornoExpresion)):
                            newScope.crearVariable(idParam, val.valor, 'Variable', val.tipo, True, None, None, None, self.linea, self.columna, console);
                        else:
                            newScope.crearVariable(idParam, val.valor, 'Variable', val.tipo, True, None, None, val.referencia, self.linea, self.columna, console);
                # ejecutando las instrucciones de la función 
                valBloque = funcion.bloque.ejecutar(console, newScope, 'Funcion');
                # verificando el retorno de la función
                if (valBloque != None):
                    funcion.tipoRetorno(valBloque.tipo, scope);
                else:
                    funcion.tipoRetorno(None, scope);
                return valBloque;
