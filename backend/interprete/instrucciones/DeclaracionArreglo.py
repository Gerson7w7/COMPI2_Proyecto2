from ..extra.Simbolo import AtributosArreglo
from ..extra.Retorno import RetornoExpresion
from .Instruccion import Instruccion
from ..expresiones.Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Tipos import TipoDato
from datetime import datetime

class Dimension:
    def __init__(self, tipo:str, dimensiones:list, esVector:bool):
        self.tipo = tipo;
        self.dimensiones = dimensiones;
        self.esVector = esVector;

class WithCapacity:
    def __init__(self, esVector:bool, capacidad:int):
        self.esVector = esVector;
        self.capacidad = capacidad;

class DeclaracionArreglo(Instruccion):
    def __init__(self, mut:bool, id:str, dimension:Dimension, valor:Expresion, esVector:bool, with_capacity:int, linea:int, columna:int):
        super().__init__(linea, columna);
        self.mut = mut;
        self.id = id;
        self.dimension = dimension;
        self.valor = valor;
        self.esVector = esVector;
        self.with_capacity = with_capacity;

    def ejecutar(self, console: Console, scope):
        '''
        <código de arreglo>
        STACK[pos] = valor.valor; 
        '''
        atrArr = AtributosArreglo(False, None);
        for dim in self.dimension.dimensiones:
            atrArr.dimensiones.append(dim);
        atrArr.dimensiones.reverse();
        self.generador.addComentario('DECLARACION DE ARREGLO');
        self.valor.generador = self.generador;
        valor:RetornoExpresion = self.valor.ejecutar(console, scope);
        pos:int = scope.crearVariable(valor.valor, self.id, 'Arreglo', valor.tipo, self.mut, atrArr, self.linea, self.columna, console);
        self.generador.setStack(pos, valor.valor);

class AsignacionArreglo(Instruccion):
    def __init__(self, id:str, indices:list, expresion, linea: int, columna: int): 
        super().__init__(linea, columna);
        self.id = id;
        self.indices = indices;
        self.expresion = expresion if(isinstance(expresion, Expresion) or isinstance(expresion, Dimension)) else list(expresion);

    def ejecutar(self, console: Console, scope):
        # obtenemos el valor de la expresion
        if (isinstance(self.expresion, Expresion)):
            self.expresion.generador = self.generador;
            val = self.expresion.ejecutar(console, scope);
        else:
            #arr = Arreglo(None, None, None, [], None, None, self.linea, self.columna);
            pass;
            #listaResultante:list = arr.nuevaDimension(self.expresion, console, scope, arr.tipo, [], -1);
        # indice
        indice:list = [];
        for i in self.indices:
            i.generador = self.generador;
            index = i.ejecutar(console, scope);
            if (index.tipo != TipoDato.INT64):
                # ERROR. No sepuede acceder a la posición index.valor
                _error = _Error(f'No sepuede acceder a la posición {index.valor}', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
            indice.append(index.valor);
        if (isinstance(self.expresion, Expresion)):
            scope.setValorArreglo(self.id, val.valor, val.tipo, indice, self.linea, self.columna);
        else:
            pass;
            #scope.setValorArreglo(self.id, listaResultante, arr.tipo, indice, self.linea, self.columna);