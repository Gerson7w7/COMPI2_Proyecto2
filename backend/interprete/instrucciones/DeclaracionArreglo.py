from ..expresiones.Arreglo import Arreglo
from ..expresiones.Vector import Vector
from ..extra.Simbolo import AtributosArreglo, Simbolo
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

class DeclaracionArreglo(Instruccion):
    def __init__(self, mut:bool, id:str, dimension:Dimension, valor:Expresion, linea:int, columna:int):
        super().__init__(linea, columna);
        self.mut = mut;
        self.id = id;
        self.dimension = dimension;
        self.valor = valor;
        self.regActual = None;

    def ejecutar(self, console: Console, scope):
        '''
        <código de arreglo>
        temp = SP + pos;
        STACK[temp] = valor.valor; 
        '''
        self.generador.addComentario('DECLARACION DE ARREGLO');
        if (self.valor == None):
            if (self.dimension.esVector):
                self.valor = Vector(None, None, self.linea, self.columna);
            else:
                self.valor = self.valorDefault(self.dimension);
        self.valor.generador = self.generador;
        valor:RetornoExpresion;
        if (isinstance(self.valor, RetornoExpresion)):
            valor = self.valor;
        else: 
            valor = self.valor.ejecutar(console, scope);
        atrArr = AtributosArreglo(False, None);
        if (self.dimension != None):
            for dim in self.dimension.dimensiones:
                atrArr.dimensiones.append(dim);
            atrArr.dimensiones.reverse();
            if (not valor.atrArr.esVector and atrArr.dimensiones != valor.atrArr.dimensiones and len(atrArr.dimensiones) > 0):
                _error = _Error(f'Las dimensiones de la expresión no son iguales a las indicadas.', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
        if (valor.atrArr.esVector):
            valor.atrArr.dimensiones = atrArr.dimensiones;
            valor.tipo = self.dimension.tipo if (valor.tipo == None) else valor.tipo;
            print("id:: " + str(id) + "     tipo:: " + str(valor.tipo))
            pos:int = scope.crearVariable(valor.valor, self.id, 'Vector', valor.tipo, self.mut, valor.atrArr, self.linea, self.columna, console, valor.esRef);
        else:
            pos:int = scope.crearVariable(valor.valor, self.id, 'Arreglo', valor.tipo, self.mut, valor.atrArr, self.linea, self.columna, console, valor.esRef);
        pos = pos + self.regActual if (self.regActual != None) else pos;
        temp:str= self.generador.newTemp();
        self.generador.addOperacion(temp, 'SP', pos, '+');
        self.generador.setStack(temp, valor.valor);

    def valorDefault(self, dimension:Dimension):
        arr = Arreglo([], self.linea, self.columna);
        if (dimension.tipo == TipoDato.INT64):
            arr.tipo = TipoDato.INT64;
            return arr;
        elif (dimension.tipo == TipoDato.FLOAT64):
            arr.tipo = TipoDato.FLOAT64;
            return arr;
        elif (dimension.tipo == TipoDato.BOOLEAN):
            arr.tipo = TipoDato.BOOLEAN;
            return arr;
        elif (dimension.tipo == TipoDato.CHAR):
            arr.tipo = TipoDato.CHAR;
            return arr;
        elif (dimension.tipo == TipoDato.STRING):
            arr.tipo = TipoDato.STRING;
            return arr;
        elif (dimension.tipo == TipoDato.STR):
            arr.tipo = TipoDato.STR;
            return arr;

class AsignacionArreglo(Instruccion):
    def __init__(self, id:str, indices:list, expresion:Expresion, linea: int, columna: int): 
        super().__init__(linea, columna);
        self.id = id;
        self.indices = indices;
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope):
        # aquí obtenemos el puntero hacia la primera posición del heap
        val:Simbolo = scope.getValor(self.id, self.linea, self.columna);
        # obtenemos el valor de la expresion
        if (val.atrArr.esVector):
            self.asignacionVector(val, console, scope);
        else:
            self.asignacionArreglo(val, console, scope);
        
    def asignacionArreglo(self, val:Simbolo, console:Console, scope):
        '''
        tIndice = 0;
        tempPos = SP + val.posicion;
        temp = STACK[tempPos];
        t1 = i*iDim;
        tIndice = tIndice + t1;
        ...
        tn = j*nDim;
        tIndice = tIndice + tn;
        tIndice = tIndice + k;
        tIndice = tIndice + temp;
        <código de valExp>
        HEAP[tIndice] = valExp.valor;
        '''
        self.generador.addComentario('ASIGNACIÓN A ARREGLO');
        _indices:list = [];
        for i in self.indices:
            i.generador = self.generador;
            index = i.ejecutar(console, scope);
            if(index.tipo != TipoDato.INT64):
                # ERROR. No se puede acceder a la posicion val.valor
                _error = _Error(f'No se puede acceder a la posición {index.valor}', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
            _indices.append(index.valor);
        tIndice:str = self.generador.newTemp();
        temp:str = self.generador.newTemp();
        tempPos:str = self.generador.newTemp();
        self.generador.addOperacion(tempPos, 'SP', val.posicion, '+');
        self.generador.addOperacion(tIndice, '0', '', '');
        self.generador.getStack(temp, tempPos);
        if (val.esRef):
            self.generador.getStack(temp, temp);
        atrArr = AtributosArreglo(False, None);
        esArr:bool = False;
        for i in range(len(val.atrArr.dimensiones)):
            try:
                if (i < len(val.atrArr.dimensiones) - 1):
                    tn:str = self.generador.newTemp();
                    self.generador.addOperacion(tn, _indices[i], self.dimTam(i + 1, val.atrArr.dimensiones), '*');
                    self.generador.addOperacion(tIndice, tIndice, tn, '+');
                else:
                    self.generador.addOperacion(tIndice, tIndice, _indices[i], '+');
                    atrArr.dimensiones = val.atrArr.dimensiones[i + 1:];
            except:
                atrArr.dimensiones = val.atrArr.dimensiones[i:];
                esArr = True;
                break;
        self.generador.addOperacion(tIndice, tIndice, temp, '+');
        self.expresion.generador = self.generador;
        valExp:RetornoExpresion = self.expresion.ejecutar(console, scope);
        if (val.tipo != valExp.tipo):
            _error = _Error(f'No se puede guardar una expresión de tipo {valExp.tipo.name} en un arreglo de tipo {val.tipo}', scope.ambito, self.linea, self.columna, datetime.now())
            raise Exception(_error);
        if (esArr):
            '''
            tLim = tIndice + total;
            Lloop:
                if (tIndice == tLim) goto Lsalida;
                HEAP[tIndice] = valExp;
                tIndice = tIndicie + 1;
                valExp = valExp + 1;
                goto Lloop;
            Lsalida:
            '''
            tLim:str = self.generador.newTemp();
            Lloop:str = self.generador.newEtq();
            Lsalida:str = self.generador.newEtq();
            total:int = 1;
            for index in atrArr.dimensiones:
                total *= index;
            self.generador.addOperacion(tLim, tIndice, total, '+');
            self.generador.addEtq(Lloop);
            self.generador.addIf(tIndice, tLim, '==', Lsalida);
            self.generador.setHeap(tIndice, f'HEAP[(int){valExp.valor}]');
            self.generador.addOperacion(tIndice, tIndice, '1', '+');
            self.generador.addOperacion(valExp.valor, valExp.valor, '1', '+');
            self.generador.addGoto(Lloop);
            self.generador.addEtq(Lsalida);
        else:
            self.generador.setHeap(tIndice, valExp.valor);
        scope.setValor(self.id, val, self.linea, self.columna);

    def asignacionVector(self, val:Simbolo, console:Console, scope):
        # indices para obtener el valor deseado
        '''
        tempPos = SP + val.posicion;
        temp = STACK[tempPos];
        '''
        self.generador.addComentario('ASIGNACIÓN A VECTOR');
        _indices:list = [];
        for i in self.indices:
            i.generador = self.generador;
            index = i.ejecutar(console, scope);
            if(index.tipo != TipoDato.INT64):
                # ERROR. No se puede acceder a la posicion val.valor
                _error = _Error(f'No se puede acceder a la posición {index.valor}', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
            _indices.append(index.valor);
        temp:str = self.generador.newTemp();
        tempPuntero:str = self.generador.newTemp();
        tempPos:str = self.generador.newTemp();
        self.generador.addOperacion(tempPos, 'SP', val.posicion, '+');
        self.generador.getStack(temp, tempPos);
        for i in _indices:
            '''
            tempPuntero = temp + indices[n];
            temp = HEAP[tempPuntero];
            '''
            self.generador.addOperacion(tempPuntero, temp, i, '+');
            self.generador.getHeap(temp, tempPuntero);
        self.expresion.generador = self.generador;
        valExp:RetornoExpresion = self.expresion.ejecutar(console, scope);
        if (val.tipo != valExp.tipo):
            _error = _Error(f'No se puede guardar una expresión de tipo {valExp.tipo.name} en un arreglo de tipo {val.tipo}', scope.ambito, self.linea, self.columna, datetime.now())
            raise Exception(_error);
        '''
        HEAP[tempPuntero] = valExp.valor;
        '''
        self.generador.setHeap(tempPuntero, valExp.valor);
        scope.setValor(self.id, val, self.linea, self.columna);

    def dimTam(self, indice:int, dimensiones:list) -> int:
        total:int = 1;
        while(indice < len(dimensiones)):
            total *= dimensiones[indice];
            indice += 1;
        return total