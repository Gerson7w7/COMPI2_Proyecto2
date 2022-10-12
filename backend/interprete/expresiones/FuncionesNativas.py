from ..extra.Tipos import TipoDato
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from ..extra.Retorno import RetornoExpresion
from datetime import datetime
import math
import copy

class Abs(Expresion):
    def __init__(self, expresion:Expresion,  linea: int, columna: int):
        super().__init__(linea, columna)
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        self.expresion.generador = self.generador;
        val = self.expresion.ejecutar(console, scope);
        # verificamos que sea un tipo de dato numérico
        if (val.tipo == TipoDato.INT64 or val.tipo == TipoDato.FLOAT64):
            '''
            if (val.valor >= 0) goto Lsalida;
            Lnegativo:
                temp = val.valor * -1;
            Lsalida:
            '''
            Lsalida:str = self.generador.newEtq();
            Lnegativo:str = self.generador.newEtq();
            temp:str = self.generador.newTemp();
            self.generador.addComentario('ABS');
            self.generador.addIf(val.valor, '0', '>=', Lsalida);
            self.generador.addEtq(Lnegativo);
            self.generador.addOperacion(temp, val.valor, '-1', '*');
            self.generador.addEtq(Lsalida);
            return RetornoExpresion(temp, val.tipo, True);
        # error, solo se aceptan datos numéricos
        _error = _Error(f'Solo se puede obtener el valor absoluto de un número, no de un {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);

class Sqrt(Expresion):
    def __init__(self, expresion:Expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        self.expresion.generador = self.generador;
        val = self.expresion.ejecutar(console, scope);
        # verificamos que sea un tipo de dato numérico
        if (val.tipo == TipoDato.INT64 or val.tipo == TipoDato.FLOAT64):
            '''
            temp = 0;
            Lloop:
                tempCuadrado = temp * temp;
                if (tempCuadrado == val.valor) goto Lsalida;
                temp = temp + 1;
                goto Lloop;
            Lsalida: 
            '''
            temp:str = self.generador.newTemp();
            Lloop:str = self.generador.newEtq();
            tempCuadrado:str = self.generador.newTemp();
            Lsalida:str = self.generador.newEtq();
            self.generador.addComentario('SQRT');
            self.generador.addOperacion(temp, '0', '', '');
            self.generador.addEtq(Lloop);
            self.generador.addOperacion(tempCuadrado, temp, temp, '*');
            self.generador.addIf(tempCuadrado, val.valor, '>=', Lsalida);
            self.generador.addOperacion(temp, temp, '1', '+');
            self.generador.addGoto(Lloop);
            self.generador.addEtq(Lsalida);
            return RetornoExpresion(temp, val.tipo, True);
        # error, solo se aceptan datos numéricos
        _error = _Error(f'Solo se puede obtener la raíz cuadrada de un número, no de un {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);

# sirve tanto par to_string() como para to_owned() xd
class ToString(Expresion):
    def __init__(self, expresion:Expresion, linea:int, columna:int):
        super().__init__(linea, columna)
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        self.expresion.generador = self.generador;
        val = self.expresion.ejecutar(console, scope);
        # verificamos que sea un tipo de dato str o string
        if (val.tipo == TipoDato.STR or val.tipo == TipoDato.STRING):
            self.generador.addComentario('TOSTRING o TOOWNED');
            return RetornoExpresion(val.valor, TipoDato.STRING, True);
        # error, solo se aceptan datos string
        _error = _Error(f'Solo se puede convertir a un string un &str, no de un {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);

class Clone(Expresion):
    def __init__(self, expresion:Expresion, linea, columna):
        super().__init__(linea, columna);
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        # retorna lo que sea que venga, ya que solo es una copia
        self.expresion.generador = self.generador;
        self.generador.addComentario('CLONE');
        return copy.deepcopy(self.expresion.ejecutar(console, scope));

class Chars(Expresion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion;

    def ejecutar(self, console: Console, scope: Scope):
        # ejecutamos la expresión
        val = self.expresion.ejecutar(console, scope);
        if (val.tipo != TipoDato.STRING and val.tipo != TipoDato.STR):
            # ERROR. Solo se puede convertir a una lista de caracteres si se trata de un string
            _error = _Error(f'Solo se puede convertir a una lista de caracteres si se trata de un string o &str, no de un {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now())
            raise Exception(_error);
        # pasamos la cadena a una lista
        listaChar:list = []
        for c in val.valor:
            listaChar.append(c);
        return RetornoExpresion(listaChar, val.tipo, None);
