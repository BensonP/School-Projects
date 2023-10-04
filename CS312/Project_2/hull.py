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

        self.solveLeft(leftHull.RM, rightHull.LM)
        self.solveRight(rightHull.LM.CCW, rightHull.LM)
        return hull

    def solveLeft(self, leftHullRight, rightHullLeft):
        slope = self.getSlope(leftHullRight.point, rightHullLeft.point)
        slope2 = self.getSlope(leftHullRight.CCW.point, rightHullLeft.point)
        if slope2 < slope:
            self.solveLeft(leftHullRight.CCW, rightHullLeft)
        else:
            rightHullLeft.CCW = leftHullRight
            leftHullRight.CW = rightHullLeft
            ##???? what now?

    def solveRight(self, leftHullRight, rightHullLeft):
        slope = self.getSlope(leftHullRight.point, rightHullLeft.point)
        slope2 = self.getSlope(leftHullRight.point, rightHullLeft.CW.point)
        if slope2 > slope:
            self.solveRight(leftHullRight, rightHullLeft.CW)
        else:
            leftHullRight.CW = rightHullLeft
            rightHullLeft.CW =leftHullRight



