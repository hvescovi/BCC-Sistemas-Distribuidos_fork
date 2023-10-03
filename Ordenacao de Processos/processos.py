from config import *
from time import sleep
from client import *
from server import *
import  threading
import sys

if(len(sys.argv) != 2):
    print("Execute o programa informando o número do processo (1, 2 ou 3)")
    exit(0)
if(sys.argv[1] != "1" and sys.argv[1] != "2" and sys.argv[1] != "3"):
    print("O nome do programa deve ser \'1\', \'2\' ou \'3\'")
    exit(0)

config.pid = int(sys.argv[1])

client_thread = threading.Thread(target=run_client)
server_thread = threading.Thread(target=run_server)

client_thread.start()
server_thread.start()


