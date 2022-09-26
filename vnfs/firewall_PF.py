from pydoc import describe
from scapy.all import *
import sys
import socket 

MY_CONTAINER_NAME = str(subprocess.check_output(['bash','-c', 'hostname']).decode("utf-8")).replace("\n","")
MY_IP = socket.gethostbyname(MY_CONTAINER_NAME)
SRC_PORT = 6000

FILTER = 'tcp and dst port 6000'

def getNextAddress():
    DEST_IP, DEST_PORT = "dst", 10000
    return DEST_IP, DEST_PORT


def handle_packet(packet):
    global SRC_PORT
    
    print("packet recieved")
    print(bytes(packet[TCP].payload))
        
    DEST_IP, DEST_PORT = getNextAddress()
    pkt = IP(ttl = 64)
    pkt = pkt/TCP(sport=SRC_PORT, dport=DEST_PORT)/Raw(load=bytes(packet[TCP].payload))
    pkt.src = packet[IP].src  # original ip of client
    pkt.dst = DEST_IP
    send(pkt)


sniff(prn=handle_packet, filter = FILTER)