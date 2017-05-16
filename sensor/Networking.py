# TCP client example
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def open_connection(ip, port):
    client_socket.connect((ip, port))


def send(string):
    data = input(string)
    client_socket.send(data)


def close_connection():
    client_socket.close()

