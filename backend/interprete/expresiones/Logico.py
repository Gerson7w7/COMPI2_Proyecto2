from interprete.extra.Retorno import RetornoExpresion
from interprete.extra.Tipos import TipoDato
from interprete.extra.Tipos import TipoLogico
from .Expresion import Expresion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from datetime import datetime

class Logico(Expresion):
    def __init__(self, izquierda:Expresion, derecha:Expresion, tipo:TipoLogico, linea, columna):
        super().__init__(linea, columna)
        self.izquierda = izquierda;
        self.derecha = derecha;
        self.tipo = tipo;

    def ejecutar(self, console: Console, scope: Scope):
        # ejecutando los valores
        self.izquierda.generador = self.generador;
        val1:RetornoExpresion = self.izquierda.ejecutar(console, scope);
        print(val1.valor + " -- " + val1.trueEtq + " -- " + val1.falseEtq)
        # verificando si se trata de NOT
        if (self.derecha != None):
            if (val1.tipo != TipoDato.BOOLEAN):
                # ERROR solo se aceptan bools
                _error = _Error(f'Solo se puede comparar a nivel lógico tipos booleanos', scope.ambito, self.linea, self.columna, datetime.now());
                raise Exception(_error);
            # OR
            if (self.tipo == TipoLogico.OR):
                '''
                val1.Lfalse:
                    ...
                '''
                self.generador.addComentario('LÓGICA OR');
                self.generador.addEtq(val1.falseEtq);
                self.derecha.generador = self.generador;
                val2:RetornoExpresion = self.derecha.ejecutar(console,scope);
                if (val2.tipo != TipoDato.BOOLEAN):
                    _error = _Error(f'Solo se puede comparar a nivel lógico tipos booleanos', scope.ambito, self.linea, self.columna, datetime.now());
                    raise Exception(_error);
                retorno = RetornoExpresion('', TipoDato.BOOLEAN, True);
                retorno.trueEtq += f'{val1.trueEtq}:\n{val2.trueEtq}:\n';
                retorno.falseEtq = val2.falseEtq;
                return retorno;
            # AND
            else:
                '''
                val1.Ltrue:
                    ...
                '''
                self.generador.addComentario('LÓGICA AND');
                self.generador.addEtq(val1.trueEtq);
                self.derecha.generador = self.generador;
                val2:RetornoExpresion = self.derecha.ejecutar(console,scope);
                if (val2.tipo != TipoDato.BOOLEAN):
                    _error = _Error(f'Solo se puede comparar a nivel lógico tipos booleanos', scope.ambito, self.linea, self.columna, datetime.now());
                    raise Exception(_error);
                retorno = RetornoExpresion('', TipoDato.BOOLEAN, None);
                retorno.trueEtq = val2.trueEtq;
                retorno.falseEtq += f'{val1.falseEtq}:\n{val2.falseEtq}:\n';
                return retorno;
        else:
            # NOT
            if (val1.tipo != TipoDato.BOOLEAN):
                # ERROR solo se aceptan bools
                _error = _Error(f'Solo se puede comparar a nivel lógico tipos booleanos', scope.ambito, self.linea, self.columna, datetime.now())
                raise Exception(_error);
            self.generador.addComentario('LÓGICA NOT');
            retorno = RetornoExpresion(not val1.valor, TipoDato.BOOLEAN, None);
            retorno.trueEtq = val1.falseEtq;
            retorno.falseEtq = val1.trueEtq;
            return retorno;