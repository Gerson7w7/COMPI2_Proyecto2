from .Tipos import TipoDato, TipoTransferencia

class RetornoExpresion:
    def __init__(self, valor, tipo: TipoDato, esTemp:bool):
        self.valor = valor;
        self.tipo = tipo;
        self.esTemp = esTemp;
        self.trueEtq = '';
        self.falseEtq = '';