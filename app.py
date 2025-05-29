from flask import Flask, request, jsonify
from RPA_INICIAL import executar_automacao  # importa sua função

app = Flask(__name__)

@app.route('/executar-rpa', methods=['POST'])
def executar():
    dados = request.json  # dados enviados pelo front
    resultado = executar_automacao(dados)  # agora sua função aceita os dados
    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(debug=True)
