import os

# obter caminho atual
caminho = os.path.dirname(os.path.abspath(__file__))
caminho2 = os.path.join(caminho, 'pasta_sincronizada')

filename = "conteudo_sobreescrito.txt"

caminho_completo = os.path.join(caminho2, filename)

print('Escrevendo dados neste arquivo: '+caminho_completo)

dados = "este será o conteúdo do novo arquivo"

try:
    f = open(caminho_completo, "w")
    f.write(dados)
    f.close()
    print("arquivo escrito!")
except Exception as e:
    print("não foi :-("+str(e))