import socket    
import dirserver.mapping as mapping
from _thread import *
from scapy import *
#!/usr/bin/env python3
# ipc_server.py

import socket
from fastapi import FastAPI

try:
    app = FastAPI()
    @app.get("/")
    def read_root():
        pass
except:
    pass


HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 9898        # Port to listen on (non-privileged ports are > 1023)


def getPacket(dst_port, dst_ip, data):
    '''
    Input: destination port, destination Ip, data to pass
    Output: the built TCP packet
    Building a TCP packet with the required fields
    '''
    return Ether()/IP(dst=dst_ip)/TCP(dport=dst_port,flags='S')/Raw(load=data)

def connected(c):
    '''
    Input: Socket c
    Output: none
    Function for thread after accepting socket connections
    '''
    while True:

        data = c.recv(1024).decode()
        if data != 'goodbye':
            print(data)
        else:
            break
        c.sendall(data.encode())
        

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

def connect_to(dst_ip, dst_port):
    '''
    Input: src_ip, src_port, dst_ip, dst_port
    Output: none
    Trying to coonect to a specific machine via socket
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting to connect")
    try:
        sock.connect((dst_ip, dst_port))
        print("Connection to server complete.")

        sock.sendall('hello'.encode())
        data = sock.recv(1024).decode()
        if data != 'goodbye':
            print(data.encode())

    except:
        print("Socket connection failed.")


def buildNodesList():
    '''
    Input: none
    Output: json string containing the avalable nodes list
    Creating the nodes list in a json format
    '''
    ipList = mapping.map_network()
    ipList.remove(mapping.get_my_ip()) 

    nodesJson = json.dumps(ipList)

    return nodesJson

def addToNodesList(nodesJson, nodeToAdd):
    '''
    Input: the nodes list as json string, the node to add
    Output: json string containing all of the previous nodes and the new node
    Adding to the nodes list and reformating the list into json
    '''
    nodesList = json.loads(nodesJson)
    nodesList.append(nodeToAdd)

    return json.dumps(nodesList)

def removeFromNodesList(nodesJson, nodeToRemove):
    '''
    Input: the nodes list as json string, the node to remove
    Output: json string containing all but the node to remove items from the original list
    Removing from the nodes list and reformating the list into json
    '''
    nodesList = json.loads(nodesJson)
    nodesList.remove(nodeToRemove)

    return json.dumps(nodesList)

def main():
    print("\n\n\n" + mapping.get_my_ip() + "\n\n\n")
    start_new_thread(listen, ())
    start_new_thread(connect_to, ("172.20.0.3", 9898))
    #Able to connect to a node via connect_to function



main()


