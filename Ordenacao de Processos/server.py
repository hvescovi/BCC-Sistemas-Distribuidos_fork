# funcao que fica recebendo:
import socket
import config

def run_server():        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # IP da pŕopria maquina
        s.bind((config.ip_list[config.pid-1], config.port))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)

                    if not data:
                        break
                    else:
                        #converte para inteiro, o valor do cont recebido
                        time_received = int(data.decode('utf-8'))
                        print(f"Evento recebido no tempo : {time_received}")
                        # Seção Crítica - INICIO
                        config.lock.acquire()
                        # o contador atual recebe o valor maximo entre si e o recebido
                        config.event_count = max(config.event_count, time_received)
                        # incrementa o contador por ser um novo evento
                        config.event_count = config.event_count + 1
                        # adiciona o evento a sua lista
                        config.event_list.append((f"{config.event_count}.{config.pid}", config.event_count, config.pid))    
                        # Seção Crítica - FIM 
                        config.lock.release()
