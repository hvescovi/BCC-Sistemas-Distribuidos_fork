import os

# obter caminho atual
caminho = os.path.dirname(os.path.abspath(__file__))
caminho2 = os.path.join(caminho, 'pasta_sincronizada')

filename = "arquivo1.txt"

caminho_completo = os.path.join(caminho2, filename)

print('Lendo dados deste arquivo: '+caminho_completo)

try:
    f = open(caminho_completo, "r")
    conteudo = f.read()
    f.close()
    print("arquivo lido!")
    print(conteudo)
except Exception as e:
    print("não foi :-("+str(e))