import requests

'''
resposta esperada do get:
{
  "files": [
    {
      "name": "teste.txt"
    },
    {
      "name": "teste2.txt"
    }
  ]
}
'''

resp = requests.get('http://191.52.7.27:4999/listar')
# ler a resposta em formato json
y = resp.json()

print(y)
# percorre o atributo json chamado "files"
for x in y['files']:
    print(x)
    print(x['name'])