# clase para manejar la salida del código
from datetime import datetime

class Console:
    def __init__(self):
        self.output = "";
        self.errores = [];
        self.simbolos = [];

    def append(self, text):
        self.output += text;

    def error(self, error):
        self.errores.append(error); 

    def appendSimbolo(self, simbolo):
        self.simbolos.append(simbolo);

class _Error:
    def __init__(self, descripcion:str, ambito:str, linea:str, columna:str, fecha:datetime):
        self.descripcion = descripcion;
        self.ambito = ambito;
        self.linea = linea;
        self.columna = columna;
        self.fecha = fecha;

    def serializar(self):
        return {
            'descripcion': self.descripcion,
            'ambito': self.ambito,
            'linea': self.linea,
            'columna': self.columna,
            'fecha': self.fecha,
        }