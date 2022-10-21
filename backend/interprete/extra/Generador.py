# clase para generar el código en 3d
class Generador:
    def __init__(self) -> None:
        self.generador = None;
        self.temporal:int = 0;
        self.etiqueta:int = 0;
        self.codigo = [];
        self.temporales = [];

    # obtiene los temporales usados
    def getTemporales(self) -> str:
        return ','.join(self.temporales);

    # obtiene el código generado
    def getCodigo(self) -> str:
        # encabezado en C
        codigo:str = '#include <stdio.h>\n';
        codigo += '#include <math.h>\n';
        codigo += 'double HEAP[10000];\n';
        codigo += 'double STACK[10000];\n';
        codigo += 'double SP = 0;\n';
        codigo += 'double HP = 0;\n';
        # cuerpo del código en C
        if(0 < len(self.temporales)):
            codigo += f'double {self.getTemporales()};\n\n';
        codigo += 'void main(){\n';
        codigo += '\n'.join(self.codigo);
        codigo += '\nreturn;\n}\n';
        return codigo;

    # genera un nuevo temporal
    def newTemp(self) -> str:
        temporal:str = f't{str(self.temporal)}';
        self.temporal += 1;
        # guardamos el temporal en la lista de temps.
        self.temporales.append(temporal);
        return temporal;

    # genera una nueva etiqueta
    def newEtq(self) -> str:
        etiqueta:str = f'L{str(self.etiqueta)}';
        self.etiqueta += 1;
        return etiqueta;

    # añade una etiqueta al código a generar
    def addEtq(self, etiqueta:str or list) -> None:
        if(isinstance(etiqueta, list)):
            etiqueta = ':\n'.join(etiqueta);
        self.codigo.append(f'{etiqueta}:');
    
    # añade expresion aritmética
    def addOperacion(self, temp:str, izq:str, der:str, operador:str) -> None:
        self.codigo.append(f'{temp} = {izq} {operador} {der};');

    # añade goto Ln
    def addGoto(self, etq:str) -> None:
        self.codigo.append(f'goto {etq};');

    # mueve una posición del puntero del heap
    def ptrNextHeap(self) -> None:
        self.codigo.append('HP = HP + 1;');

    # mueve una posición siguiente del puntero del stack
    def ptrNextStack(self, indice:str) -> None:
        self.codigo.append(f'SP = SP + {indice};');

    # mueve una posición atras del puntero del stack
    def ptrBackStack(self, indice:str) -> None:
        self.codigo.append(f'SP = SP - {indice};');

    # obtiene un valor dentro del heap
    def getHeap(self, temp:str, i:str) -> None:
        self.codigo.append(f'{temp} = HEAP[(int){i}];');

    # inserta un valor en el heap
    def setHeap(self, i:str, valor:str) -> None:
        self.codigo.append(f'HEAP[(int){i}] = {valor};');

    # obtiene un valor en el stack
    def getStack(self, temp:str, i:str) -> None:
        self.codigo.append(f'{temp} = STACK[(int){i}];');

    # inserta un valor en el stack
    def setStack(self, i:str, valor:str) -> None:
        self.codigo.append(f'STACK[(int){i}] = {valor};');

    # inseta llamada a función
    def callFunc(self, nombre:str) -> None:
        self.codigo.append(f'{nombre}();');

    # añade un if
    def addIf(self, izq:str, der:str, operador:str, etq:str) -> None:
        self.codigo.append(f'if({izq} {operador} {der}) goto {etq};');

    # añade una impresión en C
    def addPrintf(self, tipo:str, valor:str) -> None:
        self.codigo.append(f'printf("%{tipo}", {valor});');
    
    # añade salto de línea
    def newLine(self) -> None:
        self.codigo.append('printf("%c",10);');

    # añade un error semántico
    def errorSem(self, mensaje:str, Lloop:str) -> None:
        self.addEtq(Lloop);
        for m in mensaje:
            self.addPrintf('c', f'(char){ord(m)}');
        self.newLine();

    # añade comentarios
    def addComentario(self, mensaje:str) -> None:
        self.codigo.append(f'/*{mensaje}*/');

    def cambiarCodigo(self, mensaje:str) -> bool:
        for i in range(len(self.codigo)):
            if (self.codigo[i] == '/*-1*/'):
                self.codigo[i] = mensaje;
                return True;
        return False;

    def newFuncion(self, name:str) -> None:
        self.codigo.append(f'void {name} {{');
    
    def cerrarFuncion(self) -> None:
        self.codigo.append('return;\n}');