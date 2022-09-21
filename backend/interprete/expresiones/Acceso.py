# clase para poder accesar a las variables
from ..extra.Retorno import RetornoExpresion
from ..extra.Tipos import TipoDato
from ..extra.Simbolo import Simbolo
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class Acceso(Expresion):
    def __init__(self,  id: str, linea:int, columna:int):
        super().__init__(linea, columna)
        self.id = id;

    def ejecutar(self, console: Console, scope: Scope):
        # buscamos y obtenemos el valor
        valor = scope.getValor(self.id, self.linea, self.columna);
        newTemp = self.generador.newTemp();
        self.generador.getStack(newTemp, valor.posicion);
        if(valor.tipo == TipoDato.BOOLEAN):
            '''
            if(tn == 1) goto self.EV
            goto self.EF
            '''
            val:RetornoExpresion = RetornoExpresion(newTemp, valor.tipo, False);
            if(self.trueEtq == ''):
                self.trueEtq = self.generador.newEtq();
            if(self.falseEtq == ''):
                self.falseEtq = self.generador.newEtq();
            self.generador.addIf(newTemp, '1', '==', self.trueEtq);
            self.generador.addGoto(self.falseEtq);
            val.trueEtq = self.trueEtq;
            val.falseEtq = self.falseEtq;
            return val;
        else:
            return RetornoExpresion(newTemp, valor.tipo, True);

class AccesoArreglo(Expresion):
    def __init__(self, id:str, indices:list, linea:int, columna:int):
        super().__init__(linea, columna);
        self.id = id;
        self.indices = indices;

    def ejecutar(self, console: Console, scope: Scope):
        # recuperamos el símbolo
        listaSimbolo:Simbolo = scope.getValor(self.id, self.linea, self.columna);
        # indices para obtener el valor deseado
        _indices:list = [];
        for i in self.indices:
            index = i.ejecutar(console, scope);
            if(index.tipo != TipoDato.INT64):
                # ERROR. No se puede acceder a la posicion val.valor
                _error = _Error(f'No se puede acceder a la posición {index.valor}', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
            _indices.append(index.valor);
        try:
            val = self.obtenerValor(listaSimbolo.valor, _indices, 0);
            if (isinstance(val, list)):
                return Simbolo(val, '', listaSimbolo.tipo, listaSimbolo.mut, listaSimbolo.esVector, listaSimbolo.with_capacity, None);
            return Simbolo(val, '', listaSimbolo.tipo, listaSimbolo.mut, listaSimbolo.esVector, listaSimbolo.with_capacity, listaSimbolo.referencia);
        except:
            _error = _Error(f'Indice fuera de rango', scope.ambito, self.linea, self.columna, datetime.now())
            raise Exception(_error);

    def obtenerValor(self, lista:list, _indices:list, i:int):
        if (i + 1 == len(_indices)):
            indice = _indices[i];
            return lista[indice];
        else:
            indice = _indices[i];
            return self.obtenerValor(lista[indice], _indices, i + 1);

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