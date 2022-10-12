from ..extra.Retorno import RetornoExpresion
from .Instruccion import Instruccion
from ..extra.Console import Console
from ..extra.Scope import Scope

class Loop(Instruccion):
    def __init__(self, bloque: Instruccion, linea: int, columna: int):
        super().__init__(linea, columna)
        self.bloque = bloque;

    def ejecutar(self, console: Console, scope: Scope):
        '''
        Lloop:
            <código del bloque>
            goto Lloop
        Lsalida:
        '''
        Lloop:str = self.generador.newEtq();
        Lsalida:str = self.generador.newEtq();
        # le pasamos la salida para que el break pueda utilizarlo
        console.breaks.append(Lsalida);
        # le pasamos el inicio para que el continue pueda utilizarlo
        console.continues.append(Lloop);
        self.generador.addEtq(Lloop);
        self.bloque.generador = self.generador;
        val:RetornoExpresion = self.bloque.ejecutar(console, scope, 'Loop');
        self.generador.addGoto(Lloop);
        self.generador.addEtq(Lsalida);
        if (val != None):
            return val;