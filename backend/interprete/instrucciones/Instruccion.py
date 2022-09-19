from ..extra.Retorno import RetornoExpresion
from ..extra.Generador import Generador
from ..extra.Console import Console

class Instruccion:
    def __init__(self, linea: int, columna: int) -> None:
        self.linea: int = linea;
        self.columna: int = columna;
        self.generador:Generador = Generador();

    def ejecutar(self, console: Console, scope) -> RetornoExpresion:
        pass;