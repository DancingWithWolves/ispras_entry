import socket
import argparse
import logging
import sys
import multiprocessing

def run_udp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print("The server is ready to receive")

    while True:
        _, (cl_host, cl_port) = server_socket.recvfrom(2048)
        print(cl_host + ":" + str(cl_port))
        server_socket.sendto((cl_host + ":" + str(cl_port)).encode('utf-8') , (cl_host, cl_port))

def run_udp_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.sendto(b"UwU", (host, port))
    modified_message, _ = client_socket.recvfrom(2048)

    logging.info(modified_message)
    client_socket.close()


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

    if args["u"] == 1:
        logging.info("Nice UDP!")
    else:
        logging.info("Awesome TCP!")

    if args["s"]:
        logging.info("Wow I am server!")

        p = multiprocessing.Process(
            target=run_udp_server, name="Foo", args=(args["host"], int(args["port"])))
        p.start()
        p.join(10)

        if p.is_alive():
            logging.warning("OwO nobody came to a party(((((")

            p.terminate()
            p.join()

    else:
        logging.info("OwO I am client!")
        run_udp_client(args["host"], int(args["port"]))
