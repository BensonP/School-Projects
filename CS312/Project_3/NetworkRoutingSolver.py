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
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        paths = None
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        if use_heap == False:
            dArray = queueUnsortedArray(self.network, srcIndex)
            paths = queueUnsortedArray.dijkstrasArray(dArray)


        t2 = time.time()
        return (t2-t1)
    
class queueUnsortedArray:
        def __init__( self,G,srcIndex):
            self.start = srcIndex
            self.queue = {}
            self.makeQueue(G)
    
        def insert(self,V):
            self.queue[V.node_id] = [V,float('inf'), None, 0]

        def makeQueue(self,G):
            nodes = G.getNodes()
            for V in nodes:
                self.insert(V)
            self.queue[self.start] = [nodes[self.start],0,None,0]

        def findMin(self):
            currentMin = float('inf')
            for V in self.queue:
                if self.queue[V][1] < currentMin and self.queue[V][3] == 0:
                    currentMin = self.queue[V][0].node_id
            if currentMin != float('inf'):
                return currentMin
            else: 
                return self.queue[self.start][0]

        def dijkstrasArray(self):
            currentNode = self.queue[self.start][0]
            visited = 0
            while visited == 0:
                for N in currentNode.neighbors:
                    current_id = currentNode.node_id
                    if N.length <= self.queue[current_id][1]:
                        self.queue[N.dest.node_id][1] = N.length + self.queue[current_id][1]
                        self.queue[N.dest.node_id][2] = self.queue[current_id][0]
                    self.queue[current_id][3] = 1
                    currentNode = self.queue[self.findMin()][0]
                    if self.queue[currentNode.node_id][3] == 1:
                        visited = 1                
            return self.queue

                        

                    



        # use maps, (item, key)
        #delete min (iterate through each item with lowest key)
        #insert (just insert onto the map)
        #compare with previousLength(take current key and compare with new key)
        #decreseKey
        #makeQueue