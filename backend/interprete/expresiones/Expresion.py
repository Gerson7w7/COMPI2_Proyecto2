from ..extra.Console import Console
from ..extra.Generador import Generador

class Expresion:
    def __init__(self, linea, columna) -> None:
        self.linea: int = linea;
        self.columna: int = columna;
        self.trueEtq:list = [];
        self.falseEtq:list = [];
        self.generador:Generador = None;

    def ejecutar(self, console: Console, scope):
        pass; 