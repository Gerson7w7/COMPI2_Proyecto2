from .Bloque import Bloque
from interprete.expresiones.Relacional import Relacional
from interprete.extra.Tipos import TipoRelacional
from .Instruccion import Instruccion
from ..extra.Console import Console
from ..extra.Scope import Scope
from ..expresiones.Expresion import Expresion

class Match(Instruccion):
    def __init__(self, expresion:Expresion, case_list:list, linea: int, columna: int):
        super().__init__(linea, columna)
        self.expresion = expresion;
        self.case_list = case_list;

    def ejecutar(self, console: Console, scope: Scope):
        for case in self.case_list:
            condicionValida = False;
            # verificamos la se cumple la igualdad del o los cases
            for condicion in case.comparar():
                if (condicion == '_'):
                    condicionValida = True;
                    break;
                else:
                    condicionValida = Relacional(self.expresion, condicion, TipoRelacional.IGUALDAD, self.linea, self.columna).ejecutar(console, scope).valor;
                    if (condicionValida): break;
            # si se cumple, ejecutamos el case
            if (condicionValida):
                return case.ejecutar(console, scope);

class Case(Instruccion):
    def __init__(self, coincidencias, cuerpo, linea: int, columna: int):
        super().__init__(linea, columna)
        self.coincidencias = coincidencias;
        self.cuerpo = cuerpo;

    def ejecutar(self, console: Console, scope: Scope):
        if (isinstance(self.cuerpo, Bloque)):
            return self.cuerpo.ejecutar(console, scope, 'Match');
        return self.cuerpo.ejecutar(console, scope);

    
    def comparar(self):
        return self.coincidencias;