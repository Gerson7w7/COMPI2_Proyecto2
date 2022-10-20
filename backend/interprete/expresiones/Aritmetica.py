from ..extra.Retorno import RetornoExpresion
from ..extra.Tipos import TipoAritmetica, TipoDato
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class Aritmetica(Expresion):
    def __init__(self, izquierda:Expresion, derecha:Expresion, tipo: TipoAritmetica, linea: int, columna: int):
        super().__init__(linea, columna)
        self.izquierda = izquierda;
        self.derecha = derecha;
        self.tipo = tipo;

    def ejecutar(self, console: Console, scope: Scope):
        # valor y tipo de la izquierda
        self.izquierda.generador = self.generador;
        valIzquierda:RetornoExpresion = self.izquierda.ejecutar(console, scope);
        # valor y tipo de la derecha
        self.derecha.generador = self.generador;
        valDerecha:RetornoExpresion = self.derecha.ejecutar(console, scope);
        
        # verificando que sea del mismo tipo de dato
        if ((valIzquierda.tipo == valDerecha.tipo) or (valIzquierda.tipo == TipoDato.STRING and valDerecha.tipo == TipoDato.STR)):
            # si es una suma
            if (self.tipo == TipoAritmetica.SUMA):  
                if (valIzquierda.tipo == TipoDato.INT64 or valIzquierda.tipo == TipoDato.FLOAT64):
                    # se hace la operacion correspondiente y se pasa el tipo
                    '''
                    temp = valizq.valor + valder.valor;
                    '''
                    temp:str = self.generador.newTemp();
                    self.generador.addComentario('SUMA DE 2 EXPRESIONES');
                    self.generador.addOperacion(temp, valIzquierda.valor, valDerecha.valor, '+');
                    return RetornoExpresion(temp, valIzquierda.tipo, True);
                elif (valIzquierda.tipo == TipoDato.STRING):
                    '''
                    temp = HP;
                    concatenar(valizq.valor);
                    concatenar(valder.valor);
                    HEAP[HP] = -1;
                    HP = HP + 1;
                    '''
                    newTemp:str = self.generador.newTemp();
                    self.generador.addComentario('CONCATENACIÓN');
                    self.generador.addOperacion(newTemp, 'HP', '', '');
                    self.concatenar(valIzquierda.valor);
                    self.concatenar(valDerecha.valor);
                    self.generador.setHeap('HP', '-1');
                    self.generador.ptrNextHeap();
                    return RetornoExpresion(newTemp, valIzquierda.tipo, True);
                # error no se puede operar izq con der
                _error = _Error(f'No se puede sumar {valIzquierda.valor} con {valDerecha.valor}', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
            elif (self.tipo == TipoAritmetica.RESTA):
                if (valIzquierda.tipo == TipoDato.INT64 or valIzquierda.tipo == TipoDato.FLOAT64):
                    # se hace la operacion correspondiente y se pasa el tipo
                    '''
                    temp = valizq - valder;
                    '''
                    temp:str = self.generador.newTemp();
                    self.generador.addComentario('RESTA');
                    self.generador.addOperacion(temp, valIzquierda.valor, valDerecha.valor, '-');
                    return RetornoExpresion(temp, valIzquierda.tipo, True);
                # error no se puede operar izq con der
                _error = _Error(f'No se puede restar {valIzquierda.valor} con {valDerecha.valor}', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
            elif (self.tipo == TipoAritmetica.MULTIPLICACION):
                if (valIzquierda.tipo == TipoDato.INT64 or valIzquierda.tipo == TipoDato.FLOAT64):
                    # se hace la operacion correspondiente y se pasa el tipo
                    '''
                    temp = valizq * valder;
                    '''
                    temp:str = self.generador.newTemp();
                    self.generador.addComentario('MULTIPLICACIÓN');
                    self.generador.addOperacion(temp, valIzquierda.valor, valDerecha.valor, '*');
                    return RetornoExpresion(temp, valIzquierda.tipo, True);
                # error no se puede operar izq con der
                _error = _Error(f'No se puede multiplicar {valIzquierda.valor} con {valDerecha.valor}', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
            elif (self.tipo == TipoAritmetica.DIVISION):
                if (valIzquierda.tipo == TipoDato.INT64 or valIzquierda.tipo == TipoDato.FLOAT64):
                    # se hace la operacion correspondiente y se pasa el tipo
                    '''
                    temp = valizq / valder;
                    '''
                    temp:str = self.generador.newTemp();
                    self.generador.addComentario('DIVISION');
                    self.generador.addOperacion(temp, valIzquierda.valor, valDerecha.valor, '/');
                    return RetornoExpresion(temp, TipoDato.FLOAT64, True);
                # error no se puede operar izq con der
                _error = _Error(f'No se puede dividir {valIzquierda.valor} con {valDerecha.valor}', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
            elif (self.tipo == TipoAritmetica.POTENCIA_i64):
                if (valIzquierda.tipo == TipoDato.INT64):
                    # se hace la operacion correspondiente y se pasa el tipo
                    '''
                    temp = valizq.valor;
                    tempContador = 1;
                    Lloop:
                        if (valder.valor == tempContador) goto Lsalida;
                        temp = temp * valizq.valor;
                        tempContador = tempContador + 1;
                        goto Lloop;
                    Lsalida:
                    '''
                    temp:str = self.generador.newTemp();
                    tempContador:str = self.generador.newTemp();
                    Lloop:str = self.generador.newEtq();
                    Lsalida:str = self.generador.newEtq();
                    self.generador.addComentario('POW');
                    self.generador.addOperacion(temp, valIzquierda.valor, '', '');
                    self.generador.addOperacion(tempContador, '1', '', '');
                    self.generador.addEtq(Lloop);
                    self.generador.addIf(valDerecha.valor, tempContador, '==', Lsalida);
                    self.generador.addOperacion(temp, temp, valIzquierda.valor, '*');
                    self.generador.addOperacion(tempContador, tempContador, '1', '+');
                    self.generador.addGoto(Lloop);
                    self.generador.addEtq(Lsalida);
                    return RetornoExpresion(temp, valIzquierda.tipo, True);
                # error no se puede operar izq con der
                _error = _Error(f'No se puede operar la potencia de {valIzquierda.valor} con {valDerecha.valor}', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
            elif (self.tipo == TipoAritmetica.MODULO):
                if (valIzquierda.tipo == TipoDato.INT64 or valIzquierda.tipo == TipoDato.FLOAT64):
                    # se hace la operacion correspondiente y se pasa el tipo
                    '''
                    temp = valizq % valder;
                    '''
                    temp:str = self.generador.newTemp();
                    self.generador.addComentario('MODULO');
                    if(valIzquierda.esTemp): 
                        valIzquierda.valor = f'(int){valIzquierda.valor}';
                    if(valDerecha.esTemp): 
                        valDerecha.valor = f'(int){valDerecha.valor}';    
                    self.generador.addOperacion(temp, valIzquierda.valor, valDerecha.valor, '%');
                    return RetornoExpresion(temp, valIzquierda.tipo, True);
                # error no se puede operar izq con der
                _error = _Error(f'No se puede operar el módulo de {valIzquierda.valor} con {valDerecha.valor}', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
        #error, tipos diferentes
        print(str(valIzquierda.tipo) +'=='+ str(valDerecha.tipo))
        _error = _Error(f'No se puede operar un tipo {valIzquierda.tipo.name} con un tipo {valDerecha.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now())
        raise Exception(_error);

    def concatenar(self, valor):
        '''
        Lloop:
            tempChar = HEAP[valor];
            if (tempChar == -1) goto Lsalida;
            HEAP[HP] = tempChar;
            HP = HP + 1;
            valor = valor + 1;
            goto Lloop;
        Lsalida:
        '''
        Lloop:str = self.generador.newEtq();
        tempChar:str = self.generador.newTemp();
        Lsalida:str = self.generador.newEtq();
        self.generador.addEtq(Lloop);
        self.generador.getHeap(tempChar, valor);
        self.generador.addIf(tempChar, '-1', '==', Lsalida);
        self.generador.setHeap('HP', tempChar);
        self.generador.ptrNextHeap();
        self.generador.addOperacion(valor, valor, '1', '+');
        self.generador.addGoto(Lloop);
        self.generador.addEtq(Lsalida);