import numpy as np

class Solution(object):
    def findCircleNum(self, isConnected):
        """
        :type isConnected: List[List[int]]
        :rtype: int
        """
        length = len(isConnected[0])
        print(length)
        isVisited = np.zeroes((isConnected.shape[0]))
        p = 0
        for i in range(length):
            if isVisited[i] == 0:
                explore(isConnected, isVisited, i, length)
                p +=1
        return p
                

def explore(isConnected, isVisited, start, length):
    isVisited[start] = 1
    for i in range(length):
        if isVisited[i] == 0 and isConnected[start,i] == 1:
            explore(isConnected, isVisited, i, length)