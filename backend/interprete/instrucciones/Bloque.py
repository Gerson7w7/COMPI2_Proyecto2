from .Transferencia import Transferencia
from .Instruccion import Instruccion
from ..extra.Scope import Scope
from ..extra.Console import Console, _Error
from datetime import datetime

class Bloque(Instruccion):
    def __init__(self, instrucciones:list, linea: int, columna: int):
        super().__init__(linea, columna)
        self.instrucciones = instrucciones;

    def ejecutar(self, console: Console, scope: Scope, ambito:str):
        # creando un nuevo entorno
        newScope = Scope(scope, ambito);
        for instruccion in self.instrucciones:
            try:
                val = instruccion.ejecutar(console, newScope);
                if (val != None):
                    if (ambito == 'Main'):
                        _error = _Error(f'No se esperaba la sentencia {val.retorno.name}', scope.ambito, self.linea, self.columna, datetime.now());
                        raise Exception(_error);
                    return val;
            except Exception as e:
                console.append(f'ERROR: {e.args[0].descripcion}. En la línea {e.args[0].linea}, columna {e.args[0].columna}\n');
                # agregamos a lista de errores
                console.error(e.args[0]);