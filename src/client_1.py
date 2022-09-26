from mimetypes import MimeTypes
from scapy.all import *
import time
import threading
import socket
import time

MY_CONTAINER_NAME = str(subprocess.check_output(['bash','-c', 'hostname']).decode("utf-8")).replace("\n","")
MY_IP = socket.gethostbyname(MY_CONTAINER_NAME)
SRC_IP, SRC_PORT = MY_CONTAINER_NAME, 5000
rrt_time = 0

def getNextAddress():
    # global DEST_IP
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect((CONTROLLER_IP, 7000))
    # client.send(MY_CONTAINER_NAME.encode('ascii'))
    # data = client.recv(4096)
    # DEST_IP = str(data.decode("utf-8"))
    
    DEST_IP, DEST_PORT = "node_1", 6000

    # print("From Client, send data to ->", DEST_IP)
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
    global rrt_time, SRC_IP, SRC_PORT

    while True:
        rrt_time = time.time()
        DEST_IP, DEST_PORT = getNextAddress()
        data = "This is the data from the {0}".format(MY_CONTAINER_NAME)

        pkt = IP(ttl = 64)
        pkt.src = SRC_IP
        pkt.dst = DEST_IP
        pkt = pkt/TCP(sport=SRC_PORT, dport=DEST_PORT)/Raw(load=data)
        send(pkt)
        time.sleep(20)


if __name__ =="__main__":
    t1 = threading.Thread(target=send_request)
    t2 = threading.Thread(target=recieve_ack)

    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
 
    print("Done!")
