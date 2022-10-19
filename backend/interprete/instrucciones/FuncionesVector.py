from msilib.schema import SelfReg
from ..expresiones.Expresion import Expresion
from ..extra.Tipos import TipoDato
from ..extra.Simbolo import Simbolo
from .Instruccion import Instruccion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from ..extra.Retorno import RetornoExpresion
from datetime import datetime

class Push(Instruccion):
    def __init__(self, id:Expresion, expresion:Expresion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        '''
        <código de valExp>
        <código de vector>
        temp = HP;
        tempRetorno = HP;
        espacioNuevo = 2;
        Lloop:
            tempVal = HEAP[vector.valor];
            if (tempVal == -1) goto Lsalida
            HEAP[temp] = tempVal;
            vector.valor = vector.valor + 1;
            temp = temp + 1;
            espacioNuevo = espacioNuevo + 1;
            goto Lloop;
        Lsalida:
            HP = HP + espacioNuevo;
            HEAP[temp] = val.valor;
            temp = temp + 1;
            HEAP[temp] = -1;
            STACK[pos] = tempRetorno;
        '''
        # ejecutando la expresión
        self.generador.addComentario('PUSH');
        self.expresion.generador = self.generador;
        val:RetornoExpresion = self.expresion.ejecutar(console, scope);
        # obtenemos el vector
        self.id.generador = self.generador;
        vector:RetornoExpresion = self.id.ejecutar(console, scope);
        if (vector.atrArr == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función push', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (vector.tipo == None):
            vector.tipo = val.tipo;
        elif (val.tipo != vector.tipo):
            _error = _Error(f'Tipos incompatibles. No se puede almacenar una expresión {val.tipo.name} en una variable de tipo {vector.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        temp:str = self.generador.newTemp();
        tempRetorno:str = self.generador.newTemp();
        tempVal:str = self.generador.newTemp();
        nuevoEspacio:str = self.generador.newTemp();
        Lloop:str = self.generador.newEtq();
        Lsalida:str = self.generador.newEtq();
        self.generador.addOperacion(temp, 'HP', '', '');
        self.generador.addOperacion(tempRetorno, 'HP', '', '');
        self.generador.addOperacion(nuevoEspacio, '2', '', '');
        self.generador.addEtq(Lloop);
        self.generador.getHeap(tempVal, vector.valor);
        self.generador.addIf(tempVal, '-1', '==', Lsalida);
        self.generador.setHeap(temp, tempVal);
        self.generador.addOperacion(vector.valor, vector.valor, '1', '+');
        self.generador.addOperacion(temp, temp, '1', '+');
        self.generador.addOperacion(nuevoEspacio, nuevoEspacio, '1', '+');
        self.generador.addGoto(Lloop);
        self.generador.addEtq(Lsalida);
        self.generador.addOperacion('HP', 'HP', nuevoEspacio, '+');
        self.generador.setHeap(temp, val.valor);
        self.generador.addOperacion(temp, temp, '1', '+');
        self.generador.setHeap(temp, '-1');
        # ahora revisaremos si se trata de un vector con un tamaño definido
        vector.atrArr.size += 1;
        print(str(vector.atrArr.with_capacity) + "<" + str(vector.atrArr.size))
        if (vector.atrArr.with_capacity < vector.atrArr.size):
            vector.atrArr.with_capacity = vector.atrArr.with_capacity * 2;
            print("sisoi:: " + str(vector.atrArr.with_capacity))
        vector.valor = RetornoExpresion(tempRetorno, vector.tipo, True);
        pos:int = scope.setValor(self.id.id, vector, self.linea, self.columna);
        self.generador.setStack(pos, tempRetorno);

class Insert(Instruccion):
    def __init__(self, id:Expresion, exp1:Expresion, exp2:Expresion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.exp1 = exp1;
        self.exp2 = exp2;
    
    def ejecutar(self, console: Console, scope: Scope):
        '''
        <código de valPos>
        <código de valExp>
        <código de vector>
        tempPos = vector.valor + valPos.valor;
        HEAP[tempPos] = valExp.valor;
        '''
        # ejecutando las expresiones
        self.generador.addComentario('INSERT');
        self.exp1.generador = self.generador;
        valPos:RetornoExpresion = self.exp1.ejecutar(console, scope);
        self.exp2.generador = self.generador;
        valExp:RetornoExpresion = self.exp2.ejecutar(console, scope);
        # obtenemos el vector
        self.id.generador = self.generador;
        vector:Simbolo = self.id.ejecutar(console, scope);
        if (vector.atrArr.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función Insert', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (valExp.tipo != vector.tipo):
            # ERROR. Tipos incompatibles
            _error = _Error(f'Tipos incompatibles. No se puede almacenar una expresión {valExp.tipo.name} en una variable de tipo {vector.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (valPos.tipo != TipoDato.INT64):
            # ERROR. No se puede acceder al indice val1.tipo.
            _error = _Error(f'No se puede acceder al indice {valPos.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        tempPos:str = self.generador.newTemp();
        self.generador.addOperacion(tempPos, vector.valor, valPos.valor, '+');
        self.generador.setHeap(tempPos, valExp.valor);
        scope.setValor(self.id.id, vector, self.linea, self.columna);

class Remove(Instruccion):
    def __init__(self, id:Expresion, exp:Expresion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.exp = exp;

    def ejecutar(self, console: Console, scope: Scope):
        '''
        <código de valPos>
        <código de vector>
        tempPos = vector.valor + valPos.valor;
        tempDelete = HEAP[tempPos];
        '''
        # indice del elemento a eliminar
        val = self.exp.ejecutar(console, scope);
        # obtenemos el vector
        vector:Simbolo = self.id.ejecutar(console, scope);
        if (vector.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función remove', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (not vector.esVector):
            # ERROR. Los arreglos no contiene la función remove
            _error = _Error(f'Los arreglos {vector.id} no contiene la función remove', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (val.tipo != TipoDato.INT64):
            # ERROR. Tipos incompatibles
            _error = _Error(f'Se esperaba una posición de tipo i64 pero se obtuvo un tipo {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # primero obtenemos el elemento que se va a eliminar
        valorRetorno = vector.valor[val.valor];
        # ahora eliminamos el elemento
        vector.valor.remove(valorRetorno);
        # revisaremos si se trata de un vector con un tamaño definido
        if (vector.with_capacity != None):
            if (vector.with_capacity < len(vector.valor)):
                vector.with_capacity = vector.with_capacity * 2;
        scope.setValor(self.id.id, vector, self.linea, self.columna);
        return RetornoExpresion(valorRetorno, vector.tipo, None);

class Contains(Instruccion):
    def __init__(self, id:str, exp, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.exp = exp;
    
    def ejecutar(self, console: Console, scope: Scope):
        # expresion del elemento a buscar
        val = self.exp.ejecutar(console, scope);
        # obtenemos el vector
        vector:Simbolo = self.id.ejecutar(console, scope);
        if (vector.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función contains', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (not vector.esVector):
            # ERROR. Los arreglos no contiene la función contains
            _error = _Error(f'Los arreglos {vector.id} no contiene la función contains', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (val.tipo != vector.tipo):
            # ERROR. Tipos incompatibles
            _error = _Error(f'Tipos incompatibles. No se puede almacenar una expresión {val.tipo.name} en una variable de tipo {vector.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # revisamos si existe el elemento en la lista
        if (val.valor in vector.valor):
            return RetornoExpresion(True, TipoDato.BOOLEAN, None);
        return RetornoExpresion(False, TipoDato.BOOLEAN, None);

class Longitud(Instruccion):
    def __init__(self, id:str, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;

    def ejecutar(self, console: Console, scope: Scope):
        # obtenemos el vector
        vector:Simbolo = self.id.ejecutar(console, scope);
        if (isinstance(vector, RetornoExpresion)):
            # ERROR. No es un vector
            _error = _Error(f'La expresión no es un vector, no contiene la función len', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (vector.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función len', scope.ambito, self.linea, self.columna, datetime.now());
            print(_error.descripcion)
            print("vall:: " + str(vector.valor))
            raise Exception(_error);
        # retornamos la longitud de la lista
        return RetornoExpresion(len(vector.valor), TipoDato.INT64, None);

class Capacity(Instruccion):
    def __init__(self, id:Expresion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;

    def ejecutar(self, console: Console, scope: Scope):
        '''
        temp = vector.with_capacity;
        '''
        # obtenemos el vector
        self.generador.addComentario('CAPACITY');
        self.id.generador = self.generador;
        vector:RetornoExpresion = self.id.ejecutar(console, scope);
        if (vector.atrArr.esVector == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función capacity', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # retornamos la capacidad de la lista
        temp:str = self.generador.newTemp();
        self.generador.addOperacion(temp, vector.atrArr.with_capacity, '', '');
        return RetornoExpresion(temp, TipoDato.INT64, False);