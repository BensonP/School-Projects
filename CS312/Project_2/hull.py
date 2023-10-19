from convex_hull import *
from Proj2GUI import *

class Node(): #Node class to store my points, and to mantain a CW and CCW positions. 
    def __init__(self, point):
        self.point = point
        self.CW = self
        self.CCW = self

class Hull(): #Hull to store the nodes, and keep track of LM and RM nodes. 
    def __init__(self, LM, RM): 
        self.LM = LM
        self.RM = RM

    
def getSlope(point1, point2): #to get my slop. O(1) time and space
    rise = point2.y() - point1.y()
    rise = float(rise)
    run = point2.x() - point1.x()
    return rise/run

def solveHull(points): #is total O(nlog(n)), log(n) due to recursing half of the hull each time, and n due to the combine function
                        # worse case is O(n), due to potentially having to create a node at the base case for each point.
    if len(points) == 1: #where space is required and used for node creation. 
        node = Node(points[0])
        hull = Hull(node, node)
        return hull
    
    leftHull = solveHull(points[:len(points)//2])
    rightHull = solveHull(points[len(points)//2:len(points)])

    hull = combine(leftHull, rightHull) #is O(n) time
    return hull

def combine(leftHull, rightHull): #O(n) time, due to the worst case complexity being having to visit every Node within getUpperTangent/getLowerTangent
    rightNode = leftHull.RM
    leftNode = rightHull.LM
    upperTangeant = getUpperTangeant(leftNode, rightNode)
    lowerTangeant = getLowerTangeant(leftNode, rightNode)
    upperTangeant[0].CW = upperTangeant[1]
    upperTangeant[1].CCW = upperTangeant[0]
    lowerTangeant[0].CCW = lowerTangeant[1]
    lowerTangeant[1].CW = lowerTangeant[0]

    leftHull.RM = rightHull.RM
    return leftHull


def getUpperTangeant(leftNode, rightNode): #o(n), due to having to look at each node, in the worst case of a hull. 
    done = 0
    while not done: #this while loop could look at each node to compare and find the tangeant lines. 
        newLeftNode = compareLeftCCW(leftNode, rightNode)
        newRightNode = compareRightCW(newLeftNode, rightNode)
        if newLeftNode == leftNode and newRightNode == rightNode: 
            done = 1
        leftNode = newLeftNode
        rightNode = newRightNode
    return (newLeftNode, newRightNode)

def getLowerTangeant(leftNode, rightNode):  #o(n), due to having to look at each node, in the worst case of a hull. 
    done = 0
    while not done: #this while loop could look at each node to compare and find the tangeant lines. 
        newLeftNode = compareLeftCW(leftNode, rightNode)
        newRightNode = compareRightCCW(newLeftNode, rightNode)
        if newLeftNode == leftNode and newRightNode == rightNode:
            done = 1
        leftNode = newLeftNode
        rightNode = newRightNode
    return (newLeftNode, newRightNode)


def compareLeftCW(leftNode, rightNode): #following functions are all o(1)
    slope = getSlope(leftNode.point, rightNode.point)
    if(rightNode.point != leftNode.CW.point):
        slope2 = getSlope(leftNode.CW.point, rightNode.point)
        if slope2 > slope:
            return leftNode.CW
        return leftNode
        
def compareLeftCCW(leftNode, rightNode):
    slope = getSlope(leftNode.point, rightNode.point)
    if(rightNode.point != leftNode.CCW.point):
        slope2 = getSlope(leftNode.CCW.point, rightNode.point)
        if slope2 < slope:
            return leftNode.CCW
        return leftNode

def compareRightCCW(leftNode, rightNode):
    slope = getSlope(leftNode.point, rightNode.point)
    if(leftNode.point != rightNode.CCW.point):
        slope2 = getSlope(leftNode.point, rightNode.CCW.point)
        if slope2 < slope:
            return rightNode.CCW
        return rightNode

def compareRightCW(leftNode, rightNode):
    slope = getSlope(leftNode.point, rightNode.point)
    if(leftNode.point != rightNode.CW.point):
        slope2 = getSlope(leftNode.point, rightNode.CW.point)
        if slope2 > slope:
            return rightNode.CW
        return rightNode
    
def getPoints(hull): #this is O(n) due to having to iterate over every node in the hull. 
    points = []
    firstNode = hull.LM
    tempNode = hull.LM
    done = 0
    while not done:
        points.append(tempNode.point)
        tempNode = tempNode.CW
        if tempNode == firstNode:
            done = 1
    return points

def getPolygon(points): #also just O(n) to visit every item in the list
    polygon = [QLineF(points[i],points[i+1]) for i in range(len(points)-1)]
    lastLine = QLineF(points[-1],points[0])
    polygon.append(lastLine)
    return polygon