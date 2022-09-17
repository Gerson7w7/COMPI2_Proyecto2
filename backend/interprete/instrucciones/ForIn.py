from ..extra.Simbolo import Simbolo
from ..instrucciones.Arreglo import Arreglo
from ..extra.Tipos import TipoDato, TipoTransferencia
from .Instruccion import Instruccion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from .Declaracion import Asignacion, Declaracion
from ..expresiones.Literal import Literal
from datetime import datetime

class ForIn(Instruccion):
    def __init__(self, id:str, iterable, bloque:Instruccion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.iterable = iterable;
        self.bloque = bloque;

    def ejecutar(self, console: Console, scope: Scope):
        # nuevo scope
        newScope = Scope(scope, 'ForIn');
        if (isinstance(self.iterable, list)):
            # rango
            if (len(self.iterable) == 2):
                inferior = self.iterable[0].ejecutar(console, newScope);
                superior = self.iterable[1].ejecutar(console, newScope);
                if (inferior.tipo != TipoDato.INT64 or superior.tipo != TipoDato.INT64):
                    # ERROR. Los rangos tienen que ser enteros
                    _error = _Error(f'Los rangos tienen que ser de tipo i64', scope.ambito, self.linea, self.columna, datetime.now());
                    raise Exception(_error);
                # ejecutamos la declaración 
                declaracion = Declaracion(True, self.id, TipoDato.INT64, self.iterable[0], self.linea, self.columna);
                declaracion.ejecutar(console, newScope);
                for i in range(inferior.valor, superior.valor):
                    # actualizamos la variable de control
                    asignacion = Asignacion(self.id, Literal(i, TipoDato.INT64, self.linea, self.columna), self.linea, self.columna);
                    asignacion.ejecutar(console, newScope);
                    # ejecutamos el bloque de código
                    valBloque = self.bloque.ejecutar(console, newScope, 'ForIn');
                    # si es una instruccion de transferencia se analiza
                    if (valBloque != None):
                        # break
                        if (valBloque.retorno == TipoTransferencia.BREAK):
                            if (valBloque.valor != None):
                                # error no se puede retornar un valor en un for in
                                _error = _Error(f'No se puede retornar una expresión con el break en un for in', scope.ambito, self.linea, self.columna, datetime.now());
                                raise Exception(_error);
                            break;
                        # return
                        elif (valBloque.retorno == TipoTransferencia.RETURN):
                            return valBloque;
                        # continua
                        elif (valBloque.retorno == TipoTransferencia.CONTINUE):
                            continue;
            # arreglo
            else:
                arr = Arreglo(False, None, None, [], None, None, None, None);
                listaArr = arr.nuevaDimension(self.iterable, console, scope, None, None, -1);
                # ejecutamos la declaración 
                declaracion = Declaracion(True, self.id, arr.tipo, Literal(listaArr[0], arr.tipo, self.linea, self.columna), self.linea, self.columna);
                declaracion.ejecutar(console, newScope);
                for i in listaArr:
                    # actualizamos la variable de control
                    asignacion = Asignacion(self.id, Literal(i, arr.tipo, self.linea, self.columna), self.linea, self.columna);
                    asignacion.ejecutar(console, newScope);
                    # ejecutamos el bloque de código
                    valBloque = self.bloque.ejecutar(console, newScope, 'ForIn');
                    # si es una instruccion de transferencia se analiza
                    if (valBloque != None):
                        # break
                        if (valBloque.retorno == TipoTransferencia.BREAK):
                            if (valBloque.valor != None):
                                # error no se puede retornar un valor en un for in
                                _error = _Error(f'No se puede retornar una expresión con el break en un for in', scope.ambito, self.linea, self.columna, datetime.now());
                                raise Exception(_error);
                            break;
                        # return
                        elif (valBloque.retorno == TipoTransferencia.RETURN):
                            return valBloque;
                        # continua
                        elif (valBloque.retorno == TipoTransferencia.CONTINUE):
                            continue;
        else:
            # acceso a vector o arreglo
            val:Simbolo = self.iterable.ejecutar(console, newScope);
            if (not isinstance(val.valor, list)):
                # ERROR. La expresión no es iterable
                _error = _Error(f'La expresión {val.valor} no es iterable', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
            # ejecutamos la declaración 
            valorInicial = val.valor[0];
            if (isinstance(valorInicial, Scope)):
                valorInicial = Simbolo(valorInicial, 'Struct', val.tipo, val.mut, val.esVector, val.with_capacity, val.referencia);
            else:
                valorInicial = Literal(val.valor[0], val.tipo, self.linea, self.columna);
            declaracion = Declaracion(True, self.id, val.tipo, valorInicial, self.linea, self.columna);
            declaracion.ejecutar(console, newScope);
            for i in val.valor:
                    # actualizamos la variable de control
                    if (isinstance(i, Scope)):
                        valorActual = Simbolo(i, 'Struct', val.tipo, val.mut, val.esVector, val.with_capacity, val.referencia);
                    else:
                        valorActual = Literal(i, val.tipo, self.linea, self.columna);
                    asignacion = Asignacion(self.id, valorActual, self.linea, self.columna);
                    asignacion.ejecutar(console, newScope);
                    # ejecutamos el bloque de código
                    valBloque = self.bloque.ejecutar(console, newScope, 'ForIn');
                    # si es una instruccion de transferencia se analiza
                    if (valBloque != None):
                        # break
                        if (valBloque.retorno == TipoTransferencia.BREAK):
                            if (valBloque.valor != None):
                                # error no se puede retornar un valor en un for in
                                _error = _Error(f'No se puede retornar una expresión con el break en un for in', scope.ambito, self.linea, self.columna, datetime.now());
                                raise Exception(_error);
                            break;
                        # return
                        elif (valBloque.retorno == TipoTransferencia.RETURN):
                            return valBloque;
                        # continua
                        elif (valBloque.retorno == TipoTransferencia.CONTINUE):
                            continue;