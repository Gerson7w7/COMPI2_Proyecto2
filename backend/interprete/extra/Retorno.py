from .Tipos import TipoDato, TipoTransferencia

class RetornoExpresion:
    def __init__(self, valor, tipo: TipoDato, retorno:TipoTransferencia, esTemp:bool):
        self.valor = valor;
        self.tipo = tipo;
        self.retorno = retorno;
        self.esTemp = esTemp;