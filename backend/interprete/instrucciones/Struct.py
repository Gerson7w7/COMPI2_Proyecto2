from ..expresiones.Acceso import Acceso
from ..extra.Simbolo import Simbolo
from .Instruccion import Instruccion
from ..extra.Scope import Scope
from ..extra.Console import Console, _Error
import copy
from datetime import datetime 

class ExpresionesStruct:
    def __init__(self, idInstancia:str, expresiones:list):
        self.idInstancia = idInstancia;
        self.expresiones = expresiones;

class Struct(Instruccion):
    def __init__(self, id:str, atributos:list, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.atributos = atributos;

    def ejecutar(self, console: Console, scope: Scope):
        scope.guardarStruct(self.id, self, self.linea, self.columna);

    def obtenerAtributo(self, id:str, scope:Scope):
        for att in self.atributos:
            if (id == att.id):
                return att;
        # ERROR.
        _error = _Error(f'El atributo {id} no se ha econtrado', scope.ambito, self.linea, self.columna, datetime.now());
        raise Exception(_error);

class InstanciaStruct(Instruccion):
    def __init__(self, mut:bool, id:str, tipo, instancia:ExpresionesStruct, linea: int, columna: int):
        super().__init__(linea, columna);
        self.mut = mut;
        self.id = id;
        self.tipo = tipo;
        self.instancia = instancia;

    def ejecutar(self, console: Console, scope: Scope):
        # el nuevo scope es el que guardará los atributos del struct
        newScope: Scope = Scope(scope.getGlobal(), 'Struct');
        # obtenemos el struct
        struct:Struct = scope.getStruct(self.instancia.idInstancia, self.linea, self.columna);
        # verificamos que tenga los mismos campos
        if (len(struct.atributos) != len(self.instancia.expresiones)):
            # ERROR. el estruct recibe x argumentos pero se encontraron y.
            _error = _Error(f'El estruct recibe {len(struct.atributos)} argumentos pero se encontraron {len(self.instancia.expresiones)}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # verificamos que el tipo y la instancia sea del mismo tipo de struct si es que se especificó
        if (self.tipo != None and self.tipo != self.instancia.idInstancia):
            _error = _Error(f'Se esperaba una expresión de tipo {self.tipo.name} y se encontró {self.instancia.idInstancia}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        for exp in self.instancia.expresiones:
            # primero traemos el atributo o declaracion desde el struct
            atributo = struct.obtenerAtributo(exp.id, scope);
            # ahora ejecutamos la declaración para que se cree la variable
            atributo.valor = exp.valor.ejecutar(console, scope);
            atributo.ejecutar(console, newScope);
        # creando la variable de tipo struct
        scope.crearVariable(self.id, newScope, 'Struct', self.instancia.idInstancia, self.mut, None, None, None, self.linea, self.columna, console);

class AsignacionStruct(Instruccion):
    def __init__(self, id:Acceso, atributo:str, expresion, linea: int, columna: int):
        super().__init__(linea, columna);
        self.id = id;
        self.atributo = atributo;
        self.expresion = expresion;
    
    def ejecutar(self, console: Console, scope: Scope):
        # ejecutamos la expresión que es la que se cambiará 
        val = self.expresion.ejecutar(console, scope);
        # obtenemos el scope del struct
        atributos:Simbolo = copy.deepcopy(self.id.ejecutar(console, scope));
        # verificamos que sea mutable y que sean del mismo tipo
        simbolo:Simbolo = atributos.valor.getValor(self.atributo, self.linea, self.columna);
        if (simbolo == None):
            print("ERROR. El atributo " + self.atributo + " no se ha especificado en el struct.");
            _error = _Error(f'El atributo {self.atributo} no se ha especificado en el struct', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (not atributos.mut):
            print("ERROR. No se puede modificar una variable que no sea mutable.");
            _error = _Error(f'No se puede modificar la variable {atributos.id} porque no es mutable', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        if (simbolo.tipo != val.tipo):
            print("ERROR. Un tipo de dato " + simbolo.tipo + " no se puede convertir en " + val.tipo);
            _error = _Error(f'Un tipo de dato {simbolo.tipo.name} no se puede convertir en {val.tipo.name}', scope.ambito, self.linea, self.columna, datetime.now());
            raise Exception(_error);
        # cambiamos el valor del atributo indicado
        atributos.valor.setValor(self.atributo, val, self.linea, self.columna);
        # guardamos o seteamos los cambios
        scope.setValor(self.id, atributos, self.linea, self.columna);