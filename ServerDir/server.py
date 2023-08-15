# importar a biblioteca flask
from flask import Flask, jsonify
# biblioteca CORS
from flask_cors import CORS

import time

import os


class File:
    # construtor com valor padrão nos parâmetros
    def __init__(self, name="", id="", modified=""):
        self.name = name
        self.id = id
        self.modified = modified

    # expressar a classe em formato texto
    def __str__(self):
        return f'{self.name}, '+\
               f'{self.id}, {self.modified}'

    # expressar a classe em formato json
    def json(self):
        return {
            "name" : self.name,
            "id" : self.id,
            "modified" : self.modified 
        }

# acesso ao flask via variável app
app = Flask(__name__)

# inserindo a aplicação em um contexto
# https://flask.palletsprojects.com/en/2.2.x/appcontext
with app.app_context():

    # aplicando tratamento CORS ao flask
    # https://flask-cors.readthedocs.io/en/latest/
    CORS(app)

    # rota padrão
    @app.route("/")
    def ola():
        return "<b>Olá, gente!</b>"

    # rota de listar pessoas
    @app.route("/listar")
    def listar():
        try:
            # cria a lista de retorno que sera usadada para gerar o json
            lista_retorno = []
            # obtem lista dos arquivos do diretŕio atual
            dirEntrys = os.scandir(".")
            lista = []
            # percorre a lista de entradas
            for entry in dirEntrys:
                if entry.is_file() and entry.name != "server.py":
                    # obtem status referente ao arquivo e grava na lista
                    fileStatus = entry.stat()
                    file = File(entry.name, fileStatus.st_ino, fileStatus.st_mtime)
                    print(file)
                    lista.append(file)


            # percorrer a lista de arquivos e tranforma em json
            for file in lista:
                lista_retorno.append(file.json())

            # preparar uma parte da resposta: resultado ok
            meujson = {"header":"OK"}

            meujson.update({"files":lista_retorno})

            # retornar a lista de pessoas json, com resultado ok
            resposta = meujson

            # trate corretamente esse erro
        except Exception as e: 
            resposta = jsonify({"header": "erro", "files": str(e)})

        return resposta

    @app.route("/criar/<file_name>")
    def criar(file_name):
        try:
            newFile = open("./" + file_name, "x")
            newFile.close()
            entry = os.stat("./" + file_name)
            file = File(file_name, entry.st_ino, entry.st_mtime)
            resposta = jsonify({"header": "OK", "file": file.json()})
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e)})

        return resposta

    @app.route("/deletar/<file_name>")
    def deletar(file_name):
        try:
            os.remove("./" + file_name)
            resposta = jsonify({"header": "OK", "deatil": file_name + ' deleted'})
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e)})

        return resposta

    @app.route("/escrever/<file_name>/<conteudo>")
    def escrever(file_name, conteudo):
        try:
            openedFile = open("./" + file_name, "w")
            openedFile.write(conteudo)
            openedFile.close()
            print(conteudo)
            resposta = jsonify({"header": "OK", "detail": "success!"})
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e)})
        return resposta

    @app.route("/ler/<file_name>")
    def ler(file_name):
        try:
            openedFile = open("./" + file_name, "r")
            conteudo = openedFile.read()
            openedFile.close()
            resposta = jsonify({"header": "OK", "detail": conteudo})
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e)})
        return resposta

    app.run(debug=True)
    # para depurar a aplicação web no VSCode, é preciso remover debug=True
    # https://stackoverflow.com/questions/17309889/how-to-debug-a-flask-app


'''
resultado da invocação ao servidor:

curl localhost:5000/listar


'''
