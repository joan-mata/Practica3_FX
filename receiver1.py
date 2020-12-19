import socket

IP_ADDRESS = "127.0.0.1" 

PACKAGE_RECEIVER_UDP_PORT = 9002 #PUERTO DONDE RECIBIMOS LOS DATOS 
SEND_ACK_UDP_PORT = 9003 #PUERTO DONDE ENVIAMOS EL ACK

PACKAGE_SIZE = 1024
    
def main():
    # Configuration
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((IP_ADDRESS, PACKAGE_RECEIVER_UDP_PORT))
    
    while True:
        # Receive package 
        data, addr = s.recvfrom(PACKAGE_SIZE)

        # Send ACK
        s.sendto(data, (addr, SEND_ACK_UDP_PORT))  