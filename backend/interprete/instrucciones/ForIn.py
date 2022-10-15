from .DeclaracionArreglo import DeclaracionArreglo
from ..extra.Retorno import RetornoExpresion
from ..expresiones.Expresion import Expresion
from ..extra.Simbolo import AtributosArreglo, Simbolo
from ..extra.Tipos import TipoDato
from .Instruccion import Instruccion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from .Declaracion import Declaracion
from datetime import datetime

class ForIn(Instruccion):
    def __init__(self, id:str, iterable:Expresion or dict, bloque:Instruccion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.iterable = iterable;
        self.bloque = bloque;

    def ejecutar(self, console: Console, scope: Scope):
        # nuevo scope
        self.generador.addComentario('FOR IN');
        newScope = Scope(scope, 'ForIn');
        if (isinstance(self.iterable, dict)):
            '''
            <código inferiorVal>
            <código superiorVal>
            Lloop:
                temp = STACK[val.posicion];
                if (temp > superiorVal.valor) goto Lsalida;
                <código bloque>
                temp = temp + 1;
                STACK[val.posicion] = temp;
                goto Lloop;
            Lsalida: 
            '''
            # rango
            declaracion = Declaracion(True, self.id, TipoDato.INT64, self.iterable.get('inferior'), self.linea, self.columna);
            declaracion.generador = self.generador;
            declaracion.ejecutar(console, newScope);
            self.iterable.get('superior').generador = self.generador;
            superiorVal:RetornoExpresion = self.iterable.get('superior').ejecutar(console, newScope);
            if (superiorVal.tipo != TipoDato.INT64):
                # ERROR. Los rangos tienen que ser enteros
                _error = _Error(f'Los rangos tienen que ser de tipo i64', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
            Lloop:str = self.generador.newEtq();
            Lsalida:str = self.generador.newEtq();
            temp:str = self.generador.newTemp();
            val:Simbolo = newScope.getValor(self.id, self.linea, self.columna);
            self.generador.addEtq(Lloop);
            self.generador.getStack(temp, val.posicion);
            self.generador.addIf(temp, superiorVal.valor, '>', Lsalida);
            console.breaks.append(Lsalida);
            console.continues.append(Lloop);
            self.bloque.generador = self.generador;
            valRetorno:RetornoExpresion = self.bloque.ejecutar(console, newScope, 'For In');
            self.generador.addOperacion(temp, temp, '1', '+');
            self.generador.setStack(val.posicion, temp);
            self.generador.addGoto(Lloop);
            self.generador.addEtq(Lsalida);
        else:
            '''
            <código valArr>
            tempLim = valArr.valor + valArr.atrArr.dimensiones[0];
            Lloop:
                temp = HEAP[valArr.valor];
                STACK[pos] = temp;
                if (valArr.valor > tempLim) goto Lsalida;
                <código bloque>
                valArr.valor = valArr.valor + 1;
                goto Lloop;
            Lsalida: 
            '''
            # expresiones iterables
            Lloop:str = self.generador.newEtq();
            Lsalida:str = self.generador.newEtq();
            temp:str = self.generador.newTemp();
            tempLim:str = self.generador.newTemp();
            # ejecutamos el vector/arreglo
            self.iterable.generador = self.generador;
            valArr:RetornoExpresion = self.iterable.ejecutar(console, newScope);
            self.generador.addOperacion(tempLim, valArr.valor, valArr.atrArr.dimensiones[0], '+');
            self.generador.addEtq(Lloop);
            self.generador.getHeap(temp, valArr.valor);
            posicion:int = newScope.crearVariable(temp, self.id, 'Variable', valArr.tipo, True, None, self.linea, self.columna, console);
            self.generador.setStack(posicion, temp);
            self.generador.addIf(valArr.valor, tempLim, '>=', Lsalida);
            console.breaks.append(Lsalida);
            console.continues.append(Lloop);
            self.bloque.generador = self.generador;
            valRetorno:RetornoExpresion = self.bloque.ejecutar(console, newScope, 'For In');
            self.generador.addOperacion(valArr.valor, valArr.valor, '1', '+');
            self.generador.addGoto(Lloop);
            self.generador.addEtq(Lsalida);
        # retornamos el valor en caso de que se tenga
        if (valRetorno != None):
            return valRetorno;