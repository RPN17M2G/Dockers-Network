import socket
from node.rscs import calc_worst_system_resource
from fastapi import FastAPI
from _thread import *
from scapy import *

SERVER_IP = "172.20.0.2"
SERVER_PORT = 9898

# Required to connect to the uvicorn server and perform debug
try:
    app = FastAPI()
    @app.get("/")
    def read_root():
        pass
except:
    pass


def connect_to(ip, port):
    '''
    Input: src_ip, src_port, dst_ip, dst_port
    Output: none
    Trying to coonect to a specific machine via socket
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting to connect")
    try:
        sock.connect((ip, port))
        print("Connection to server complete.")

        pac = getPacket(SERVER_IP,SERVER_PORT, "Hello")
        sock.sendall(pac)
        print("Sent hello to server!")
        data = sock.recv(1024)
        if data.haslayer(Raw):
            print(data.getLayer(Raw))

    except:
        print("Socket connection failed.")

def connected(c):
    '''
    Input: Socket c
    Output: none
    Function for thread after accepting socket connections
    '''
    while True:

        data = c.recv(1024)
        if data.haslayer(Raw):
            print(data.getLayer(Raw))
        else:
            break

        pac = getPacket('0.0.0.0',PORT, "Hello")
        c.sendall(pac)
        

    c.close()


def listen():
    '''
    Input: none
    Output: none
    Listening in a specific port and accepting clients which are transfered to a new thread session
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Listenning...")
        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            start_new_thread(connected, (conn,))

def get_my_ip():
    """
    Find my IP address
    :return: my local ip address
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def main():
    start_new_thread(connect_to, (SERVER_IP, SERVER_PORT))
    start_new_thread(listen, ())

main()

