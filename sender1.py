import argparse
import socket
import sys

IP_ADDRESS = "127.0.0.1"

SEND_PACKAGE_UDP_PORT = 9001 # PUERTO DONDE ENVIAMOS LOS DATOS 
ACK_RECEIVER_UDP_PORT = 9004 # PUERTO DONDE RECIBIMOS EL ACK

PACKAGE_SIZE = 1024


def parse_arguments(): # INICIALIZAMOS LAS VARIABLES PARA LOS DATOS QUE EVIAMOS 

    # Create argument parser
    parser = argparse.ArgumentParser(description='Package shipping process and ACK receipt process.')
    
    # Add parser parameters #PONER DEFAULTS
    parser.add_argument('shipping_rate', type=float, nargs="?", help="Data delivery rate in bits per second") #TAXA D'ENVIAMENT
    parser.add_argument('package_size', type=int, nargs="?", default=BUFFER_LENGTH, help="Package size in bytes (maximum = 1024)") #MIDA DELS PAQUETS DE DADES EN BITS 
    parser.add_argument('package_number', type=int, nargs="?", default=1, help="Number of data package to send") #n total de paquets de dades enviar abans de finalitzar l’execució

    # Parse the program input arguments
    args = parser.parse_args()
    
    return args

def create_package(): # CREAMOS EL PAQUETE, LE PONEMOS LOS DATOS 
    args = parse_arguments()


def main():

    data = create_package() # CREATE PACKAGE 

    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((IP_ADDRESS, PACKAGE_RECEIVER_UDP_PORT))

 
    



def main():
    # Configuration
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((IP_ADDRESS, PACKAGE_RECEIVER_UDP_PORT))
    
    while True:
        # Send package
        s.sendto(data, (IP_ADDRESS, SEND_PACKAGE_UDP_PORT))  

        #WAIT

        # Receive ACK 
        ack_data, addr = s.recvfrom(PACKAGE_SIZE)

