from flask import Flask, request, jsonify
from RPA_INICIAL import executar_automacao

app = Flask(__name__)

@app.route('/')
def home():
    return "API do RPA CNPJ no ar! Use POST em /executar-rpa."

@app.route('/executar-rpa', methods=['POST'])
def executar():
    dados = request.get_json()
    resultado = executar_automacao(dados)  # aqui roda seu Selenium
    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
