from ..instrucciones.Funcion import Funcion
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
            instruccion.guardarFn(scope);

        main:Funcion = scope.getFuncion('main', 0, 0);
        main.generador = self.generador;
        main.newScope = scope;
        main.ejecutar(console, scope);
        main.yaActivo = True;
        scope.setFuncion('main', main);

        flag:bool = True;
        while(flag):
            flag = False;
            for instruccion in self.instrucciones:
                #try:
                funcion:Funcion = scope.getFuncion(instruccion.id, 0, 0);
                if (funcion.sePuedeEjecutar and not funcion.yaActivo):
                    funcion.generador = self.generador;
                    funcion.ejecutar(console, scope);
                    funcion.yaActivo = True;
                    scope.setFuncion(funcion.id, funcion);
                if (not funcion.yaActivo):
                    flag = True;
                # except Exception as e:
                #     # errores para recuperarse
                #     console.append(f'ERROR: {e.args[0].descripcion}. En la línea {e.args[0].linea}, columna {e.args[0].columna}\n');
                #     # agregamos a lista de errores
                #     console.error(e.args[0]);