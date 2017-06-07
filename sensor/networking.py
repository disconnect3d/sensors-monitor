import json
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def open_connection(ip, port):
    global client_socket
    # close_connection()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((ip, port))


def send(string):
    global client_socket
    data = string.encode()
    client_socket.sendall(data)


def recv():
    global client_socket
    data = client_socket.recv(1024)
    print('Received: ', data)
    return json.loads(data.decode('utf8'))


def close_connection():
    global client_socket
    client_socket.shutdown(1)
