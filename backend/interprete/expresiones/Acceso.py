# clase para poder accesar a las variables
from ..extra.Retorno import RetornoExpresion
from ..extra.Tipos import TipoDato
from ..extra.Simbolo import AtributosArreglo, Simbolo
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from ..expresiones.Literal import Literal
from datetime import datetime

class Acceso(Expresion):
    def __init__(self,  id: str, linea:int, columna:int):
        super().__init__(linea, columna)
        self.id = id;

    def ejecutar(self, console: Console, scope: Scope):
        # buscamos y obtenemos el valor
        '''
        newTemp = STACK[valor.posicion];
        '''
        valor:RetornoExpresion = scope.getValor(self.id, self.linea, self.columna);
        newTemp = self.generador.newTemp();
        self.generador.addComentario('ACCESO A VARIABLE');
        self.generador.getStack(newTemp, valor.posicion);
        retorno = RetornoExpresion(newTemp, valor.tipo, True);
        if (valor.tipo == TipoDato.BOOLEAN):
            '''
            if (retorno.valor == 1) goto trueEtq;
            goto falseEtq;
            '''
            retorno.trueEtq = self.generador.newEtq();
            retorno.falseEtq = self.generador.newEtq();
            self.generador.addIf(retorno.valor, '1', '==', retorno.trueEtq);
            self.generador.addGoto(retorno.falseEtq);
            return retorno;
        if (valor.atrArr != None):
            retorno.atrArr = valor.atrArr;
        return retorno;
        
class AccesoArreglo(Expresion):
    def __init__(self, id:str, indices:list, linea:int, columna:int):
        super().__init__(linea, columna);
        self.id = id;
        self.indices = indices;

    def ejecutar(self, console: Console, scope: Scope):
        # aquí obtenemos el puntero hacia la primera posición del heap
        val:Simbolo = scope.getValor(self.id, self.linea, self.columna);
        if (val.atrArr.esVector):
            return self.accesoVector(val, console, scope);
        else:
            return self.accesoArreglo(val, console, scope);
        
    def accesoArreglo(self, val:Simbolo, console:Console, scope:Scope):
        # indices para obtener el valor deseado
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
        tempRetorno = HEAP[tIndice];
        '''
        self.generador.addComentario('ACCESO A ARREGLO');
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
        tempRetorno:str = self.generador.newTemp();
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
        if (esArr):
            retorno = RetornoExpresion(tIndice, val.tipo, True);
            retorno.atrArr = atrArr;
            return retorno;
        else:
            self.generador.getHeap(tempRetorno, tIndice);
            return RetornoExpresion(tempRetorno, val.tipo, True);

    def accesoVector(self, val:Simbolo, console:Console, scope:Scope):
        # indices para obtener el valor deseado
        '''
        temp = STACK[val.posicion];
        '''
        self.generador.addComentario('ACCESO A ARREGLO');
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
        self.generador.getStack(temp, val.posicion);
        for i in _indices:
            '''
            temp = temp + indices[n];
            temp = HEAP[temp];
            '''
            self.generador.addOperacion(temp, temp, i, '+');
            self.generador.getHeap(temp, temp);
        atrArr = AtributosArreglo(True, None);
        if (len(_indices) < len(val.atrArr.dimensiones)):
            atrArr.dimensiones = val.atrArr.dimensiones[len(_indices):];
            retorno = RetornoExpresion(temp, val.tipo, True);
            retorno.atrArr = atrArr;
            return retorno;
        else:
            return RetornoExpresion(temp, val.tipo, True);

    def dimTam(self, indice:int, dimensiones:list) -> int:
        total:int = 1;
        while(indice < len(dimensiones)):
            total *= dimensiones[indice];
            indice += 1;
        return total

class AccesoStruct(Expresion):
    def __init__(self, id:Acceso, atributo:str, linea, columna):
        super().__init__(linea, columna);
        self.id = id;
        self.atributo = atributo;

    def ejecutar(self, console: Console, scope: Scope):
        # obtenemos el struct
        struct: Simbolo = self.id.ejecutar(console, scope);
        # obtenemos el atributo del struct y retornamos
        return struct.valor.getValor(self.atributo, self.linea, self.columna);