from mimetypes import MimeTypes
from sys import flags
from scapy.all import *
import time
import threading
import socket
import time
import json

flag = 'F'

MY_CONTAINER_NAME = str(subprocess.check_output(['bash','-c', 'hostname']).decode("utf-8")).replace("\n","")
MY_IP = socket.gethostbyname(MY_CONTAINER_NAME)
SRC_IP, SRC_PORT = MY_CONTAINER_NAME, 5000
CONTROLLER_IP = socket.gethostbyname("sdn")
rrt_time = 0
routingTable = {}

flagsMapping = {
    'F': '1',
    'S': '2',
    'R': '3',
    'P': '4',
    'A': '5',
    'U': '6',
    'E': '7',
    'C': '8',
}


def getNextAddress(sfcNo):
    global routingTable, MY_CONTAINER_NAME
    sfcPath = routingTable[sfcNo]

    DEST_IP, DEST_PORT = "0.0.0.0", 10000

    for i in range(len(sfcPath)):
        l = sfcPath[i]
        if MY_CONTAINER_NAME in l:
            DEST_IP, DEST_PORT = sfcPath[i+1][0], sfcPath[i+1][1]

    print(DEST_IP, DEST_PORT)
    return DEST_IP, DEST_PORT
    

def recieve_ack():
    global rrt_time
    def handle_packet(packet):
        print("ack recieved")
        print(bytes(packet[TCP].payload).decode('utf-8'))
        print("---- RTT = {0} seconds ---- ".format(time.time() - rrt_time))

    sniff(prn=handle_packet, filter = "tcp and src port 10000 and dst port 5000")    
   

def send_request():
    time.sleep(3)
    global rrt_time, SRC_IP, SRC_PORT, flagsMapping, flag

    while True:
        rrt_time = time.time()
        DEST_IP, DEST_PORT = getNextAddress(flagsMapping[flag])
        data = "This is the data from the {0}".format(MY_CONTAINER_NAME)

        pkt = IP(ttl = 64)
        pkt.src = SRC_IP
        pkt.dst = DEST_IP
        pkt = pkt/TCP(sport=SRC_PORT, dport=DEST_PORT, flags=flag)/Raw(load=data)
        send(pkt)
        time.sleep(20)


def getRoutingTable():
    global routingTable
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((CONTROLLER_IP, 4000))
    data = client.recv(4096)
    routingTable = json.loads(data.decode('utf-8'))

    # print(routingTable)

if __name__ =="__main__":
    getRoutingTable()

    t1 = threading.Thread(target=send_request)
    t2 = threading.Thread(target=recieve_ack)

    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
 
    print("Done!")
