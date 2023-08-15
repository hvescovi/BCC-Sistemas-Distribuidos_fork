import os

# obter caminho atual
caminho = os.path.dirname(os.path.abspath(__file__))
caminho2 = os.path.join(caminho, 'pasta_sincronizada')

filename = "vai_sumir2.txt"

caminho_completo = os.path.join(caminho2, filename)

print('Removing this file: '+caminho_completo)

try:
    os.remove(caminho_completo)
    print("REMOVIDO!")
except Exception as e:
    print("não foi :-("+str(e))