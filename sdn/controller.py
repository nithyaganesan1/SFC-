import socket
import json 
from antColonyOptimization import getSFCPath

graph = {}
degree = []
start = end = edges = 0


VNFPortMapping = {"src": 5000, "FW": 6000, "DPI": 7000, "LB": 8000, "dst": 12000}
nodeContainerMapping = {}

SFCreqs = []

SFCPathTable = {    }

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendRoutingTable():
    global SFCPathTable
    serv.bind(('', 4000))

    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        data = json.dumps(SFCPathTable).encode('utf-8')
        conn.sendall(data)
        conn.close()


def readGraph():
    global graph, degree, start, end, edges
    file = open("graph.txt", "r")
    content = str(file.read()).split('\n')

    start, end, edges = int(content[0]), int(content[1]), int(content[2])

    for i in range(start, end+1):
        graph[i] = []

    for i in range(3, 3+edges):
        line = content[i].split(' ')
        src, dst, wgt = int(line[0]), int(line[1]), float(line[2])
        graph[src].append([dst, wgt])
        graph[dst].append([src, wgt])


    degree = [0]*len(graph)
    for i in range(len(graph)):
        degree[i] = len(graph[i])

    for i in range(len(graph)):
        nodeContainerMapping[i] = "node_{0}".format(i)
    
    nodeContainerMapping[start] = "src"; nodeContainerMapping[end] = "dst"


def readSFCRequests():
    global SFCreqs
    file = open("sfc.txt", "r")
    content = str(file.read()).split('\n')

    for line in content:
        req = line.split(' ')
        SFCreqs.append(req[1:])


def calculateSFCPath():
    global SFCPathTable
    for idx, sfc in enumerate(SFCreqs):
        print("SFC_1: CNF_order = {0}".format(sfc), end =" ")
        path = getSFCPath(graph, degree, start, end, len(sfc))
        # print(sfc, path)
        

        chain = []

        for i in range(len(path)):
            port = 9000
            if(i < len(sfc)-1):
                port = VNFPortMapping[sfc[i]]

            n = [nodeContainerMapping[path[i]], port]
            chain.append(n)
        
        chain[-1][1] = 10000
        SFCPathTable[str(idx+1)] = chain


if __name__ == "__main__" :
    readGraph()
    readSFCRequests()
    calculateSFCPath()

    print("Routing Table = {0}".format(SFCPathTable))

    sendRoutingTable()