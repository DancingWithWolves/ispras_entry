from socket import *
import argparse
import logging
import sys
import multiprocessing
import time

def RunServer (host, port):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind((host, port))
    logging.info("The server is ready to receive")

    while True:
        message, client_address = server_socket.recvfrom(2048)
        server_socket.sendto(client_address[0], client_address)

if __name__ == '__main__' :
    ap = argparse.ArgumentParser()

    ap.add_argument("host", help="Host to connect/listen")
    ap.add_argument("port", help="Port to connect/listen")

    ap.add_argument("-s", action="store_true", help="Run as a server")
    ap.add_argument("-t", action="store_true", required=False, help="Use TCP")
    ap.add_argument("-u", action="store_true", required=False, help="Use UDP")
    ap.add_argument("-o", action="store_true", required=False, help="Logs to STDOUT")
    ap.add_argument("-f", required=False, help="Logs to file given after flag")

    args = vars(ap.parse_args())

    if args["o"] and args["f"]:
        exit()

    if args["t"] and args["u"]:
        exit()

    if (args["f"]):
        logging.basicConfig(filename=args["f"], encoding='utf-8', level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, encoding='utf-8', level=logging.DEBUG)


    if (args["u"] == 1):
        logging.info("Nice UDP!")
    else:
        logging.info("Awesome TCP!")

    if (args["s"]):
        logging.info("Wow I am server!")

        p = multiprocessing.Process(target=RunServer, name="Foo", args=(args["host"], int(args["port"])))
        p.start()
        p.join(10)

        if p.is_alive():
            logging.warning("OwO nobody came to a party(((((")

            p.terminate()
            p.join()
        
    else:
        logging.info("OwO I am client!")

        serverName = '127.0.0.1'
        serverPort = 5312
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        message = input('Input lowercase sentence:').encode('utf-8')
        clientSocket.sendto(message, (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        logging.info(modifiedMessage)
        clientSocket.close()
