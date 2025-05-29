from flask import Flask, jsonify, render_template_string, request
from RPA_INICIAL import executar_automacao

app = Flask(__name__)

FORM_HTML = """
<!DOCTYPE html>
<html>
  <head><title>Rodar RPA CNPJ</title></head>
  <body>
    <h2>Clique no botão para rodar o RPA</h2>
    <form method="post">
      <button type="submit">Rodar</button>
    </form>
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resultado = executar_automacao()  # roda o RPA
        return jsonify({"resultado": resultado})
    return render_template_string(FORM_HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
