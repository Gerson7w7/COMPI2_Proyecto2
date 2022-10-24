from ..instrucciones.Funcion import Funcion
from ..extra.Simbolo import Simbolo
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from ..extra.Retorno import RetornoExpresion
from .Expresion import Expresion
from datetime import datetime

class LlamadaFuncion(Expresion):
    def __init__(self, id:str, argumentos:list, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.argumentos = argumentos;
    
    def ejecutar(self, console: Console, scope: Scope):
        '''
        tempFuturoPos = SP + scope.size; // tamaño del reg. actual
        '''
        tempFuturoPos:str = self.generador.newTemp();
        self.generador.addComentario('LLAMADA A FUNCIÓN');
        self.generador.addOperacion(tempFuturoPos, 'SP', scope.size, '+'); # posiblemente lo quite :D
        # obtenemos la función 
        funcion:Funcion = scope.getFuncion(self.id, self.linea, self.columna);
        newScope:Scope = funcion.newScope;
        # verificando si la cantidad de argumentos son == a la cantidad de parámetros de la función
        if (len(self.argumentos) != len(funcion.parametros)):
            # ERROR. Se esperaban x parametros y se encontraron x argumentos
            _error = _Error(f'Se esperaban {len(funcion.parametros)} parametros y se encontraron {len(self.argumentos)} argumentos', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        for i in range(len(self.argumentos)):
            '''
            <código de declaración>
            '''
            if (isinstance(self.argumentos[i], Puntero)):
                # el pasamos el valor del argumento al parámetro
                funcion.parametros[i].valor = self.argumentos[i].expresion;
                funcion.parametros[i].generador = self.generador;
                funcion.parametros[i].ejecutar(console, newScope);
            else:
                funcion.parametros[i].valor = self.argumentos[i];
                funcion.parametros[i].generador = self.generador;
                self.argumentos[i].ejecutar(console, newScope);
        # verificando el retorno de la función
        retorno:RetornoExpresion = funcion.tipoRetorno(scope);
        return retorno;

class Puntero:
    def __init__(self, expresion):
        self.expresion = expresion;