from .Tipos import TipoDato

class Simbolo:
    def __init__(self, valor, id: str, tipo: TipoDato, mut:bool, esVector:bool, with_capacity:int, referencia):
        self.valor = valor;
        self.id = id;
        self.tipo = tipo;
        self.mut = mut;
        self.esVector = esVector;
        self.with_capacity = with_capacity;
        self.referencia = referencia;