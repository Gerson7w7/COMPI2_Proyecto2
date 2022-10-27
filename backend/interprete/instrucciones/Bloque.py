from ..extra.Retorno import RetornoExpresion
from .Instruccion import Instruccion
from ..extra.Scope import Scope
from ..extra.Console import Console

class Bloque(Instruccion):
    def __init__(self, instrucciones:list, linea: int, columna: int):
        super().__init__(linea, columna)
        self.instrucciones = instrucciones;
        self.temp:str = '';

    def ejecutar(self, console: Console, scope: Scope, ambito:str):
        # creando un nuevo entorno
        newScope = Scope(scope, ambito);
        retorno:RetornoExpresion = None;
        for instruccion in self.instrucciones:
            try:
                instruccion.generador = self.generador;
                val:RetornoExpresion = instruccion.ejecutar(console, newScope);
                if (val != None):
                    if(self.temp == ''):
                        self.temp = self.generador.newTemp();
                    self.temp = val.valor;
                    retorno = RetornoExpresion(self.temp, val.tipo, True);
            except Exception as e:
                self.generador.errorSem(f'ERROR: {e.args[0].descripcion}. En la línea {e.args[0].linea}, columna {e.args[0].columna}\n', self.generador.newEtq());
                # agregamos a lista de errores
                console.error(e.args[0]);
        if (retorno != None):
            return retorno;