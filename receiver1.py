import socket

IP_ADDRESS = "127.0.0.1" 

PACKAGE_RECEIVER_UDP_PORT = 9002 #PUERTO DONDE RECIBIMOS LOS DATOS 
SEND_ACK_UDP_PORT = 9003 #PUERTO DONDE ENVIAMOS EL ACK

PACKAGE_SIZE = 1024
    
def main():
    # Configuration
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_socket.bind((IP_ADDRESS, PACKAGE_RECEIVER_UDP_PORT))
    
    while True:
        # Receive package 
        data, addr = udp_socket.recvfrom(PACKAGE_SIZE)
        print("Package received. Data length = {}".format(len(data)))
        #.format()
        #print(data)
        
        # Send ACK
        udp_socket.sendto(data, (IP_ADDRESS, SEND_ACK_UDP_PORT))
        print("ACK sended.") 

main()