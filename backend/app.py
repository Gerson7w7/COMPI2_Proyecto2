from flask import Flask, request, jsonify
from flask_cors import CORS

from interprete.extra.Generador import Generador
from interprete.extra.Console import Console
from interprete.extra.Scope import Scope
from interprete.extra.Ast import Ast
from interprete.analizador.parser import parser

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})
console: Console = Console();

@app.route("/")
def hello_world():
    return "HOLAAA"

@app.route('/grammar', methods=['POST'])
def grammar():
    if request.method == 'POST':
        data = request.json
        print(data['data']);
        console.output = ""; console.errores = []; console.simbolos = [];
        generador: Generador = Generador();
        #try:
        ast: Ast = parser.parse(data['data']);
        scope: Scope = Scope(None, 'Global');
        ast.generador = generador;
        ast.ejecutar(console, scope);
        # except Exception as e:
        #     generador.errorSem(e.args[0]);
        #print("soi console: " + generador.getCodigo());
        return {
            'salida': generador.getCodigo()
        }

@app.route('/errores', methods=['GET'])
def errores():
    return jsonify(res = [e.serializar() for e in console.errores]);

@app.route('/simbolos', methods=['GET'])
def simbolos():
    return jsonify(res = [s.serializar() for s in console.simbolos]);

if __name__=='__main__':
    app.run(debug = True, port = 5000)