import socket

IP_ADDRESS = "127.0.0.1"

PACKAGE_RECEIVER_UDP_PORT = 9002
SEND_ACK_UDP_PORT = 9003

SIZE_PACKAGE = 1024
    
def main():
    # Configuration
    s = socket.socket()
    s.bind((IP_ADDRESS, PACKAGE_RECEIVER_UDP_PORT))
    s.listen
    
    while True:
        (conn, addr) = s.accept()
        data=conn.recv(SIZE_PACKAGE)
