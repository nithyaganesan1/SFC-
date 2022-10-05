import random

class Ant :
    trail = []
    trailWeight = 0.0

    def __init__(self, numberOfNodes) :
        self.numberOfNodes = numberOfNodes
        self.visited = [False] * (numberOfNodes +1)

    def visitNode(self, node, weight) :
        self.trail.append(node)
        self.trailWeight += weight
        self.visited[node] = True

    def getVisited(self) :
        return self.visited

    def getTrailLength(self) : 
        return len(self.trail)

    def getTrail(self) : 
        return self.trail
    
    def getTrailWeight(self) :
        return self.trailWeight

    def clear(self) :
        self.trail = []
        self.trailWeight = 0.0
        self.visited = [False] * (self.numberOfNodes)

class AntColonyOptimization : 
    alpha = 1.0
    beta = 5.0
    evaporation = 0.5
    # Q = 500
    antFactor = 500
    maxIterations = 10

    ants = []
    bestTrail = []
    bestTrailWeight = 1e18
    # probabilities = []
    pheromones = []

    def __init__(self, graph, start, end, minTrailLength) : 
        self.graph = graph
        self.minTrailLength = minTrailLength
        self.numberOfNodes = len(graph)
        self.numberOfAnts = int(self.numberOfNodes * self.antFactor)

        for i in range(self.numberOfNodes) :
            self.pheromones.append([0]*(self.numberOfNodes))
        
        self.start = start
        self.end = end

        # self.probabilities = [0] * self.numberOfNodes
        for i in range(self.numberOfAnts) :
            self.ants.append(Ant(self.numberOfNodes))

        # print(len(self.ants))
        # print (self.numberOfNodes)
        self.solve()

    def getEdgeWeight(self, source, target) :
        for edge in self.graph[source] :
            if (edge[0] == target) :
                return edge[1]
        return -1        

    def initPheromones(self) :
        for i in range(self.numberOfNodes) : 
            for j in range(self.numberOfNodes) :
                weight = float(self.getEdgeWeight(i,j))
                # print(i, j, weight)
                if (weight != -1) :
                    self.pheromones[i][j] = 1.0/weight #magnification
                    # print('===', i, j, weight)
                # print(self.pheromones[i][j])
        return

    def calculateProbability(self, currentNode, visited) : 
        probabilities = [0] * (self.numberOfNodes)
        sum = 0.0

        for edge in self.graph[currentNode] :
            nextNode = edge[0]
            if (visited[nextNode] == False) :
                weight = edge[1]
                nij = 1.0/weight #magnification
                tij = self.pheromones[currentNode][nextNode]
                sum += ((tij ** self.alpha) * (nij ** self.beta))

        if(sum == 0) :
            return probabilities

        for edge in self.graph[currentNode] :
            nextNode = edge[0]
            if (visited[nextNode] == False) :
                weight = edge[1]
                nij = 1.0/weight #magnification
                tij = self.pheromones[currentNode][nextNode]
                probabilities[nextNode] = ((tij ** self.alpha) * (nij ** self.beta)) / sum
        
        return probabilities

    def findNextNode(self, currentNode, visited) :
        probabilities = self.calculateProbability(currentNode,visited)
        sum = 0.0
        nextNode = -1
        for i in range( len(probabilities)) :
            probabilities[i] *= 100
            sum += probabilities[i]

        if (sum == 0) :
            return -1
        # random number between (0, sum] = [1,sum] - [0, 1) 
        number = random.uniform(1.0,sum) - random.random() 
        prev = 0.0
        for i in range(len(probabilities)) :
            if (prev <= number and number <= prev + probabilities[i]) :
                nextNode = i
                break
            prev += probabilities[i]
        #check if it returns a single value or list
        # todo = update random selection --done
        # nextNode = random.choices(range(len(probabilities)), weights=probabilities, k=1)
        return nextNode

    # check if a given edge is present in the best trail
    def checkEdgeInShortestTrail(self, src, dst) :
        # todo update code for multiple best trail -- done
        for  trail in self.bestTrail :
            length = len(trail)
            for i in range(length - 1) :
                if (trail[i] == src and trail[i+1] == dst) :
                    return True
        return False

    # only update if the current path is smallest
    def updatePheromones(self) :
        dt = 1.0 / float(self.bestTrailWeight) #magnification

        for i in range(self.numberOfNodes) : 
            for j in range(self.numberOfNodes) :
                weight = float(self.getEdgeWeight(i,j))
                dtij = dt if self.checkEdgeInShortestTrail(i,j) else 0.0
                tij = self.pheromones[i][j]
                if (weight != -1) :
                    self.pheromones[i][j] = (1.0 - self.evaporation) * tij + dtij

    # update on pheromone on path taken by ant
    def updateLocalPheromones(self, currentNode, nextNode) :
        # todo = move local pheromone update to another function -- done 
        weight = float(self.getEdgeWeight(currentNode,nextNode))
        t0 = 1.0 / weight #magnification
        if (weight < 0) :
            t0 = 0
        tij = self.pheromones[currentNode][nextNode]
        self.pheromones[currentNode][nextNode] = ((1.0 - self.evaporation) * tij) + (self.evaporation * t0)

    # find solution for one ant
    def solveAnt(self, ant) :
        currentNode = self.start
        while(currentNode != self.end):
            nextNode = self.findNextNode(currentNode, ant.getVisited())
            if(nextNode == -1):
                ant.visitNode(-1, 1e9)
                break
            self.updateLocalPheromones(currentNode, nextNode)
            ant.visitNode(nextNode, self.getEdgeWeight(currentNode, nextNode))
            currentNode = nextNode

    # initialise all ants for each iteration 
    def initAnts(self) :
        for ant in self.ants :
            ant.clear()
            ant.visitNode(self.start, 0.0)

    def uniqueTrail(self, trail, trails):
        for x in trails:
            if(len(x) == len(trail)):
                eq = True
                for i in range(len(x)) :
                    if(x[i] != trail[i]) :
                        eq = False
                        break
                if(eq):
                    return False
        return True

    # find solution for for all ants for 1 iteration
    def solveIteration(self) :
        self.initAnts()
        bestTrail = []
        bestTrailWeight = 1e18
        for ant in self.ants :
            self.solveAnt(ant)
            if (ant.getTrailLength() >= self.minTrailLength):
                if (ant.getTrailWeight() < bestTrailWeight) :
                    bestTrail = []
                    bestTrail.append(ant.getTrail())
                    bestTrailWeight = ant.getTrailWeight()
                    self.updatePheromones()
                elif (ant.getTrailWeight() == bestTrailWeight) :
                    if(self.uniqueTrail(ant.getTrail(),bestTrail)):
                        bestTrail.append(ant.getTrail())
                        self.updatePheromones()
        return bestTrail, bestTrailWeight

    def solve(self) :
        # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.pheromones]))
        self.initPheromones()
        # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.pheromones]))

        for i in range(self.maxIterations) :
        # for i in range(100) :
            trails, trailWeight = self.solveIteration()
            # print(trailWeight, trails)
            if(trailWeight < self.bestTrailWeight) :
                self.bestTrail = trails
                self.bestTrailWeight = trailWeight
            if(trailWeight == self.bestTrailWeight) :
                for trail in trails :
                    if( self.uniqueTrail(trail,self.bestTrail) ) :
                        self.bestTrail.append(trail)
        
    def getBestTrail(self) :
        return self.bestTrail
    
    def getBestTrailWeight(self) :
        return self.bestTrailWeight

if __name__ == "__main__":
    file = open("graph.txt", "r")
    content = str(file.read()).split('\n')

    start = int(content[0])
    end = int(content[1])
    edges = int(content[2])
    
    graph = {}

    for i in range(start, end+1):
        graph[i] = []

    for i in range(3, 3+edges):
        line = content[i].split(' ')
        src, dst, wgt = int(line[0]), int(line[1]), float(line[2])
        graph[src].append([dst, wgt])
        

    minTrailLength = 2
    
    print('====debug====')
    antColony = AntColonyOptimization(graph, start, end, minTrailLength)
    print('====debug====')

    trails = antColony.getBestTrail()
    print(antColony.getBestTrailWeight())
    for trail in trails :
        print(trail)