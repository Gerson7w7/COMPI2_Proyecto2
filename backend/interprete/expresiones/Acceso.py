# clase para poder accesar a las variables
from ..extra.Retorno import RetornoExpresion
from ..extra.Tipos import TipoDato
from ..extra.Simbolo import AtributosArreglo, Simbolo
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class Acceso(Expresion):
    def __init__(self,  id: str, linea:int, columna:int):
        super().__init__(linea, columna)
        self.id = id;
        self.esRef = False;

    def ejecutar(self, console: Console, scope: Scope):
        # buscamos y obtenemos el valor
        '''
        tempPos = SP + pos;
        newTemp = STACK[tempPos];
        '''
        self.generador.addComentario('ACCESO A VARIABLE');
        newTemp = self.generador.newTemp();
        valor:Simbolo = scope.getValor(self.id, self.linea, self.columna);
        retorno = RetornoExpresion(newTemp, valor.tipo, True);
        if (valor.atrArr != None):
            retorno.atrArr = valor.atrArr;
        tempPos:str= self.generador.newTemp();
        self.generador.addOperacion(tempPos, 'SP', valor.posicion, '+');
        if (self.esRef): 
            retorno.esRef = True;
            retorno.valor = tempPos;
            return retorno; # devuelve la posición del arr/vec
        self.generador.getStack(newTemp, tempPos);
        if (valor.tipo == TipoDato.BOOLEAN):
            '''
            if (retorno.valor == 1) goto trueEtq;
            goto falseEtq;
            '''
            retorno.trueEtq = [self.generador.newEtq()];
            retorno.falseEtq = [self.generador.newEtq()];
            self.generador.addIf(retorno.valor, '1', '==', retorno.trueEtq[0]);
            self.generador.addGoto(retorno.falseEtq[0]);
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
        tempPos = SP + pos;
        temp = STACK[tempPos];
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
        Lmensaje:str = self.generador.newEtq();
        Lsalida:str = self.generador.newEtq();
        tempPos:str= self.generador.newTemp();
        self.generador.addOperacion(tIndice, '0', '', '');
        self.generador.addOperacion(tempPos, 'SP', val.posicion, '+');
        self.generador.getStack(temp, tempPos);
        if (val.esRef):
            '''
            <> // ref del arreglo
            temp = STACK[temp]; // valor del arreglo
            '''
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
        self.generador.addIf(tIndice, self.dimTam(0, _indices), '<', Lmensaje);
        if (esArr):
            retorno = RetornoExpresion(tIndice, val.tipo, True);
            retorno.atrArr = atrArr;
            self.generador.addGoto(Lsalida);
            self.generador.errorSem('Indice fuera de rango', Lmensaje);
            self.generador.addEtq(Lsalida);
            return retorno;
        else:
            self.generador.getHeap(tempRetorno, tIndice);
            self.generador.addGoto(Lsalida);
            self.generador.errorSem('Indice fuera de rango', Lmensaje);
            self.generador.addEtq(Lsalida);
            return RetornoExpresion(tempRetorno, val.tipo, True);

    def accesoVector(self, val:Simbolo, console:Console, scope:Scope):
        # indices para obtener el valor deseado
        '''
        tempPos = SP + pos;
        temp = STACK[tempPos];
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
        tempPos:str= self.generador.newTemp();
        self.generador.addOperacion(tempPos, 'SP', val.posicion, '+');
        self.generador.getStack(temp, tempPos);
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

    def dimTam(self, indice:int, dimensiones:list) -> str:
        '''
        tempTotal = 1;
        tempTotal = tempTotal * dimensiones[indice];
        '''
        tempTotal:str = self.generador.newTemp();
        self.generador.addOperacion(tempTotal, '1', '', '');
        while(indice < len(dimensiones)):
            self.generador.addOperacion(tempTotal, tempTotal, dimensiones[indice], '*');
            indice += 1;
        return tempTotal

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