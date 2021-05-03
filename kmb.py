import socket
import argparse
import logging
import sys
import multiprocessing

max_buf_size = 2048

def run_udp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    logging.info("Socket binded")

    while True:
        _, (cl_host, cl_port) = server_socket.recvfrom(max_buf_size)
        message = (cl_host + ":" + str(cl_port)).encode('utf-8')
        logging.info("There is a new connection with " + message.decode("utf-8"))
        server_socket.sendto(message, (cl_host, cl_port))
        logging.info("Sended message <host:port> to " + message.decode("utf-8"))
        logging.info("Closed connetion with " + message.decode("utf-8"))

def run_tcp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    logging.info("Socket binded")

    server_socket.listen(1)
    while 1:
        connection_socket, (cl_host, cl_port) = server_socket.accept()
        message = (cl_host + ":" + str(cl_port)).encode('utf-8')
        logging.info("There is a new connection with " + message.decode("utf-8"))
        connection_socket.send(message)
        logging.info("Sended message <host:port> to " + message.decode("utf-8"))
        connection_socket.close()
        logging.info("Closed connection with" + message.decode("utf-8"))

def run_udp_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.info("Socket created")

    client_socket.sendto(b"", (host, port))
    logging.info("Sended empty message, socket binded")
    recieved_message, _ = client_socket.recvfrom(max_buf_size)
    logging.info("Recieved message" + recieved_message.decode("utf-8"))
    
    print(recieved_message)
    client_socket.close()
    logging.info("Connection closed")

        
def run_tcp_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info("Socket created")

    client_socket.connect((host,port))
    logging.info("Connected to the server")
    
    client_socket.send(b"")

    recieved_message = client_socket.recv(max_buf_size)
    logging.info("Recieved message" + recieved_message.decode("utf-8"))
    print(recieved_message)

    client_socket.close()
    logging.info("Connection closed")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    ap.add_argument("host", help="Host to connect/listen")
    ap.add_argument("port", help="Port to connect/listen")

    ap.add_argument("-s", action="store_true", help="Run as a server")
    ap.add_argument("-t", action="store_true", required=False, help="Use TCP")
    ap.add_argument("-u", action="store_true", required=False, help="Use UDP")
    ap.add_argument("-o", action="store_true",
                    required=False, help="Logs to STDOUT")
    ap.add_argument("-f", required=False, help="Logs to file given after flag")

    args = vars(ap.parse_args())

    if args["o"] and args["f"]:
        sys.exit()

    if args["t"] and args["u"]:
        sys.exit()

    if args["f"]:
        logging.basicConfig(
            filename=args["f"], encoding='utf-8', level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout,
                            encoding='utf-8', level=logging.DEBUG)

    

    if args["s"]:
        logging.debug("Wow I am server!")

        if args["u"]:
            logging.debug("Nice UDP!")
            p = multiprocessing.Process(
            target=run_udp_server, name="Foo", args=(args["host"], int(args["port"])))
        else:
            logging.info("Awesome TCP!")
            p = multiprocessing.Process(
            target=run_tcp_server, name="Foo", args=(args["host"], int(args["port"])))


    else:
        logging.debug("O_o I am client!")

        if args["u"]:
            logging.debug("Nice UDP!")
            p = multiprocessing.Process(
            target=run_udp_client, name="Foo", args=(args["host"], int(args["port"])))
        else:
            logging.debug("Awesome TCP!")
            p = multiprocessing.Process(
            target=run_tcp_client, name="Foo", args=(args["host"], int(args["port"])))
    
    p.start()
    p.join(10)
    if p.is_alive():
        logging.debug("OwO mom calls to bed, see you guys(((((")

        p.terminate()
        p.join()
