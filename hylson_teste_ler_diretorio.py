import os

# obter caminho atual
caminho = os.path.dirname(os.path.abspath(__file__))
caminho2 = os.path.join(caminho, 'pasta_sincronizada')

print('Starting folder reading:'+caminho2)

# percorrer diretório
for dentry in os.scandir(caminho2):

    t = type(dentry) # tipo do arquivo
    n = dentry.name # nome do arquivo

    print(f'{t}, {n} is biiiig')