#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    infinity_var = float('inf')

    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        destNode = self.network.nodes[destIndex]
        total_length = self.lengths[destNode]
        length = self.lengths[destNode]
        currInd = destIndex
        while length != 0:
            if self.prev[currInd] == None:
                return {'cost':float('inf'), 'path':path_edges}
            prevNode = self.network.nodes[self.prev[currInd]]
            for N in prevNode.neighbors:
                if N.dest == destNode:
                    edge = N
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            length = self.lengths[prevNode]
            currInd = prevNode.node_id
            destNode = self.network.nodes[currInd]
        return {'cost':total_length, 'path':path_edges}



    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        self.paths = []
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        if use_heap == False:
            self.dijkstrasArray(srcIndex)
        else:
            self.dijkstrasHeap(srcIndex)

        t2 = time.time()
        return (t2-t1)
    
    def dijkstrasHeap(self, srcIndex):
        priQueue = queueBinaryHeap()
        priQueue.createQueue(self.network)
        self.prev = []
        self.lengths = {}
        for N in self.network.getNodes():
            self.prev.append(None)
            self.lengths[N] = float('inf')
        self.lengths[self.network.nodes[srcIndex]] = 0
        priQueue.insert(self.network.nodes[srcIndex], 0)
        priQueue.currentMin = self.network.nodes[srcIndex]
        while len(priQueue.heap) != 0:
            u,length = priQueue.deleteMin()
            for V in u.neighbors:
                if V.dest != None:
                    if self.lengths[V.dest] > length + V.length:
                        newLength = length + V.length
                        self.prev[V.dest.node_id] = u.node_id
                        self.lengths[V.dest] = newLength
                        if len(priQueue.heap) != 0:
                            priQueue.decreaseKey(V.dest, newLength)
                        self.paths.append(V)

    def dijkstrasArray(self, srcIndex):
        priQueue = queueUnsortedArray2(srcIndex)
        priQueue.createQueue(self.network)
        self.prev = []
        self.lengths = {}
        for N in self.network.getNodes():
            self.prev.append(None)
            self.lengths[N] = float('inf')
        self.lengths[self.network.nodes[srcIndex]] = 0
        priQueue.insert(self.network.nodes[srcIndex], 0)
        priQueue.currentMin = self.network.nodes[srcIndex]
        while len(priQueue.queue) != 0:
            u,length = priQueue.deleteMin()
            for V in u.neighbors:
                if V.dest != None:
                    if self.lengths[V.dest] > length + V.length:
                        newLength = length + V.length
                        self.prev[V.dest.node_id] = u.node_id
                        if priQueue.queue.get(V.dest) != None:
                            priQueue.insert(V.dest, newLength) 
                            priQueue.currentMin = V.dest
                        self.lengths[V.dest] = newLength

class queueUnsortedArray2:
        def __init__( self,srcIndex):
            self.start = srcIndex
            self.queue = {}
    
        def insert(self,V,weight): #manages inserts and decreases
            self.queue[V] = weight

        def deleteMin(self):
            keys = self.queue.keys()
            if len(self.queue) != 0:
                for key in keys:
                    if self.queue.get(self.currentMin) == None:
                        tempMin = key
                        self.currentMin = tempMin
                    if self.queue[key] < self.queue[self.currentMin]:
                        self.currentMin = key
                currLength = self.queue[self.currentMin]
                del self.queue[self.currentMin]
                return self.currentMin, currLength
            else:
                return None
        
        def createQueue(self,G):
            for V in G.nodes:
                self.insert(V, float('inf'))


        # use maps, (item, key)
        #delete min (iterate through each item with lowest key)
        #insert (just insert onto the map)
        #compare with previousLength(take current key and compare with new key)
        #decreseKey
        #makeQueue

class queueBinaryHeap:
    def __init__(self):
        self.heap = []
        self.priorities = {}
        self.positions = {}
        pass

    def bubbleUp(self, V):
        Vindex = self.positions[V]
        Pindex = self.getParent(Vindex)
        if Pindex < len(self.heap) - 1:
            PNode = self.heap[Pindex]
            VNode = self.heap[Vindex]
            test = self.positions[self.heap[Pindex]]
            if self.priorities[V] < self.priorities[self.heap[Pindex]]:
                self.positions[V] = Pindex
                self.positions[PNode] = Vindex
                self.heap[Vindex] = PNode
                self.heap[Pindex] = VNode
                if self.heap[0] != VNode:
                    self.bubbleUp(VNode)


    def siftDown(self,V):
        Vindex = self.positions[V]
        RCindex = self.getRChild(Vindex)
        LCIndex = self.getLChild(Vindex)
        VNode = self.heap[Vindex]
        if RCindex > len(self.heap) - 1 and RCindex < len(self.heap) - 1:
            RCNode = self.heap[RCindex]
            LCNode = self.heap[LCIndex]
            if self.priorities[RCNode] < self.priorities[LCNode]:
                smallChild = self.priorities[RCNode]
                smallChildInd = RCindex
            else:
                smallChild = self.priorities[LCNode]
                smallChildInd = LCIndex
            if self.priorities[V] > smallChild:
                self.positions[V] = self.positions[self.heap[smallChildInd]]
                self.positions[smallChild] = Vindex
                self.heap[Vindex] = smallChild
                self.heap[smallChildInd] = VNode
                self.siftDown(smallChild)

    def minChild(self,V):
        pass

    def insert(self, V, pri):
        if self.positions.get(V)!= None:
            self.decreaseKey(V, pri)
        else:
            self.heap.append(V)
            self.priorities[V] = float('inf')
            self.positions[V] = self.heap.index(V)
            self.bubbleUp(V)

    def createQueue(self, G):
        for V in G.nodes:
            self.heap.append(V)
            self.priorities[V] = float('inf')
            self.positions[V] = self.heap.index(V)

    def deleteMin(self):
        min = self.heap[0]
        self.heap[0] = self.heap[len(self.heap) - 1]
        self.positions[self.heap[0]] = 0
        self.siftDown(self.heap[0])
        del self.heap[-1]
        return min,self.priorities[min]

    def decreaseKey(self, V, newPri):
        self.priorities[V] = newPri
        if self.heap[0] != V:
            self.bubbleUp(V)
        

    def getParent(self,i):
        return ((i + 1)//2) - 1

    def getLChild(self,i):
        return (i + 1)* 2 - 1

    def getRChild(self,i):
        return (i + 1) * 2