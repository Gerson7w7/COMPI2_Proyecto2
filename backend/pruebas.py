from interprete.extra.Console import Console
from interprete.extra.Scope import Scope
from interprete.extra.Ast import Ast
from interprete.analizador.parser import parser

prueba = 'let xdsaf : i64 = 5+5;';
resultado: Ast = parser.parse(prueba);

scope: Scope = Scope(None)
console: Console = Console();

resultado.ejecutar(console, scope)