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

    def getShortestPath( self, destIndex ): #O(|V| * |E|) this has to iterate through all nodes that are in the path from src to dest, and it also has to check each V of each Node in that path. 
        path_edges = []
        destNode = self.network.nodes[destIndex]
        if self.prev[destIndex] == None:
                return {'cost':float('inf'), 'path':path_edges}
        total_length = self.lengths[destIndex]
        length = self.lengths[destIndex]
        while length != 0:
            prevNode = self.network.nodes[self.prev[destIndex]]
            for N in prevNode.neighbors:
                if N.dest == destNode:
                    edge = N
                    break
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            length = self.lengths[prevNode.node_id]
            destIndex = prevNode.node_id
            destNode = self.network.nodes[destIndex]
        return {'cost':total_length, 'path':path_edges}



    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        self.paths = []
        if use_heap == False:
            priQueue = queueUnsortedArray() #create queue with unsorted array
        else:
            priQueue = queueBinaryHeap() #create queue with binary heap

        self.dijkstras(srcIndex, priQueue) 

        t2 = time.time()
        return (t2-t1)
    
    def dijkstras(self, srcIndex, priQueue):                #array: O(|V|^|E|), == O(N^2) of having to delete min for each node, and decreaseKey for each neighboring nodes
                                                            #Heap: O(|V| * log(V) + |E| * log(|V|)) == O((|V| + |E|)log(|V|)) having to delete for each node, and decrease key for each neighboring nodes. 
        priQueue.createQueue(self.network)                  #create queue: for both binary heap and array: O(N). Has to insert into data structures for as nodes in Network. 
        self.prev = [None] * len(self.network.getNodes())   #previous array to store what node was previous on the graph for each node
        self.lengths = {}                                   #lengths dictionary to store how far the node from the srcIndex
        self.lengths[srcIndex] = 0                          
        for G in self.network.getNodes():
            self.lengths[G.node_id] = float('inf')          #O(N)
        self.lengths[srcIndex] = 0                          #set srcNode dist to 0
        priQueue.decreaseKey(srcIndex, 0)                   #set srcNode in queue priority to 0
        while len(priQueue.queue) != 0:                     #Run dijkstras until queue is empty, see below for appropriate O(N) complexities.
            u,length = priQueue.deleteMin()                 #Array: O(N), heap: O(log(N))
            u = self.network.nodes[u]
            for V in u.neighbors:                           #Array: has to run for each Edge, and run insert, which is O(1) 
                if V.dest != None:
                    if self.lengths[V.dest.node_id] > length + V.length:
                        newLength = length + V.length
                        self.prev[V.dest.node_id] = u.node_id
                        priQueue.decreaseKey(V.dest.node_id, newLength)      #Array: O(1) heap: O(log(N))
                        self.lengths[V.dest.node_id] = newLength

class queueUnsortedArray:                      #insert - O(1), decreaseKey O(1), deleteMin O(N), createQueue O(N)
        def __init__( self):
            self.queue = {}
    
        def insert(self,V,pri):               #insert a new Node V with given prioirity, constant time
            self.queue[V] = pri

        def decreaseKey(self, V, newPri):     #decrease the node V with newPriority newPri, constant time
            self.queue[V] = newPri


        def deleteMin(self):                  #iterate through all the nodes in my queue and find the lowest priority, and return it. O(N)
            minKey, currentMin = self.findMin()
            if minKey != None:
                del self.queue[minKey]
                return minKey, currentMin
            
        def findMin(self):                     #iterating through all nodes to find min
            keys = list(self.queue.keys())
            minKey = keys[0]
            currentMin = self.queue[minKey]
            for key in self.queue.keys():
                if self.queue[key] < currentMin:
                    currentMin = self.queue[key]
                    minKey = key
            return minKey,currentMin
        
        def createQueue(self,G):                #for each node G in my network, create a key:value pair in my dictionary with node_id associated with infinity as its priority
            for V in G.nodes:
                self.insert(V.node_id, float('inf'))

class queueBinaryHeap:                         #insert - O(log(N)), decreaseKey O(log(N)), deleteMin O(log(N)), createQueue O(N)
    def __init__(self):
        self.queue = []
        self.priorities = {}
        self.positions = {}

    def swap(self,V1, V2):
        V1Node = self.queue[V1]
        V2Node = self.queue[V2]
        self.positions[V1Node] = V2
        self.positions[V2Node] = V1
        self.queue[V1] = V2Node
        self.queue[V2] = V1Node

    def bubbleUp(self, Vindex):                #space - O(logN), for having to potentially call this that many times as their all levels in tree
        Pindex = self.getParent(Vindex)
        VNode = self.queue[Vindex]
        PNode = self.queue[Pindex]
        while Vindex > 0 and self.priorities[VNode] < self.priorities[PNode]:
            self.swap(Vindex, Pindex)
            Vindex = Pindex
            Pindex = self.getParent(Vindex)
            VNode = self.queue[Vindex]
            PNode = self.queue[Pindex]


    def siftDown(self,Vindex):                  #space - O(logN), for having to potentially call this that many times as their all levels in tree
        Vnode = self.queue[Vindex]              
        minChild,minIndex = self.minChild(Vindex)
        while minChild != None and minIndex < len(self.queue) - 1 and self.priorities[minChild] < self.priorities[Vnode]:
            self.swap(Vindex,minIndex)
            Vindex = minIndex
            minChild,minIndex = self.minChild(Vindex)
            Vnode = self.queue[Vindex]


    

    def minChild(self,Vindex):                  #Recieves the min left or right child, constant time. 
        RCindex = self.getRChild(Vindex)
        LCindex = self.getLChild(Vindex)
        if LCindex == None and RCindex == None:
            return None,None
        LCNode = self.queue[LCindex]
        if LCindex != None and RCindex == None:
            return LCNode,LCindex
        RCNode = self.queue[RCindex]
        if LCindex != None and RCindex != None:
            if self.priorities[RCNode] < self.priorities[LCNode]:
                return RCNode,RCindex
            else: return LCNode, LCindex


    def insert(self, V, pri):             #log(N) due to having to bubble up potentially all the levels of the tree
        self.queue.append(V)
        self.priorities[V] = pri
        self.positions[V] = len(self.queue) - 1
        self.bubbleUp(self.positions[V])

    def createQueue(self, G):    #O(N) due to iterating through all my nodes to set default values for a dijkstras problem. 
        for V in G.nodes:
            V = V.node_id
            self.queue.append(V)
            self.priorities[V] = float('inf')
            self.positions[V] = len(self.queue) - 1

    def deleteMin(self):         #O(log(N)) due to sifting down log(N) levels
        min = self.queue[0]
        self.queue[0] = self.queue[len(self.queue) - 1]
        self.positions[self.queue[0]] = 0
        self.siftDown(0)
        del self.queue[-1]
        return min,self.priorities[min]

    def decreaseKey(self, V, newPri):  #O(log(N)) due to bubling up levels. 
        if len(self.queue) != 0:
            self.priorities[V] = newPri
            if self.queue[0] != V:
                self.bubbleUp(self.positions[V])
            

    def getParent(self,i):
        return ((i + 1)//2) - 1

    def getLChild(self,i):
        Lindex = (i + 1)* 2 - 1
        if Lindex < len(self.queue) - 1:
            return Lindex
        else:
            return None

    def getRChild(self,i):
        Rindex = (i + 1) * 2
        if Rindex < len(self.queue) - 1:
            return Rindex
        else:
            return None