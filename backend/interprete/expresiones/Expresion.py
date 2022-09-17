from ..extra.Console import Console
from ..extra.Generador import Generador
from ..extra.Scope import Scope

class Expresion:
    def __init__(self, linea, columna) -> None:
        self.linea: int = linea;
        self.columna: int = columna;
        self.generador:Generador = None;

    def ejecutar(self, console: Console, scope:Scope):
        pass; 