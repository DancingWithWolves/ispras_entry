"""Simple client-server module"""

import socket
import argparse
import logging
import sys
import signal

MAX_BUF_SIZE = 2048
is_term_ = False
await_ = False 


def run_udp_server(host, port):
    """Runs UDP server that returns host:port to any client"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    logging.info("Socket binded")

    while True:
        _, (cl_host, cl_port) = server_socket.recvfrom(MAX_BUF_SIZE)
        message = (cl_host + ":" + str(cl_port)).encode('utf-8')
        logging.info("There is a new connection with %s",
                     message.decode("utf-8"))
        server_socket.sendto(message, (cl_host, cl_port))
        logging.info("Sent message <host:port> to %s",
                     message.decode("utf-8"))
        logging.info("Closed connection with %s", message.decode("utf-8"))


def run_tcp_server(host, port):
    """Runs TCP server that returns host:port to any client"""
    global is_term_, await_
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    logging.info("Socket binded")

    server_socket.listen(1)
    while not is_term_:
        await_ = True
        connection_socket, (cl_host, cl_port) = server_socket.accept()
        await_ = False
        message = (cl_host + ":" + str(cl_port)).encode('utf-8')
        logging.info("There is a new connection with %s",
                     message.decode("utf-8"))
        connection_socket.send(message)
        logging.info("Sent message <host:port> to %s",
                     message.decode("utf-8"))
        connection_socket.close()
        logging.info("Closed connection with %s", message.decode("utf-8"))


def run_udp_client(host, port):
    """Runs UDP client that recieves 1 message from server"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.info("Socket created")

    client_socket.sendto(b"", (host, port))
    logging.info("Sended empty message, socket binded")
    recieved_message, _ = client_socket.recvfrom(MAX_BUF_SIZE)
    logging.info("Recieved message %s", recieved_message.decode("utf-8"))

    print(recieved_message)
    client_socket.close()
    logging.info("Connection closed")


def run_tcp_client(host, port):
    """Runs TCP client that recieves 1 message from server"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info("Socket created")

    client_socket.connect((host, port))
    logging.info("Connected to the server")

    client_socket.send(b"")

    recieved_message = client_socket.recv(MAX_BUF_SIZE)
    logging.info("Recieved message %s", recieved_message.decode("utf-8"))
    print(recieved_message.decode("utf-8"))

    client_socket.close()
    logging.info("Connection closed")


def server_stop_sighandler(signal, frame):
    """Function that will be called after exact signals. Stops the server"""
    global is_term_, await_
    logging.debug("Sigint called")
    is_term_ = True
    if await_:
        sys.exit(0)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, server_stop_sighandler)

    AP = argparse.ArgumentParser()

    AP.add_argument("host", help="Host to connect/listen")
    AP.add_argument("port", help="Port to connect/listen")

    AP.add_argument("-s", action="store_true", help="Run as a server")

    EXCLUSIVE_ARGS_PROTOCOL = AP.add_mutually_exclusive_group()
    EXCLUSIVE_ARGS_PROTOCOL.add_argument("-t", action="store_true", required=False, help="Use TCP")
    EXCLUSIVE_ARGS_PROTOCOL.add_argument("-u", action="store_true", required=False, help="Use UDP")


    EXCLUSIVE_ARGS_LOGOUT = AP.add_mutually_exclusive_group()
    EXCLUSIVE_ARGS_LOGOUT.add_argument("-o", action="store_true",
                    required=False, help="Logs to STDOUT")
    EXCLUSIVE_ARGS_LOGOUT.add_argument("-f", required=False, help="Logs to file given after flag")

    ARGS = vars(AP.parse_args())


    if ARGS["f"]:
        logging.basicConfig(filename=ARGS["f"], level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    if ARGS["s"]:
        logging.debug("Wow I am server!")

        if ARGS["u"]:
            logging.debug("Nice UDP!")
            
            run_udp_server(ARGS["host"], int(ARGS["port"]))
        else:
            logging.debug("Awesome TCP!")
            run_tcp_server(ARGS["host"], int(ARGS["port"]))

    else:
        logging.debug("O_o I am client!")

        if ARGS["u"]:
            logging.debug("Nice UDP!")
            run_udp_client(ARGS["host"], int(ARGS["port"]))
        else:
            logging.debug("Awesome TCP!")
            run_tcp_client(ARGS["host"], int(ARGS["port"]))



