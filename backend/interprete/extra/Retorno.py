from ..extra.Simbolo import AtributosArreglo
from .Tipos import TipoDato

class RetornoExpresion:
    def __init__(self, valor, tipo: TipoDato, esTemp:bool):
        self.valor = valor;
        self.tipo = tipo;
        self.esTemp = esTemp;
        self.trueEtq = '';
        self.falseEtq = '';
        self.atrArr:AtributosArreglo = None;