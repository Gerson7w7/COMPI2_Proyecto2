from ..extra.Tipos import TipoDato
from ..extra.Simbolo import AtributosArreglo
from ..extra.Retorno import RetornoExpresion
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from datetime import datetime

class Vector(Expresion):
    def __init__(self, valor:list, with_capacity:Expresion, linea:int, columna:int):
        super().__init__(linea, columna);
        self.valor = valor;
        self.with_capacity = with_capacity;
        self.temp = '';
        self.tipo = None;

    def ejecutar(self, console: Console, scope):
        # el vector siempre será de una dimensión
        self.generador.addComentario('VECTOR');
        if (self.valor == None and self.with_capacity == None):
            # Vec::new();
            '''
            self.temp = HP;
            HP = HP + 1;
            HEAP[self.temp] = -1;
            '''
            self.temp = self.generador.newTemp();
            self.generador.addOperacion(self.temp, 'HP', '', '');
            self.generador.addOperacion('HP', 'HP', '1', '+');
            self.generador.setHeap(self.temp, '-1');
            retorno = RetornoExpresion(self.temp, self.tipo, True);
            atrArr = AtributosArreglo(True, 1);
            atrArr.size = 0;
            retorno.atrArr = atrArr;
        elif(self.valor != None):
            # vec![exp, exp, exp];
            '''
            self.temp = HP;
            tempRetorno = self.temp;
            HP = HP + len(self.valor)
            <código de la lista>
            HEAP[self.temp] = -1;
            '''
            self.temp = self.generador.newTemp();
            tempRetorno:str = self.generador.newTemp();
            self.generador.addOperacion(self.temp, 'HP', '', '');
            self.generador.addOperacion(tempRetorno, self.temp, '', '');
            self.generador.addOperacion('HP', 'HP', len(self.valor) + 1, '+');
            self.recorrerLista(self.valor, console, scope);
            self.generador.setHeap(self.temp, '-1');
            retorno = RetornoExpresion(tempRetorno, self.tipo, True);
            atrArr = AtributosArreglo(True, len(self.valor) + 1);
            atrArr.size = len(self.valor);
            retorno.atrArr = atrArr;
        elif(self.with_capacity != None):
            # Vec::with_capacity(3);
            '''
            self.temp = HP;
            <código de valCapacity>
            HP = HP + valCapacity;
            HEAP[self.temp] = -1;
            '''
            self.temp = self.generador.newTemp();
            self.generador.addOperacion(self.temp, 'HP', '', '');
            self.with_capacity.generador = self.generador;
            valCapacity:RetornoExpresion = self.with_capacity.ejecutar(console, scope);
            if (valCapacity.tipo != TipoDato.INT64):
                _error = _Error(f'La capacidad de un vector tiene que ser de tipo INT64', 'Vector', self.linea, self.columna, datetime.now());
                raise Exception(_error);
            self.generador.addOperacion('HP', 'HP', valCapacity.valor, '+');
            self.generador.setHeap(self.temp, '-1');
            retorno = RetornoExpresion(self.temp, self.tipo, True);
            atrArr = AtributosArreglo(True, int(valCapacity.valor));
            atrArr.size = 0;
            retorno.atrArr = atrArr;
        return retorno;

    def recorrerLista(self, valor, console:Console, scope):
        if (isinstance(valor, list)):
            for v in valor:
                self.recorrerLista(v, console, scope);
        elif(isinstance(valor, dict)):
            for i in range(valor.get('cantidad')):
                self.recorrerLista(valor.get('expresion'), console, scope);
        else:
            valor.generador = self.generador;
            val:RetornoExpresion = valor.ejecutar(console, scope);
            if (self.tipo == None):
                self.tipo = val.tipo;
            elif(self.tipo != val.tipo):
                _error = _Error(f'Los arreglos tienen que ser de un solo tipo. Se obtuvo {self.tipo.name} y {val.tipo.name}', 'Arreglo', self.linea, self.columna, datetime.now());
                raise Exception(_error);
            '''
            HEAP[self.temp] = val.valor;
            self.temp = self.temp + 1;
            '''
            self.generador.setHeap(self.temp, val.valor);
            self.generador.addOperacion(self.temp, self.temp, '1', '+');