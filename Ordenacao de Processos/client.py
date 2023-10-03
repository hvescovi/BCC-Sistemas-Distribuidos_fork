import socket
import config
from time import sleep

def run_client():
    # (tempo de realização do evento, destino) 
    events_queue = []

    # Figure 11.6 example - Coulouris, 4ed.
    if config.pid == 1:
        events_queue = [(1, ""), (4, config.ip_list[1]), ()]
    elif config.pid == 2:
        events_queue = [(6, config.ip_list[2])]
    else:
        events_queue = [(2, "")]

    for event in events_queue:
        
        # Travar para acessar seção crítica
        config.lock.acquire()
        config.event_count += 1
        # Destravar seção
        config.lock.release() 
        
        # se o endereço de destino não for vazio
        if(event[1] != ''):
            # envia uma requisição
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Incrementar contador - registrar novo evento
                print(f"Sending a message to {event[1]}")
                s.connect((event[1], config.port))
                s.sendall(str(config.event_count).encode())
        else:
            # Travar para acessar seção crítica
            config.lock.acquire()
            config.event_list.append((f"{config.event_count}.{config.pid}", config.event_count, config.pid))
            # Destravar seção
            config.lock.release()        
        
        # Esperar o tempo de realização do evento
        print(f"Waiting {event[1]} second(s)...")
        sleep(event[0])