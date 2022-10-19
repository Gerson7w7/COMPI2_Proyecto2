from ..expresiones.Expresion import Expresion
from ..extra.Retorno import RetornoExpresion
from ..extra.Tipos import TipoDato
from .Instruccion import Instruccion
from ..extra.Console import Console
from ..extra.Scope import Scope

class Imprimir(Instruccion):
    def __init__(self, saltoLinea:bool, cadena:str, expresiones:list, linea: int, columna: int):
        super().__init__(linea, columna)
        self.saltoLinea = saltoLinea;
        self.cadena = cadena;
        self.expresiones = expresiones;

    def ejecutar(self, console: Console, scope: Scope):
        i:int = 0;
        esArr:bool = False;
        esExp:bool = False;
        self.generador.addComentario('=== IMPRIMIENDO ===');
        for c in self.cadena:
            if (c == '{'): esExp = True; pass;
            elif (c == ':'): 
                if (esExp): 
                    esArr = True;
                else: 
                    self.generador.addPrintf('c', f'(char){str(ord(c))}');
            elif (c == '?'):
                if (not (esExp and esArr)): 
                    self.generador.addPrintf('c', f'(char){str(ord(c))}');
            elif (c == '}'): 
                # expresiones
                exp:Expresion = self.expresiones[i];
                exp.generador = self.generador
                val:RetornoExpresion = exp.ejecutar(console, scope);
                i += 1;
                if (esExp and esArr):
                    if (val.atrArr.esVector):
                        self.imprimirVector(val, 1);
                    else:
                        self.imprimirArreglo(val);
                else:
                    self.imprimirExpresion(val);
            else:
                self.generador.addPrintf('c', f'(char){str(ord(c))}');
        # si es println
        if(self.saltoLinea):
            self.generador.newLine();

    def imprimirExpresion(self, val:RetornoExpresion):
        if(val.tipo == TipoDato.CHAR):
            '''
            printf("%c", 'val.valor');
            '''
            self.generador.addComentario('IMPRIMIENDO CHAR');
            self.generador.addPrintf('c', f'(char){val.valor}');
        elif(val.tipo == TipoDato.INT64):
            '''
            printf("%d", (int)"valor.valor");
            '''
            self.generador.addComentario('IMPRIMIENDO INT Y BOOLEAN');
            self.generador.addPrintf('d', f'(int){val.valor}');
        elif(val.tipo == TipoDato.BOOLEAN):
            '''
            trueEtq:
                printf("%d", (int)1);
                goto Lsalida;
            trueEtq:
                printf("%d", (int)1);
            Lsalida:
            '''
            Lsalida:str = self.generador.newEtq();
            self.generador.addEtq(val.trueEtq);
            self.generador.addPrintf('d', '1');
            self.generador.addGoto(Lsalida);
            self.generador.addEtq(val.falseEtq);
            self.generador.addPrintf('d', '0');
            self.generador.addEtq(Lsalida);
        elif(val.tipo == TipoDato.FLOAT64):
            '''
            printf("%f", (double)"valor.valor");
            '''
            self.generador.addComentario('IMPRIMIENDO FLOAT');
            self.generador.addPrintf('f', f'(double){val.valor}');
        elif(val.tipo == TipoDato.STR or val.tipo == TipoDato.STRING):
            '''
            Lloop:
                temp = HEAP[(int)val.valor]; 
                if temp == -1 goto Lsalida;   
                printf("%c", (char)temp);
                val.valor = val.valor + 1;
                goto Lloop
            Lsalida:
            '''
            self.generador.addComentario('IMPRIMIENDO STR O STRING');
            Lloop:str = self.generador.newEtq();
            Lsalida:str = self.generador.newEtq();
            temp:str = self.generador.newTemp();
            self.generador.addEtq(Lloop);
            self.generador.getHeap(temp, val.valor);
            self.generador.addIf(temp, '-1', '==', Lsalida);
            self.generador.addPrintf('c', f'(char){temp}');
            self.generador.addOperacion(val.valor, val.valor, '1', '+');
            self.generador.addGoto(Lloop);
            self.generador.addEtq(Lsalida);

    def imprimirArreglo(self, val:RetornoExpresion):
        '''
        tempLim = val.valor + total;
        Lloop:
            if (val.valor == tempLim) goto Lsalida;
            temp = HEAP[val.valor];
            <código para imprimir>
            val.valor = val.valor + 1;
            goto Lloop;
        Lsalida:
        '''
        # arreglos
        self.generador.addComentario('IMPRIMIENDO ARREGLO');
        total:int = 1;
        for index in val.atrArr.dimensiones:
            total *= index;
        tempLim:str = self.generador.newTemp();
        Lloop:str = self.generador.newEtq();
        Lsalida:str = self.generador.newEtq();
        temp:str = self.generador.newTemp();
        self.generador.addOperacion(tempLim, val.valor, total, '+');
        self.generador.addEtq(Lloop);
        self.generador.addIf(val.valor, tempLim, '==', Lsalida);
        self.generador.getHeap(temp, val.valor);
        self.imprimirExpresion(RetornoExpresion(temp, val.tipo, True));
        self.generador.addPrintf('c', '(char)44'); # 44 = ,
        self.generador.addOperacion(val.valor, val.valor, '1', '+');
        self.generador.addGoto(Lloop);
        self.generador.addEtq(Lsalida);

    def imprimirVector(self, val:RetornoExpresion, i:int):
        '''
        Lloop:
            temp = HEAP[val.valor];
            if (temp == -1) goto Lsalida;
            ...
            <código para imprimir>
            val.valor = val.valor + 1;
            goto Lloop;
        Lsalida:
        '''
        # arreglos
        self.generador.addComentario('IMPRIMIENDO VECTOR');
        Lloop:str = self.generador.newEtq();
        Lsalida:str = self.generador.newEtq();
        temp:str = self.generador.newTemp();
        self.generador.addEtq(Lloop);
        self.generador.getHeap(temp, val.valor);
        self.generador.addIf(temp, '-1', '==', Lsalida);
        if (i != len(val.atrArr.dimensiones)):
            retorno = RetornoExpresion(temp, val.tipo, True);
            retorno.atrArr = val.atrArr;
            self.imprimirVector(retorno, i + 1);
        else:
            self.imprimirExpresion(RetornoExpresion(temp, val.tipo, True));
            self.generador.addPrintf('c', '(char)44'); # 44 = ,
        self.generador.addOperacion(val.valor, val.valor, '1', '+');
        self.generador.addGoto(Lloop);
        self.generador.addEtq(Lsalida);