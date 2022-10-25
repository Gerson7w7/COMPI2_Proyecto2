from ..extra.Tipos import TipoDato
from ..instrucciones.DeclaracionArreglo import Dimension
from ..extra.Retorno import RetornoExpresion
from ..instrucciones.Declaracion import Asignacion, Declaracion
from ..instrucciones.Funcion import Funcion
from ..extra.Simbolo import Simbolo
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from .Expresion import Expresion
from datetime import datetime

class LlamadaFuncion(Expresion):
    def __init__(self, id:str, argumentos:list, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.argumentos = argumentos;
    
    def ejecutar(self, console: Console, scope: Scope):
        self.generador.addComentario('LLAMADA A FUNCIÓN');
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
            asignacion:Asignacion;
            if (isinstance(self.argumentos[i], Puntero)):
                # el pasamos el valor del argumento al parámetro
                acceso = self.argumentos[i].expresion;
                acceso.esRef = True;
                acceso.generador = self.generador;
                asignacion = Asignacion(funcion.parametros[i].id, acceso.ejecutar(console, scope), self.linea, self.columna);
            else:
                self.argumentos[i].generador = self.generador;
                asignacion = Asignacion(funcion.parametros[i].id, self.argumentos[i].ejecutar(console, scope), self.linea, self.columna);
            asignacion.generador = self.generador;
            asignacion.ejecutar(console, newScope);
        '''
        self.id();
        '''
        self.generador.callFunc(self.id);
        # verificando el retorno de la función
        retorno:RetornoExpresion = None;
        if (funcion.retorno_fn != None):
            '''
            temp = STACK[valPos.posicion];
            '''
            valRetorno:Simbolo = newScope.getValor('retorno', self.linea, self.columna);
            temp:str = self.generador.newTemp();
            self.generador.getStack(temp, valRetorno.posicion);
            retorno = RetornoExpresion(temp, valRetorno.tipo, True);
        scope.setFuncionScope(funcion.id, newScope);
        return retorno;

class Puntero:
    def __init__(self, expresion):
        self.expresion = expresion;