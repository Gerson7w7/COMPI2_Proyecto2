from ..extra.Simbolo import Simbolo
from ..instrucciones.Instruccion import Instruccion
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

class Arreglo(Instruccion):
    def __init__(self, mut:bool, id:str, dimension:Dimension, valor, esVector:bool, with_capacity:int, linea:int, columna:int):
        super().__init__(linea, columna);
        self.mut = mut;
        self.id = id;
        self.dimension = dimension;
        self.valor = valor if(isinstance(valor, list) or isinstance(valor, Dimension)) else list(valor);
        self.esVector = esVector;
        self.with_capacity = with_capacity;
        self.tipo = None;

    def ejecutar(self, console: Console, scope):
        # primero miramos de que tipo de dato será el arreglo
        # y las dimensiones que tendrá}
        if (isinstance(self.valor, Simbolo)):
            scope.crearVariable(self.id, self.valor.valor, 'Arreglo', self.valor.tipo, self.valor.mut, self.valor.esVector, self.valor.with_capacity, None, self.linea, self.columna, console);
        else:
            _tipo: TipoDato = None;
            _dimensiones:list = [];
            if (self.dimension != None):
                if (self.dimension.tipo == 'i64' or self.dimension.tipo == 'usize'):
                    _tipo = TipoDato.INT64
                elif (self.dimension.tipo == 'f64'):
                    _tipo = TipoDato.FLOAT64
                elif (self.dimension.tipo == 'bool'):
                    _tipo = TipoDato.BOOLEAN
                elif (self.dimension.tipo == 'char'):
                    _tipo = TipoDato.CHAR
                elif (self.dimension.tipo == 'String'):
                    _tipo = TipoDato.STRING
                elif (self.dimension.tipo == 'str'):
                    _tipo = TipoDato.STR
                else:
                    _tipo = self.dimension.tipo;

                for dim in self.dimension.dimensiones:
                    _dimensiones.append(dim);
            # with_capacity
            val_with_capacity = None;
            if (self.with_capacity != None):
                val_with_capacity = self.with_capacity.ejecutar(console, scope);
                if (val_with_capacity.tipo != TipoDato.INT64):
                    #ERROR. Se esperaba un int
                    _error = _Error(f'Se esperaba un i64 para la capacidad del vector, no un {val_with_capacity.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
                    raise Exception(_error);
                val_with_capacity = val_with_capacity.valor;

            # inicializamos el arreglo resultante que quedará
            listaResultante:list = [];
            # indice del arreglo con las dimensiones
            iAux:int = -1 if (len(_dimensiones) == 0) else len(_dimensiones) - 1;
            listaResultante = self.nuevaDimension(self.valor, console, scope, _tipo, _dimensiones, iAux);
            # esto nos ayudará para saber que tipo de dato es en la asignación
            if (self.tipo == None and self.dimension != None):
                self.tipo = _tipo;
            tipoSimbolo:str = 'Vector' if (self.esVector) else 'Arreglo';
            scope.crearVariable(self.id, listaResultante, tipoSimbolo, self.tipo, self.mut, self.esVector, val_with_capacity, None, self.linea, self.columna, console);

    def nuevaDimension(self, valor, console: Console, scope, _tipo:TipoDato, dimensionesAux:list, iAux:int):
        # verificamos que se trate de una lista, sino es una expresion
        listaAux:list = [];
        # contador para verificar cuantos elementos contiene el arreglo
        cont:int = 0;
        if (isinstance(valor, list) == True):
            # cuando sea una lista
            for v in valor:
                # mientras sea una lista, se hará recursiva la función
                listaAux.append(self.nuevaDimension(v, console, scope, _tipo, dimensionesAux, iAux - 1));
                cont += 1;
            if (iAux >= 0):
                if (dimensionesAux[iAux] == cont):
                    return listaAux;
                # ERROR. se esperaba un arreglo de {dimensionesAux[iAux]} elemenots y se encontró {cont} elementos.
                _error = _Error(f'Se esperaba un arreglo de {dimensionesAux[iAux]} elementos y se encontró {cont} elementos', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
            return listaAux;
        elif (isinstance(valor, Expresion) == True):
            # cuando sea expresion
            val = valor.ejecutar(console, scope);
            # verificamos el tipo si coincide con el arreglo
            self.tipo = val.tipo if (_tipo == None) else _tipo;
            if (val.tipo == self.tipo):
                return val.valor;
            # ERROR. tipos incopatibles
            _error = _Error(f'No se puede almacenar una expresion de tipo {val.tipo.name} en una variable de tipo {self.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        elif (isinstance(valor, Dimension) == True):
            # cuando sea expresion ; ENTERO
            for i in range(valor.dimensiones[0]):
                # aki ejecutaremos n veces la misma expresion para llenar el arreglo
                val = valor.tipo.ejecutar(console, scope);
                self.tipo = val.tipo if (_tipo == None) else _tipo;
                if (val.tipo != self.tipo):
                    # ERROR. tipos incopatibles
                    _error = _Error(f'No se puede almacenar una expresion de tipo {val.tipo.name} en una variable de tipo {self.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
                    raise Exception(_error);
                listaAux.append(val.valor);
                cont += 1;
            if (iAux >= 0):
                if (dimensionesAux[iAux] == cont):
                    return listaAux;
                # ERROR. se esperaba un arreglo de {dimensionesAux[iAux]} elemenots y se encontró {cont} elementos.
                _error = _Error(f'Se esperaba un arreglo de {dimensionesAux[iAux]} elementos y se encontró {cont} elementos', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
            return listaAux;


class AsignacionArreglo(Instruccion):
    def __init__(self, id:str, indices:list, expresion, linea: int, columna: int): 
        super().__init__(linea, columna);
        self.id = id;
        self.indices = indices;
        self.expresion = expresion if(isinstance(expresion, Expresion) or isinstance(expresion, Dimension)) else list(expresion);

    def ejecutar(self, console: Console, scope):
        # obtenemos el valor de la expresion
        if (isinstance(self.expresion, Expresion)):
            val = self.expresion.ejecutar(console, scope);
        else:
            arr = Arreglo(None, None, None, [], None, None, self.linea, self.columna);
            listaResultante:list = arr.nuevaDimension(self.expresion, console, scope, arr.tipo, [], -1);
        # indice
        indice:list = [];
        for i in self.indices:
            index = i.ejecutar(console, scope);
            if (index.tipo != TipoDato.INT64):
                # ERROR. No sepuede acceder a la posición index.valor
                _error = _Error(f'No sepuede acceder a la posición {index.valor}', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
            indice.append(index.valor);
        if (isinstance(self.expresion, Expresion)):
            scope.setValorArreglo(self.id, val.valor, val.tipo, indice, self.linea, self.columna);
        else:
            scope.setValorArreglo(self.id, listaResultante, arr.tipo, indice, self.linea, self.columna);