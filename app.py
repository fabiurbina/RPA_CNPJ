from flask import Flask, request, jsonify
from RPA_INICIAL import executar_automacao  # importa sua função
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'API do RPA CNPJ no ar! Use POST em /executar-rpa.'

@app.route('/executar-rpa', methods=['POST'])
def executar():
    dados = request.json  # dados enviados pelo front
    resultado = executar_automacao(dados)
    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
