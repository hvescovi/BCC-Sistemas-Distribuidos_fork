import requests
import json
import os

SERVER_ADDR = "http://localhost:5000"
FILE_DIR = "./files"

class File:
    # construtor com valor padrão nos parâmetros
    def __init__(self, nome="", id="", modified=""):
        self.nome = nome
        self.id = id
        self.modified = modified

    # expressar a classe em formato texto
    def __str__(self):
        return f'{self.nome}, '+\
               f'{self.id}, {self.modified}'

    # expressar a classe em formato json
    def json(self):
        return {
            "nome" : self.nome,
            "id" : self.id,
            "modified" : self.modified 
        }

class Client:

    def __init__(self, server_addr=SERVER_ADDR, file_dir=FILE_DIR):
        self.server_addr = server_addr
        self.file_dir = file_dir

    def list_server_files(self, verbose=False):
        response = requests.get(f'{self.server_addr}/listar').json()

        if verbose:
            for n in response['files']:
                print(n['name'])

        return response

    def list_local_files(self, verbose=False):
        files = []
        json_files = []

        dirEntrys = os.scandir(self.file_dir)
        
        for entry in dirEntrys:
            if entry.is_file() and entry.name != "client.py":
                file = File(entry.name, entry.stat().st_ino, entry.stat().st_mtime)
                #print(file)
                files.append(file)

        for file in files:
            json_files.append(file.json())

        if verbose:
            print(json_files)

        return json_files

    def create_file(self, file_name):
        response = requests.get(f'{self.server_addr}/criar/{file_name}').json()

        if response['header'] == "OK":
            f = open(f"{self.file_dir}/{file_name}", "x")
            f.close()
            return True

        return False

    def delete_file(self, file_name):
        response = requests.get(f'{self.server_addr}/deletar/{file_name}').json()
        
        if response['header'] == "OK":
            os.remove(f"{self.file_dir}/{file_name}")
            return True
    
        return False

    def write_to_file(self, file_name, content):
        response = requests.get(f'{self.server_addr}/escrever/{file_name}/{content}').json()
        
        if response['header'] == "OK":
            f = open(f"{self.file_dir}/{file_name}", "w")
            f.write(content)
            f.close()
            return True
    
        return False

    def read_from_file(self, file_name):
        response = requests.get(f'{self.server_addr}/ler/{file_name}').json()
        
        if response['header'] == "OK":
            #print(type(response['detail']))
            return response['detail']
    
        return None

    def update_local_files(self):
        pass

    def install(self):

        # get the servers folder files list
        
        # create locally all files recovered from the server
        pass

    def merge(self):

        # get the servers folder files list

        # load the list of local files, in the FILE_DIR folder      

        # Compares and find the difference from the two dicts  
        # example of comparison results:
        # [('local_remove','praia.png'), 
        # ('remote_create','texto.txt'), 
        # ('remote_write','texto.txt','este-e-o-conteudo-d)]

        pass

    # Tmp methods
    def dump(self):
        server_files = self.list_server_files()
        
        for file in server_files['files']:
            f = open(f"{self.file_dir}/{file['name']}", "w")
            f.close()


def test():
    client_1 = Client()
    file_name = "newFileFromClient.txt"
    content_to_write = "conteudo-para-teste-de-escrita"

    print("Initial files:")
    client_1.list_server_files(verbose=True)
    #client_1.dump()
    
    print(f"*** Creating file {file_name}")
    client_1.create_file(file_name)

    print("*** The file was created?")
    client_1.list_server_files(verbose=True)
    
    print(f"*** Writing {content_to_write} to {file_name}")
    if client_1.write_to_file(file_name, content_to_write):
        print("Success in writing")
    else:
        print("I could not write :-(")
    
    print("The content was written? Testing file reading...")
    content2 = client_1.read_from_file(file_name)
    print(f"Content read from {file_name}: {content2}")

    print(f"Removing file {file_name}")
    client_1.delete_file(file_name)

    print("Final listing")
    client_1.list_server_files(verbose=True)
    
    #client_1.dump()

# client paratemers for execution:
# install - load all files from server
# merge - compare files between client and server, and do the actions required to make them equals

if __name__ == "__main__":
    test()