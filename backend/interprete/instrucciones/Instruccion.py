from ..extra.Console import Console

class Instruccion:
    def __init__(self, linea: int, columna: int):
        self.linea: int = linea;
        self.columna: int = linea;

    def ejecutar(self, console: Console, scope):
        pass;