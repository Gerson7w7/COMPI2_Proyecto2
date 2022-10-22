from ..extra.Simbolo import AtributosArreglo
from ..extra.Retorno import RetornoExpresion
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from datetime import datetime

class Arreglo(Expresion):
    def __init__(self, valor:list or dict, linea:int, columna:int):
        super().__init__(linea, columna);
        self.valor = valor;
        self.contador = 0;
        self.temp = '';
        self.dimensiones = [];
        self.tipo = None;

    def ejecutar(self, console: Console, scope):
        '''
        self.temp = HP;
        tempRetorno = self.temp;
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
        atrArr.size = int(self.dimensiones[0]) if (len(self.dimensiones) > 0) else 0;
        retorno.atrArr = atrArr;
        return retorno;

    def reservarEspacio(self, valor, agregado:bool):
        if (isinstance(valor, list)):
            if (not agregado and len(valor) > 1):
                self.dimensiones.append(len(valor));
            for v in valor:
                self.reservarEspacio(v, agregado);
                agregado = True;
        elif(isinstance(valor, dict)):
            if (not agregado):
                self.dimensiones.append(valor.get('cantidad'));
            for i in range(valor.get('cantidad')):
                self.reservarEspacio(valor.get('expresion'), agregado);
                agregado = True;
        else:
            self.contador += 1;

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
