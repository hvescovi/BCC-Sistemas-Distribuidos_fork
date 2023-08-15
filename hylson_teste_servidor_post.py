from flask import Flask, jsonify
app = Flask(__name__)

# rota padrão
@app.route("/")
def ola():
    return "The file server is on"

@app.route("/gravar", methods=['post'])
def gravar():
    
    retorno = {
        "files":[
            {"name":"teste.txt"},
            {"name":"teste2.txt"}
        ]
    }
    return jsonify(retorno)

app.run(debug=True, host="0.0.0.0", port=4999)

