# !/usr/bin/env python3
# server.py is responsible for starting the server and handling incoming connections.
import socket
import threading
from websocket_handler import handle_client_connection
from init_db import init_db
import argparse

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Servidor escutando em {host}:{port}")
    
    while True:
        client_socket, _ = server_socket.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, port))
        client_thread.start()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Inicia o servidor na porta e host especificados.')
    parser.add_argument('--host', type=str, default='localhost', help='Host onde o servidor será iniciado. Padrão é "localhost".')
    parser.add_argument('--port', type=int, default=8080, help='Porta na qual o servidor escutará. Padrão é 8080.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    init_db()
    HOST, PORT = args.host, args.port
    start_server(HOST, PORT)