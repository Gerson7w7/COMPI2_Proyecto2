from .Console import Console
from .Scope import Scope

# clase con la que se formará el ast final
class Ast:
    def __init__(self, instrucciones):
        self.instrucciones: list = instrucciones;

    def ejecutar(self, console: Console, scope: Scope):
        for instruccion in self.instrucciones:
            try:
                instruccion.ejecutar(console, scope);
            except Exception as e:
                # errores para recuperarse
                console.append(f'ERROR: {e.args[0].descripcion}. En la línea {e.args[0].linea}, columna {e.args[0].columna}\n');
                # agregamos a lista de errores
                console.error(e.args[0]);
        funMain = scope.getFuncion('main', 0, 0);
        # si es el main se ejecuta de una vez
        funMain.bloque.ejecutar(console, scope, 'Main');