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
        nuevaCadena:str = self.cadena;
        if (self.expresiones != None):
            for expresion in self.expresiones:
                val = expresion.ejecutar(console, scope)
                if (isinstance(val.valor, list) == True):
                    nuevaCadena = nuevaCadena.replace("{:?}", str(val.valor), 1);
                else:
                    nuevaCadena = nuevaCadena.replace("{}", str(val.valor), 1);
            # para agregar los saltos de líneas que vengas explícitos
            nuevaCadena = nuevaCadena.replace('\\n', '\n');
            if (self.saltoLinea):
                console.append(nuevaCadena + '\n');
            else:
                console.append(nuevaCadena);
        else:
            # para agregar los saltos de líneas que vengas explícitos
            nuevaCadena = nuevaCadena.replace('\\n', '\n');
            if (self.saltoLinea):
                console.append(nuevaCadena + '\n');
            else:
                console.append(nuevaCadena);