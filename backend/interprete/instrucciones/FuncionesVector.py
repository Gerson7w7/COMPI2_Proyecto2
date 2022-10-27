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
            tempPos = SP + pos;
            STACK[tempPos] = tempRetorno;
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
        if (vector.atrArr.with_capacity < vector.atrArr.size):
            vector.atrArr.with_capacity = vector.atrArr.with_capacity * 2;
        vector.valor = RetornoExpresion(tempRetorno, vector.tipo, True);
        pos:int = scope.setValor(self.id.id, vector, self.linea, self.columna);
        tempPos:str= self.generador.newTemp();
        self.generador.addOperacion(tempPos, 'SP', pos, '+');
        self.generador.setStack(tempPos, tempRetorno);

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
        if (vector.atrArr == None):
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
        Lloop:
            tempPosNext = tempPos + 1;
            temp = HEAP[tempPosNext];
            if(temp == -1) goto Lsalida;
            HEAP[tempPos] = temp;
            tempPos = tempPos + 1;
            goto Lloop;
        Lsalida:
            HEAP[tempPos] = -1;
        '''
        self.generador.addComentario('REMOVE');
        # indice del elemento a eliminar
        self.exp.generador = self.generador;
        valPos:RetornoExpresion = self.exp.ejecutar(console, scope);
        # obtenemos el vector
        self.id.generador = self.generador;
        vector:RetornoExpresion = self.id.ejecutar(console, scope);
        if (vector.atrArr == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función remove', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (valPos.tipo != TipoDato.INT64):
            # ERROR. Tipos incompatibles
            _error = _Error(f'Se esperaba una posición de tipo i64 pero se obtuvo un tipo {valPos.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        tempPos:str = self.generador.newTemp();
        tempDelete:str = self.generador.newTemp(); # esta etiqueta es la que hay que retornar
        tempPosNext:str = self.generador.newTemp();
        temp:str = self.generador.newTemp();
        Lloop:str = self.generador.newEtq();
        Lsalida:str = self.generador.newEtq();
        self.generador.addOperacion(tempPos, vector.valor, valPos.valor, '+');
        self.generador.getHeap(tempDelete, tempPos);
        self.generador.addEtq(Lloop);
        self.generador.addOperacion(tempPosNext, tempPos, '1', '+');
        self.generador.getHeap(temp, tempPosNext);
        self.generador.addIf(temp, '-1', '==', Lsalida);
        self.generador.setHeap(tempPos, temp);
        self.generador.addOperacion(tempPos, tempPos, '1', '+');
        self.generador.addGoto(Lloop);
        self.generador.addEtq(Lsalida);
        self.generador.setHeap(tempPos, '-1');
        vector.atrArr.size -= 1;
        scope.setValor(self.id.id, vector, self.linea, self.columna);
        return RetornoExpresion(tempDelete, vector.tipo, True);

class Contains(Instruccion):
    def __init__(self, id:Expresion, exp:Expresion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.exp = exp;
    
    def ejecutar(self, console: Console, scope: Scope):
        '''
        <código de valExp>
        <código de vector>
        Lloop:
            temp = HEAP[vector.valor];
            if(temp == -1) goto Lfalse;
            if(temp == valExp.valor) goto Ltrue;
            vector.valor = vector.valor + 1;
            goto Lloop;
        '''
        self.generador.addComentario('CONTAINS');
        # expresion del elemento a buscar
        self.exp.generador = self.generador;
        valExp:RetornoExpresion = self.exp.ejecutar(console, scope);
        # obtenemos el vector
        self.id.generador = self.generador;
        vector:RetornoExpresion = self.id.ejecutar(console, scope);
        if (vector.atrArr == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función contains', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (valExp.tipo != vector.tipo):
            # ERROR. Tipos incompatibles
            _error = _Error(f'Tipos incompatibles. No se puede almacenar una expresión {valExp.tipo.name} en una variable de tipo {vector.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # revisamos si existe el elemento en la lista
        Lloop:str = self.generador.newEtq();
        Ltrue:str = self.generador.newEtq();
        Lfalse:str = self.generador.newEtq();
        temp:str = self.generador.newTemp();
        self.generador.addEtq(Lloop);
        self.generador.getHeap(temp, vector.valor);
        self.generador.addIf(temp, '-1', '==', Lfalse);
        if(vector.tipo == TipoDato.STR or vector.tipo == TipoDato.STRING):
            '''
            tempPos = temp;
            Lloop2:
                tempVal = HEAP[tempPos];
                tempComparacion = HEAP[valExp.valor];
                if(tempVal == -1) goto Ltrue2;
                if(tempVal != tempComparacion) goto Lnext;
                tempPos = tempPos + 1;
                valExp.valor = valExp.valor + 1;
                goto Lloop2;
            Ltrue2:
                if(tempComparacion == -1) goto Ltrue;
                goto Lnext;
            Lnext:
            '''
            tempPos:str = self.generador.newTemp();
            tempVal:str = self.generador.newTemp();
            tempComparacion:str = self.generador.newTemp();
            Lloop2:str = self.generador.newEtq();
            Ltrue2:str = self.generador.newEtq();
            Lnext:str = self.generador.newEtq();
            self.generador.addOperacion(tempPos, temp, '', '');
            self.generador.addEtq(Lloop2);
            self.generador.getHeap(tempVal, tempPos);
            self.generador.getHeap(tempComparacion, valExp.valor);
            self.generador.addIf(tempVal, '-1', '==', Ltrue2);
            self.generador.addIf(tempVal, tempComparacion, '!=', Lnext);
            self.generador.addOperacion(tempPos, tempPos, '1', '+');
            self.generador.addOperacion(valExp.valor, valExp.valor, '1', '+');
            self.generador.addGoto(Lloop2);
            self.generador.addEtq(Ltrue2);
            self.generador.addIf(tempComparacion, '-1', '==', Ltrue);
            self.generador.addGoto(Lnext);
            self.generador.addEtq(Lnext);
        else:
            self.generador.addIf(temp, valExp.valor, '==', Ltrue);
        self.generador.addOperacion(vector.valor, vector.valor, '1', '+');
        self.generador.addGoto(Lloop);
        retorno = RetornoExpresion('', TipoDato.BOOLEAN, False);
        retorno.trueEtq = [Ltrue];
        retorno.falseEtq = [Lfalse];
        return retorno;

class Longitud(Instruccion):
    def __init__(self, id:Expresion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;

    def ejecutar(self, console: Console, scope: Scope):
        '''
        <código de vector>
        '''
        self.generador.addComentario('LEN');
        # obtenemos el vector
        self.id.generador = self.generador;
        vector:RetornoExpresion = self.id.ejecutar(console, scope);
        if (vector.atrArr == None):
            # ERROR. No es un vector
            _error = _Error(f'La variable {vector.id} no es un vector, no contiene la función len', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # retornamos la longitud de la lista
        return RetornoExpresion(vector.atrArr.size, TipoDato.INT64, False);

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