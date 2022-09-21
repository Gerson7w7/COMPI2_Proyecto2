from .Tipos import TipoDato

class AtributosArreglo:
    def __init__(self, esVector:bool, with_capacity:int) -> None:
        self.esVector = esVector;
        self.with_capacity = with_capacity;

class Simbolo:
    def __init__(self, id: str, tipo: TipoDato, mut:bool, atrArr:AtributosArreglo, posicion:int):
        self.id = id;
        self.tipo = tipo;
        self.mut = mut;
        self.atrArr = atrArr;
        self.posicion = posicion;