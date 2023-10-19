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
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        t2 = time.time()
        return (t2-t1)
    
    def dijkstraUnsortedArray():
        # use maps, (item, key)
        #delete min (iterate through each item with lowest key)
        #insert (just insert onto the map)
        #compare with previousLength(take current key and compare with new key)
        #decreseKey
        #makeQueue
        return None
    
    def dijkstraBinaryHeap():
        #delete min 
        #insert
        #decreseKey
        #makeQueue
        return None

