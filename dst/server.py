from scapy.all import *
import socket

MY_CONTAINER_NAME = str(subprocess.check_output(['bash','-c', 'hostname']).decode("utf-8")).replace("\n","")
MY_IP = socket.gethostbyname(MY_CONTAINER_NAME)
SRC_IP, SRC_PORT = MY_CONTAINER_NAME, 10000
DST_PORT = 5000

FILTER = 'tcp and dst port 10000 and (src port 6000 or src port 7000 or src port 8000 or src port 9000) and dst {0}'.format(MY_IP)

ack_data = "This is ack from the {0}".format(MY_CONTAINER_NAME)


def send_ack(dst, dst_port):
    global MY_CONTAINER_NAME, ack_data, SRC_IP, SRC_PORT, DST_PORT

    pkt = IP(ttl = 64)
    pkt.src = SRC_IP
    pkt = pkt/TCP(sport=SRC_PORT, dport=dst_port)/Raw(load=ack_data)
    pkt.dst = dst
    send(pkt)

def handle(packet):
    global MY_IP
    d = bytes(packet[TCP].payload).decode('utf-8')
    
    print("packet recived")
    print(d)

    if("client_1" in d):
        send_ack(packet[IP].src, 5000)
    elif("client_2" in d):
        send_ack(packet[IP].src, 5001)
    elif("client_3" in d):
        send_ack(packet[IP].src, 5002)
    elif("client_4" in d):
        send_ack(packet[IP].src, 5003)
    elif("client_5" in d):
        send_ack(packet[IP].src, 5004)

sniff(prn = handle, filter = FILTER)