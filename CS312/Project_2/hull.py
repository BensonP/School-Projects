class Node():
    def __init__(self, point, CW = None, CCW = None):
        self.point = point
        self.CW = CW
        self.CCW = CCW

class Hull():
    def __init__(self, points):
        self.LM = Node(points[0])
        self.RM = Node(points[-1])
        self.points = points

    

class HullSolver():

    def __init__(self) -> None:
        pass

    def getSlope(self, point1, point2):
        
        rise = point2.y() - point1.y()
        run = point2.x() - point1.x()
        return rise/run
    
    def solveHull(self, hull):
        if len(hull.points) == 1:
            '''point = Node(hull.points[0])
            point.setCCW(point)
            point.setCW(point)'''
            hull.LM.CW = hull.LM
            hull.LM.CCW = hull.LM
            hull.RM.CW = hull.RM
            hull.RM.CCW = hull.RM
            return hull
        
        leftHull = self.solveHull(Hull(hull.points[:len(hull.points)//2]))
        rightHull = self.solveHull(Hull(hull.points[len(hull.points)//2:len(hull.points)]))

        hull = self.combine(leftHull, rightHull)
        return hull

    def combine(self, leftHull, rightHull):
        rightPoint = leftHull.RM
        leftPoint = rightHull.LM
        if len(leftHull.points) == 1:
            leftHull.RM = rightHull.RM
            leftHull.LM.CR = leftHull.RM
            leftHull.LM.CCW = leftHull.RM
            leftHull.RM.CW = leftHull.LM
            leftHull.RM.CCW = leftHull.LM
            return leftHull
        self.compareLeftCW(leftPoint, rightPoint)
        self.compareLeftCCW(leftPoint, rightPoint)
        self.compareRightCCW(leftPoint, rightPoint)
        self.compareRightCW(leftPoint, rightPoint)
        leftHull.RM = rightHull.RM
        return leftHull



    def solveRight(self, leftHullRight, rightHullLeft):
        slope = self.getSlope(leftHullRight.point, rightHullLeft.point)
        if(rightHullLeft.point != rightHullLeft.CW.point):
            slope2 = self.getSlope(leftHullRight.point, rightHullLeft.CW.point)
            if slope2 > slope:
                self.solveRight(leftHullRight, rightHullLeft.CW)
        else:
            leftHullRight.CW = rightHullLeft
            rightHullLeft.CW =leftHullRight

    def compareLeftCCW(self, leftNode, rightNode):
        slope = self.getSlope(leftNode.point, rightNode.point)
        slope2 = self.getSlope(leftNode.CCW.point, rightNode.point)
        if slope2 < slope:
            self.compareLeftCCW(leftNode.CCW, rightNode)
        else:
            rightNode.CCW = leftNode
            leftNode.CW = rightNode

    def compareLeftCW(self, leftNode, rightNode):
        slope = self.getSlope(leftNode.point, rightNode.point)
        slope2 = self.getSlope(leftNode.CW.point, rightNode.point)
        if slope2 > slope:
            self.compareLeftCW(leftNode.CW, rightNode)
        else:
            rightNode.CW = leftNode
            leftNode.CCW = rightNode

    def compareRightCCW(self, leftNode, rightNode):
        slope = self.getSlope(leftNode.point, rightNode.point)
        slope2 = self.getSlope(leftNode.point, rightNode.CCW.point)
        if slope2 < slope:
            self.compareRightCCW(leftNode, rightNode.CCW)
        else:
            rightNode.CW = leftNode
            leftNode.CCW = rightNode 

    def compareRightCW(self, leftNode, rightNode):
        slope = self.getSlope(leftNode.point, rightNode.point)
        slope2 = self.getSlope(leftNode.point, rightNode.CW.point)
        if slope2 > slope:
            self.compareRightCW(leftNode, rightNode.CW)
        else:
            rightNode.CCW = leftNode
            leftNode.CW = rightNode 
