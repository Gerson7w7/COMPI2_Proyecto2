from .Tipos import TipoDato

class AtributosArreglo:
    def __init__(self, esVector:bool, with_capacity:str) -> None:
        self.esVector = esVector;
        self.with_capacity = with_capacity;
        self.size = 0;
        self.dimensiones = [];

class Simbolo:
    def __init__(self, valor:str, id: str, tipo: TipoDato, mut:bool, atrArr:AtributosArreglo, posicion:int, esRef:bool):
        self.valor = valor;
        self.id = id;
        self.tipo = tipo;
        self.mut = mut;
        self.atrArr = atrArr;
        self.posicion = posicion;
        self.esRef = esRef;