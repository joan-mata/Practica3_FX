import argparse
import socket
import sys
import random
import os
import time
import datetime

IP_ADDRESS = "127.0.0.1"

SEND_PACKAGE_UDP_PORT = 9001 # PUERTO DONDE ENVIAMOS LOS DATOS 
ACK_RECEIVER_UDP_PORT = 9004 # PUERTO DONDE RECIBIMOS EL ACK

PACKAGE_SIZE = 1024


def parse_arguments(): # INICIALIZAMOS LAS VARIABLES PARA LOS DATOS QUE EVIAMOS 

    # Create argument parser
    parser = argparse.ArgumentParser(description='Package shipping process and ACK receipt process.')
    
    # Add parser parameters #PONER DEFAULTS
    parser.add_argument('shipping_rate', type=float, nargs="?", help="Data delivery rate in bits per second") #TAXA D'ENVIAMENT
    parser.add_argument('package_size', type=int, nargs="?", default=PACKAGE_SIZE, help="Package size in bytes (maximum = 1024)") #MIDA DELS PAQUETS DE DADES EN BITS 
    parser.add_argument('package_number', type=int, nargs="?", default=1, help="Number of data package to send") #n total de paquets de dades enviar abans de finalitzar l’execució

    # Parse the program input arguments
    args = parser.parse_args()
    
    return args




def main():
    # Parse input arguments
    args = parse_arguments()

    # Get the values passed as parameters
    shipping_rate   = args.shipping_rate
    package_size    = args.package_size
    package_number  = args.package_number

    # Input values
    print("Enter the shipping rate (bits per second):")
    shipping_rate = float(input())
    
    print("Enter the data package size (Maximum 1024 bytes):")
    package_size = int(input())
    while package_size > 1024 or package_size <= 0:
        print("Enter the data package size (Maximum 1024 bytes):")
        package_size = int(input())

    print("Enter the number of data packages:")  
    package_number = int(input())

    # Create data package through input data
    #data = 'A' * (package_size - 49)
    data = os.urandom(package_size)

    # Create socket
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_socket.bind((IP_ADDRESS, ACK_RECEIVER_UDP_PORT)) #port 9004

    counter = 0
    wait_time = (package_size * 8) / shipping_rate
    
    print('')
    print('Starting...')

    send_time = datetime.datetime.now() 

    while counter < package_number:
        # Send package
        udp_socket.sendto(data, (IP_ADDRESS, SEND_PACKAGE_UDP_PORT)) #port 9001
        print("Package sended: data length = {}".format(len(data)))

        #WAIT
        time.sleep(wait_time)

        # Receive ACK 
        ack_data, addr = udp_socket.recvfrom(PACKAGE_SIZE)
        print("ACK received")

        counter += 1

    print('Finished.')
    print('')
    print('Results:')
    
    received_time = datetime.datetime.now() 
    total_time = (received_time - send_time).total_seconds()
    total_bits = package_size * 8 * package_number
    effective_rate = total_bits / total_time
    link_use = effective_rate / shipping_rate * 100

    print("Total time: {} [seconds]".format(total_time))
    print("Effective rate: {} [bits per seconds]".format(effective_rate))
    print("Use of the link: {} [%]".format(link_use))

    
main()
 