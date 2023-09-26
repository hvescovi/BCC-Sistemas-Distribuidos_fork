import socket
import struct
import json
import os
from threading import Event

ADDR = '224.3.29.71'
PORT = 10000
CLIENT_DIR = "client_files/"

class Client:

    def __init__(self, addr_group, port, client_dir):
        self.multicast_group = (addr_group, port)
        self.client_dir = client_dir

    def run(self) -> None:
        
        if not os.path.exists(self.client_dir):
            os.mkdir(self.client_dir)
        
        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block indefinitely when trying
        # to receive data.
        sock.settimeout(0.5)

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        while True:
            try:
                message = input("--> File: ")
                
                # Send data to the multicast group
                #print (sys.stderr, 'sending "%s"' % message)
                #print ('sending "%s"' % message)
                
                data = '{"fileName": "' +  message + '"}'
                sent = sock.sendto(data.encode(), self.multicast_group)

                # Look for responses from all recipients
                while True:
                    #print (sys.stderr, 'waiting to receive')
                    print('--> waiting to receive')
                    try:
                        data, server = sock.recvfrom(1024)

                    except socket.timeout:
                        #print (sys.stderr, 'timed out, no more responses')
                        print('--> timed out, no more responses :(')
                        break
                    else:
                        parsed_data = json.loads(data.decode()) 
                        #print (sys.stderr, 'received "%s" from %s' % (data, server))
                        print('--> received from %s', server)
                        
                        with open(os.path.join(self.client_dir, message), 'w') as file:
                            file.write(parsed_data['detail'])
                        
                        break
            finally:
                pass
                #print (sys.stderr, 'closing socket')
                #print ('closing socket')
                #sock.close()
