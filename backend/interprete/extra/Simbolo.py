from ..instrucciones.Arreglo import AtributosArreglo
from .Tipos import TipoDato

class Simbolo:
    def __init__(self, id: str, tipo: TipoDato, mut:bool, atrArr:AtributosArreglo, posicion:int):
        self.id = id;
        self.tipo = tipo;
        self.mut = mut;
        self.atrArr = atrArr;
        self.posicion = posicion;