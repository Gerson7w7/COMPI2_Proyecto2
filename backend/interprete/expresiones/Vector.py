from ..extra.Simbolo import AtributosArreglo
from ..extra.Retorno import RetornoExpresion
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class Vector(Expresion):
    def __init__(self, valor:list, with_capacity:int, linea:int, columna:int):
        super().__init__(linea, columna);
        self.valor = valor;
        self.with_capacity = with_capacity;
        self.contador = 0;
        self.temp = '';
        self.dimensiones = [];
        self.tipo = None;

    def ejecutar(self, console: Console, scope:Scope):
        if (self.valor == None and self.with_capacity == None):
            # Vec::new();
            '''
            self.temp = HP;
            tempRetorno = self.temp;
            HP = HP + 1;
            <código de la lista>
            '''
            self.generador.addComentario('VECTOR');
            self.temp = self.generador.newTemp();
            tempRetorno:str = self.generador.newTemp();
            self.generador.addOperacion(self.temp, 'HP', '', '');
            self.generador.addOperacion(tempRetorno, self.temp, '', '');
            self.generador.addOperacion('HP', 'HP', '1', '+');
            retorno = RetornoExpresion(tempRetorno, self.tipo, True);
            atrArr = AtributosArreglo(True, 2);
            atrArr.dimensiones = [1];
            retorno.atrArr = atrArr;
        elif(self.valor != None):
            pass;
        elif(self.with_capacity != None):
            pass;
        return retorno;
        '''
        self.temp = HP;
        HP = HP + self.contador
        <código de la lista>
        '''
        self.generador.addComentario('ARREGLO');
        self.reservarEspacio(self.valor, False);
        self.temp = self.generador.newTemp();
        tempRetorno:str = self.generador.newTemp();
        self.generador.addOperacion(self.temp, 'HP', '', '');
        self.generador.addOperacion(tempRetorno, self.temp, '', '');
        self.generador.addOperacion('HP', 'HP', self.contador, '+');
        self.recorrerLista(self.valor, console, scope);
        retorno = RetornoExpresion(tempRetorno, self.tipo, True);
        atrArr = AtributosArreglo(False, None);
        atrArr.dimensiones = self.dimensiones;
        retorno.atrArr = atrArr;

    def recorrerLista(self, valor, console:Console, scope:Scope):
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
