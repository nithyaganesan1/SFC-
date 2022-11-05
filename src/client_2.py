from mimetypes import MimeTypes
from sys import flags
from scapy.all import *
import time
import threading
import socket
import time
import json

flag = 'S'

MY_CONTAINER_NAME = str(subprocess.check_output(['bash','-c', 'hostname']).decode("utf-8")).replace("\n","")
MY_IP = socket.gethostbyname(MY_CONTAINER_NAME)
SRC_IP, SRC_PORT = MY_CONTAINER_NAME, 5001
CONTROLLER_IP = socket.gethostbyname("sdn")
data = "This is the data from the client_2"
rrt_time = []
rtt_index = 0
routingTable = {}
total_pkt_send = 100
total_ack_receive = 0

total_rtt = 0.0
total_thorughput = 0.0

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
    global rrt_time, data, total_ack_receive, rtt_index, total_rtt, total_thorughput, SRC_PORT

    def handle_packet(packet):
        global total_ack_receive, rrt_time, rtt_index, total_rtt, total_thorughput
        print("ack recieved")
        print(bytes(packet[TCP].payload).decode('utf-8'))
        rtt = time.time() - rrt_time[rtt_index]
        rtt_index += 1
        total_rtt += rtt
        total_thorughput += ((len(data)/rtt)*8)
        print("---- RTT = {0} seconds ---- ".format(rtt))
        print("---- Throughput = {0} B/s ---- ".format((len(data)/rtt)*8))
        total_ack_receive += 1

    sniff(prn=handle_packet, filter = "tcp and src port 10000 and dst port 5001")    
   

def send_request():
    time.sleep(3)
    global rrt_time, SRC_IP, SRC_PORT, flagsMapping, flag, data, total_pkt_send, total_rtt, total_thorughput

    for i in range(total_pkt_send):
        rrt_time.append(time.time())
        DEST_IP, DEST_PORT = getNextAddress(flagsMapping[flag])
    
        pkt = IP(ttl = 64)
        pkt.src = SRC_IP
        pkt.dst = DEST_IP
        pkt = pkt/TCP(sport=SRC_PORT, dport=DEST_PORT, flags=flag)/Raw(load=data)
        send(pkt)
        print(len(pkt))
        time.sleep(1)
    
    time.sleep(20)

    print("########################################################################################################## Packetloss = {0}% ####### ".format((total_pkt_send-total_ack_receive)*100/total_pkt_send))
    print("########################################################################################################## Avg RTT = {0} seconds ####### ".format(total_rtt/total_ack_receive))
    print("########################################################################################################## Avg Throghput = {0} B/s ####### ".format(total_thorughput/total_ack_receive))

def getRoutingTable():
    global routingTable
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((CONTROLLER_IP, 4000))
    data = client.recv(4096)
    routingTable = json.loads(data.decode('utf-8'))

    # print(routingTable)

if __name__ == "__main__" :
    getRoutingTable()

    t1 = threading.Thread(target=send_request)
    t2 = threading.Thread(target=recieve_ack)

    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
 
    print("Done!")
