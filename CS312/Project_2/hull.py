from convex_hull import *
from Proj2GUI import *

class Node():
    def __init__(self, point):
        self.point = point
        self.CW = self
        self.CCW = self

class Hull():
    def __init__(self, LM, RM): ##left node and right node as init
        self.LM = LM
        self.RM = RM

    
def getSlope(point1, point2):
    
    rise = point2.y() - point1.y()
    rise = float(rise)
    run = point2.x() - point1.x()
    return rise/run

def solveHull(points):
    if len(points) == 1:
        node = Node(points[0])
        hull = Hull(node, node)
        return hull
    
    leftHull = solveHull(points[:len(points)//2])
    rightHull = solveHull(points[len(points)//2:len(points)])

    hull = combine(leftHull, rightHull)
    return hull

def combine(leftHull, rightHull): ##make call to creat upper and lower tangeants, then rewire my hull. 
    rightNode = leftHull.RM
    leftNode = rightHull.LM
    upperTangeant = getUpperTangeant(leftNode, rightNode)
    lowerTangeant = getLowerTangeant(leftNode, rightNode)
    upperTangeant[0].CW = upperTangeant[1]
    upperTangeant[1].CCW = upperTangeant[0]
    lowerTangeant[0].CCW = lowerTangeant[1]
    lowerTangeant[1].CW = lowerTangeant[0]

    leftHull.RM = rightHull.RM
    hull = leftHull
    return hull


def getUpperTangeant(leftNode, rightNode):
    done = 0
    while not done:
        newLeftNode = compareLeftCCW(leftNode, rightNode)
        newRightNode = compareRightCW(newLeftNode, rightNode)
        if newLeftNode == leftNode and newRightNode == rightNode:
            done = 1
        leftNode = newLeftNode
        rightNode = newRightNode
    return (newLeftNode, newRightNode)

def getLowerTangeant(leftNode, rightNode):
    done = 0
    while not done:
        newLeftNode = compareLeftCW(leftNode, rightNode)
        newRightNode = compareRightCCW(newLeftNode, rightNode)
        if newLeftNode == leftNode and newRightNode == rightNode:
            done = 1
        leftNode = newLeftNode
        rightNode = newRightNode
    return (newLeftNode, newRightNode)


def compareLeftCW(leftNode, rightNode):
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
    
def getPoints(hull):
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

def getPolygon(points):
    polygon = [QLineF(points[i],points[i+1]) for i in range(len(points)-1)]
    lastLine = QLineF(points[-1],points[0])
    polygon.append(lastLine)
    return polygon