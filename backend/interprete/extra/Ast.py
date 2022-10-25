from ..instrucciones.Instruccion import Instruccion
from .Console import Console
from .Scope import Scope

# clase con la que se formará el ast final
class Ast:
    def __init__(self, instrucciones):
        self.generador = None;
        self.instrucciones: list = instrucciones;

    def ejecutar(self, console: Console, scope: Scope):
        # guardando las funciones
        for instruccion in self.instrucciones:
            instruccion.guardarFn(console, scope);
        for instruccion in self.instrucciones:
            #try:
            instruccion.generador = self.generador;
            instruccion.ejecutar(console, scope);
            # except Exception as e:
            #     # errores para recuperarse
            #     console.append(f'ERROR: {e.args[0].descripcion}. En la línea {e.args[0].linea}, columna {e.args[0].columna}\n');
            #     # agregamos a lista de errores
            #     console.error(e.args[0]);