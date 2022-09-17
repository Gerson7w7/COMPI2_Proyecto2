from ..instrucciones.Arreglo import Dimension

class TablaSimbolo:
    def __init__(self, identificador:str, tipo:str, tipoDato:str, ambito:str, linea:int, columna:int):
        self.identificador = identificador;
        self.tipo = tipo;
        self.tipoDato = tipoDato;
        self.ambito = ambito;
        self.linea = linea;
        self.columna = columna;

    def serializar(self):
        tipoDato = self.tipoDato;
        if (isinstance(self.tipoDato, Dimension)):
            tipoDato = self.tipoDato.tipo;
        return {
            'identificador': self.identificador,
            'tipo': self.tipo,
            'tipoDato': tipoDato,
            'ambito': self.ambito,
            'linea': self.linea,
            'columna': self.columna,
        }