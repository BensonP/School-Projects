import numpy as np
import math as math


M1 = ([math.cos(math.radians(30)), 0, math.sin(math.radians(30)),0], 
      [0,1,0,0], 
      [-math.sin(math.radians(30)), 0,math.cos(math.radians(30)),0],
      [0,0,0,1])
M2= ([1.73,0,0,0], 
      [0,0.974,0,0], 
      [0,0,1.02,-20.20],
      [0,0,1,0])
M3 = ([5,-5,50,1])

newCoords = np.matmul(M2,M3)
print(newCoords)

V1 = np.matrix([25,40,25])
V2 = np.matrix([25,20,5])
V3 = V1-V2
v4 = V3/np.linalg.norm(V3)
print(V3)
print(v4)


VX = np.matrix([-.71,0,0])
VXF = VX/np.linalg.norm(VX)
print(VXF)

YX = np.matrix([0,0.71,-0.71])
VYF = YX/np.linalg.norm(YX)
print(VYF)





mT = ([-1,0,0,0], 
      [0,.71,-.71,0], 
      [0,.71,.71,0],
      [0,0,0,1])
mR= ([1,0,0,-25], 
      [0,1,0,-20], 
      [0,0,1,-5],
      [0,0,0,1])
P = ([5,6,7,1])
TR = np.matmul(mR,mT)
print(np.matmul(TR,P))