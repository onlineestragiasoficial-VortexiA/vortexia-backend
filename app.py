from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "API Vortexia rodando 🚀"

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        "status": "ok",
        "mensagem": "API funcionando!"
    })

@app.route('/api/enviar', methods=['POST'])
def enviar():
    data = request.json

    return jsonify({
        "status": "sucesso",
        "dados_recebidos": data
    })

if __name__ == '__main__':
    app.run(debug=True)
