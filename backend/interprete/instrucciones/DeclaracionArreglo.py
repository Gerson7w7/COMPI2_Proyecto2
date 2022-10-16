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

class WithCapacity:
    def __init__(self, esVector:bool, capacidad:int):
        self.esVector = esVector;
        self.capacidad = capacidad;

class DeclaracionArreglo(Instruccion):
    def __init__(self, mut:bool, id:str, dimension:Dimension, valor:Expresion, linea:int, columna:int):
        super().__init__(linea, columna);
        self.mut = mut;
        self.id = id;
        self.dimension = dimension;
        self.valor = valor;

    def ejecutar(self, console: Console, scope):
        '''
        <código de arreglo>
        STACK[pos] = valor.valor; 
        '''
        self.generador.addComentario('DECLARACION DE ARREGLO');
        self.valor.generador = self.generador;
        valor:RetornoExpresion = self.valor.ejecutar(console, scope);
        if (self.dimension != None and not self.dimension.esVector):
            atrArr = AtributosArreglo(False, None);
            for dim in self.dimension.dimensiones:
                atrArr.dimensiones.append(dim);
            atrArr.dimensiones.reverse();
            print(str(atrArr.dimensiones) + ' != ' + str(valor.atrArr.dimensiones))
            if (atrArr.dimensiones != valor.atrArr.dimensiones):
                _error = _Error(f'Las dimensiones de la expresión no son iguales a las indicadas.', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
        if (valor.atrArr.esVector):
            print("sisoiii");
            print("dim:: " + str(valor.atrArr.dimensiones))
            print("capacity:: " + str(valor.atrArr.with_capacity))
            pos:int = scope.crearVariable(valor.valor, self.id, 'Vector', valor.tipo, self.mut, valor.atrArr, self.linea, self.columna, console);
        else:
            pos:int = scope.crearVariable(valor.valor, self.id, 'Arreglo', valor.tipo, self.mut, valor.atrArr, self.linea, self.columna, console);
        self.generador.setStack(pos, valor.valor);

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
        '''
        tIndice = 0;
        temp = STACK[val.posicion];
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
        self.generador.addOperacion(tIndice, '0', '', '');
        self.generador.getStack(temp, val.posicion);
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

    def dimTam(self, indice:int, dimensiones:list) -> int:
        total:int = 1;
        while(indice < len(dimensiones)):
            total *= dimensiones[indice];
            indice += 1;
        return total