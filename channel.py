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

finished = False

# Receives the data from the transmitter and puts it on a queue
def rx_function(args=None):
    global finished

    # Get the values passed as parameters
    thread_name = args[0] # The name of the thread
    udp_port    = args[1] # The UDP port to send the packets to
    queue       = args[2] # A reference to the queue to receive packets from

    logging.debug(thread_name + ": starting")
    logging.debug(thread_name + ": receiving on port={} using queue={}".format(udp_port, queue))

    # Create UDP socket to receive packets from
    # The socket is non-blocking to allow other actions
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((IP_ADDRESS, udp_port))
    udp_socket.settimeout(SOCKET_TIMEOUT)

    # Execute while the program is stopped
    while not finished:
        try:
            # Get a data packet from the UDP socket
            data, addr = udp_socket.recvfrom(BUFFER_LENGTH)
            logging.debug(thread_name + ": recvfrom")
            try:
                # Try to put the data packet to the queue
                # The operation is non-blocking, so if the queue is full the packet is dropped
                queue.put_nowait(data)
                logging.debug(thread_name + ": put_nowait")
            except:
                logging.debug(thread_name + ": packet dropped!")
        except:
            pass

    logging.debug(thread_name + ": finishing")

# Gets the data from the receive queue and transmits it to the receiver
def tx_function(args=None):
    global finished

    # Get the values passed as parameters
    thread_name      = args[0] # The name of the thread
    udp_port         = args[1] # The UDP port to send the packets to
    queue            = args[2] # A reference to the queue to receive packets from
    delay            = args[3] # The delay for each packet to send
    drop_probability = args[4] # The probability of dropping a packet

    logging.debug(thread_name + ": starting")
    logging.debug(thread_name + ": transmitting on port={} using queue={}".format(udp_port, queue))

    # Create UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Execute while the program is stopped
    while not finished:
        # Record the start time of the loop
        start_time = time.time()

        # Initialize the data variable
        data = None

        try:
            # Try to get an element from the queue
            # The operation is non-blocking, so if the queue is empty the call returns immediately
            data = queue.get_nowait()
            logging.debug(thread_name + ": get_nowait")
        except:
            pass

        # If we got a packet from the queue, process it now
        if (data is not None):
            # Get length of data
            data_length = len(data)
            logging.debug(thread_name + ": data length = {}".format(data_length))

            # Generate a probability of dropping the packet by sampling from a uniform distribution
            random_value = int(100 * random.random())
            logging.debug(thread_name + ": random_value = {}".format(random_value))

            # If the value is larger than the target probability, the packet is lost
            if (random_value < drop_probability):
                logging.debug(thread_name + ": packet discarded")
            else:
                # Wait to transmit the packet
                time.sleep(delay)

                # Transmit the data packet using the UDP socket
                udp_socket.sendto(data, (IP_ADDRESS, udp_port))
                logging.debug(thread_name + ": sendto to port {}".format(udp_port))        

        # Finished executing the loop 
        end_time = time.time()

        # Calculate time elapsed in the loop
        elapsed_time = end_time - start_time

        # Small loop delay
        time.sleep(LOOP_TIMEOUT)

    logging.debug(thread_name + ": finishing")


def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Simulates delay and packet loss in the channel between the transmitter and receiver.')

    # Add parser parameters
    parser.add_argument('--up_delay', type=int, nargs="?", default=10, help="Uplink (sender to receiver) delay in milliseconds.")
    parser.add_argument('--down_delay', type=int, nargs="?", default=10, help="Downlink (receiver to sender) delay in milliseconds.")
    parser.add_argument('--up_loss', type=int, nargs="?", default=0, help="Uplink (sender to receiver) packet loss in percentage.")
    parser.add_argument('--down_loss', type=int, nargs="?", default=0, help="Downlink (receiver to sender) packet loss in percentage.")
    parser.add_argument('--up_queue', type=int, nargs="?", default=1, help="Uplink (sender to receiver) queue length in packets.")
    parser.add_argument('--down_queue', type=int, nargs="?", default=1, help="Downlink (receiver to sender) queue length in packets.")
    parser.add_argument('--random', type=bool, nargs="?", default=False, help="Determines if the simulation is random or deterministic.")

    # Parse the program input arguments
    args = parser.parse_args()

    return args


def signal_handler(sig, frame):
    global finished
    finished = True

def main():
    global finished

    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')

    # Parse input arguments
    args = parse_arguments()

    # Initilize the random number generator
    if (args.random is True):
        random.seed(time.time())
    else:
        random.seed(0)

    # Get the values passed as parameters
    up_queue_length   = args.up_queue          # Uplink queue length
    down_queue_length = args.down_queue        # Downlink queue length
    up_delay          = args.up_delay / 1000   # Uplink delay in milliseconds
    up_loss           = args.up_loss           # Uplink packet loss probability
    down_delay        = args.down_delay / 1000 # Downlink delay in milliseconds
    down_loss         = args.down_loss         # Downlink packet loss probability

    # Queues to stor the data packets
    sender_to_receiver_queue = Queue(maxsize=up_queue_length)
    receiver_to_sender_queue = Queue(maxsize=down_queue_length)

    # List to hold threads
    threads = []

    # Start the sender RX thread
    sender_rx_thread = threading.Thread(target=rx_function, args=(["sender_rx", SENDER_RX_UDP_PORT, sender_to_receiver_queue],))
    threads.append(sender_rx_thread)

    # Start the sender TX thread
    sender_tx_thread = threading.Thread(target=tx_function, args=(["sender_tx", SENDER_TX_UDP_PORT, sender_to_receiver_queue, up_delay, up_loss],))
    threads.append(sender_tx_thread)

    # Start the receiver RX thread
    receiver_rx_thread = threading.Thread(target=rx_function, args=(["receiver_rx", RECEIVER_RX_UDP_PORT, receiver_to_sender_queue],))
    threads.append(receiver_rx_thread)

    # Start the receiver TX thread
    receiver_tx_thread = threading.Thread(target=tx_function, args=(["receiver_tx", RECEIVER_TX_UDP_PORT, receiver_to_sender_queue, down_delay, down_loss],))
    threads.append(receiver_tx_thread)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for the simulation to finish, threads execute in parallel
    while (not finished):
        time.sleep(0.1)

    # Wait for threads to finish
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
