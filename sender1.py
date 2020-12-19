import signal
import sys
import socket
import argparse
import time
import threading
import random
import logging

from queue import Queue

IP_ADDRESS = "127.0.0.1"

SENDER_RX_UDP_PORT   = 9001
SENDER_TX_UDP_PORT   = 9002
RECEIVER_RX_UDP_PORT = 9003
RECEIVER_TX_UDP_PORT = 9004

SOCKET_TIMEOUT = 0.001
LOOP_TIMEOUT   = 0.0001

BUFFER_LENGTH = 1024

def create_package():
    
    
#ACABAR -> DEFAULTS
def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Package shipping process and ACK receipt process.')
    
    #Add parser parameters #PONER DAFAULTS
    parser.add_argument('shipping_rate', type=float, nargs="?", help="Data delivery rate in bits per second")
    parser.add_argument('package_size', type=int, nargs="?", default=BUFFER_LENGTH, help="Package size in bytes (maximum = 1024)")
    parser.add_argument('package_number', type=int, nargs="?", help="Number of data package to send")

    # Parse the program input arguments
    args = parser.parse_args()
    
    return args

def main():

    # Parse input arguments
    args = parse_arguments()
    # HAY QUE MIRAR COMO SE LE CAMBIAN LOS VALORES DE ENTRADA ¿¿??

    # Create package to send
    
