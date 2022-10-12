from ..extra.Retorno import RetornoExpresion
from .Bloque import Bloque
from .Instruccion import Instruccion
from ..extra.Console import Console, _Error
from ..extra.Scope import Scope
from ..expresiones.Expresion import Expresion
from datetime import datetime

class Match(Instruccion):
    def __init__(self, expresion:Expresion, case_list:list, linea: int, columna: int):
        super().__init__(linea, columna)
        self.expresion = expresion;
        self.case_list = case_list;

    def ejecutar(self, console: Console, scope: Scope):
        '''
        <código de expresion>
        goto Lprueba;
        L1:
            <bloque de código del case1>
            goto Lsalida;
        Ln:
            <bloque de código del casen>
            goto Lsalida;
        Ldefault: 
            <bloque de código del default>
            goto Lsalida;
        Lprueba:
            if (E.valor == case1.valor) goto L1;
            if (E.valor == casen.valor) goto Ln;
            goto Ldefult;
        Lsalida:
        '''
        retorno:RetornoExpresion = None;
        temp:str = self.generador.newTemp();
        Lsalida:str = self.generador.newEtq();
        self.expresion.generador = self.generador;
        valMatch:RetornoExpresion = self.expresion.ejecutar(console, scope);
        Lprueba:str = self.generador.newEtq();
        self.generador.addGoto(Lprueba);
        Ldefault:str = self.generador.newEtq();
        for case in self.case_list:
            # etiqueta para ejecutar el case
            case.etq = self.generador.newEtq();
            if(case.getCoincidencias()[0] == '_'):
                self.generador.addEtq(Ldefault);
            else:
                self.generador.addEtq(case.etq);
            case.generador = self.generador;
            valCase:RetornoExpresion = case.ejecutar(console, scope);
            if(valCase != None):
                self.generador.addOperacion(temp, valCase.valor, '', '');
                retorno = RetornoExpresion(temp, valCase.tipo, True);
            self.generador.addGoto(Lsalida);
        self.generador.addEtq(Lprueba);
        for case in self.case_list:
            for coincidencia in case.getCoincidencias():
                if (coincidencia == '_'):
                    self.generador.addGoto(Ldefault);
                else:
                    coincidencia.generador = self.generador;
                    valCoincidencia:RetornoExpresion = coincidencia.ejecutar(console, scope);
                    if (valMatch.tipo != valCoincidencia.tipo):
                        _error = _Error(f'La expresión del match y de las coincidencias tiene que ser del mismo tipo.', scope.ambito, self.linea, self.columna, datetime.now())
                        raise Exception(_error);
                    self.generador.addIf(valMatch.valor, valCoincidencia.valor, '==', case.etq);
        self.generador.addEtq(Lsalida);
        # si se cumple, ejecutamos el case
        if (retorno != None):
            return retorno;

class Case(Instruccion):
    def __init__(self, coincidencias, cuerpo, linea: int, columna: int):
        super().__init__(linea, columna)
        self.coincidencias = coincidencias;
        self.cuerpo = cuerpo;
        self.etq = '';

    def ejecutar(self, console: Console, scope: Scope):
        self.cuerpo.generador = self.generador;
        if (isinstance(self.cuerpo, Bloque)):
            # bloque
            return self.cuerpo.ejecutar(console, scope, 'Match');
        # expresion
        return self.cuerpo.ejecutar(console, scope);

    def getCoincidencias(self):
        return self.coincidencias;