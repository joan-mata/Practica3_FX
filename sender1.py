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

def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Package shipping process and ACK receipt process.')
    
    #Add parser parameters
    parser.add_argument('--shipping_rate', type=float, nargs="?", help="Data delivery rate in bits per second")
    parser.add_argument('--')
    parser.add_argument('--')

    # Parse the program input arguments
    args = parser.parse_args()
    
    return args

def main():
    
