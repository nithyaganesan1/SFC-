import socket
import json 

routingTable = {
    "1" : [["src"],["node_1",7000],["node_2",7000],["dst",10000]]
}


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendRoutingTable():
    serv.bind(('', 4000))

    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        data = json.dumps(routingTable).encode('utf-8')
        conn.sendall(data)
        conn.close()

sendRoutingTable()