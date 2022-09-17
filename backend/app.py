from flask import Flask, request, jsonify
from flask_cors import CORS

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
        try:
            ast: Ast = parser.parse(data['data']);
            scope: Scope = Scope(None, 'Global');
            # limpiamos la consola de salida
            ast.ejecutar(console, scope);
        except Exception as e:
            console.append(e.args[0]);
        print("soi console: " + console.output);
        return {
            'salida': console.output
        }

@app.route('/errores', methods=['GET'])
def errores():
    return jsonify(res = [e.serializar() for e in console.errores]);

@app.route('/simbolos', methods=['GET'])
def simbolos():
    return jsonify(res = [s.serializar() for s in console.simbolos]);

if __name__=='__main__':
    app.run(debug = True, port = 5000)