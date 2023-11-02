# Import a library of functions called 'pygame'
import pygame
from math import pi
import numpy as np

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Point3D:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		
class Line3D():
	
	def __init__(self, start, end):
		self.start = start
		self.end = end

def loadOBJ(filename):
	
	vertices = []
	indices = []
	lines = []
	
	f = open(filename, "r")
	for line in f:
		t = str.split(line)
		if not t:
			continue
		if t[0] == "v":
			vertices.append(Point3D(float(t[1]),float(t[2]),float(t[3])))
			
		if t[0] == "f":
			for i in range(1,len(t) - 1):
				index1 = int(str.split(t[i],"/")[0])
				index2 = int(str.split(t[i+1],"/")[0])
				indices.append((index1,index2))
			
	f.close()
	
	#Add faces as lines
	for index_pair in indices:
		index1 = index_pair[0]
		index2 = index_pair[1]
		lines.append(Line3D(vertices[index1 - 1],vertices[index2 - 1]))
		
	#Find duplicates
	duplicates = []
	for i in range(len(lines)):
		for j in range(i+1, len(lines)):
			line1 = lines[i]
			line2 = lines[j]
			
			# Case 1 -> Starts match
			if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
				if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
					duplicates.append(j)
			# Case 2 -> Start matches end
			if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
				if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
					duplicates.append(j)
					
	duplicates = list(set(duplicates))
	duplicates.sort()
	duplicates = duplicates[::-1]
	
	#Remove duplicates
	for j in range(len(duplicates)):
		del lines[duplicates[j]]
	
	return lines

def loadHouse():
	house = []
	#Floor
	house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
	house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
	house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
	house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
	#Ceiling
	house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
	house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
	house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
	house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
	#Walls
	house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
	house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
	house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
	house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
	#Door
	house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
	house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
	house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
	#Roof
	house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
	house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
	house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
	house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
	house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))
	
	return house

def loadCar():
	car = []
	#Front Side
	car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
	car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
	car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
	car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
	car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
	car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

	#Back Side
	car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
	car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
	car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
	car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
	car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
	car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))
	
	#Connectors
	car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
	car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
	car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
	car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
	car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
	car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

	return car

def loadTire():
	tire = []
	#Front Side
	tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
	tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
	tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
	tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
	tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
	tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
	tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
	tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

	#Back Side
	tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
	tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
	tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
	tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
	tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
	tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
	tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
	tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

	#Connectors
	tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
	tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
	tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
	tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
	tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
	tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
	tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
	tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))
	
	return 

#helpful matrixes
def homogenize(x,y,z):
	return np.matrix([[x],[y],[z],[1]])

def getCameraMatrix(x,y,z,theta):
	return np.matmul(getRotationMatrix(theta), getTransformationMatrix(x,y,z))
	return np.matrix([[np.cos(np.radians(theta)), 0, np.sin(np.radians(theta)),x], 
      				[0,1,0,y], 
      				[-np.sin(np.radians(theta)), 0,np.cos(np.radians(theta)),z],
      				[0,0,0,1]])

def deviceNormalize(m,w):
	n = m/w
	return np.matrix([[n[0,0]],
				   [n[1,0]],
				   [1]])

def getPoint(m):
	m = np.matrix([[m[0,0]],
				[m[1,0]],
				[1]])
	screenMatrix = np.matrix([[width/2, 0, width/2],
						   [0, -height/2, height/2],
						   [0,0,1]])
	m = np.matmul(screenMatrix,m)
	point = Point(m[0,0], m[1,0])
	return point

def getClipMatrix():
	return np.matrix([[zoom_x,0,0,0], 
      				[0,zoom_y,0,0], 
      				[0,0,(f+n)/(f-n), (-2*n*f)/(f-n)],
      				[0,0,1,0]])

def clipTests(start, end, start_w, end_w):
	start_x = start[0,0]
	start_y = start[1,0]
	start_z = start[2,0]
	end_x = end[0,0]
	end_y = end[1,0]
	end_z = end[2,0]

	if start_z < -start_w or end_z < -end_w:
		return True
	if start_x < -start_w and end_x < -end_w:
		return True
	if start_x > start_w and end_x > end_w:
		return True
	if start_y < -start_w and end_y < -end_w :
		return True
	if start_y > start_w and end_y > end_w:
		return True
	if start_z > start_w and end_z > end_w:
		return True
	
	return False

def getTransformationMatrix(x,y,z):
	return np.matrix([[1,0,0,x], 
							[0,1,0,y], 
							[0,0,1,z],
							[0,0,0,1]])

def getRotationMatrix(angle):
	return np.matrix([[np.cos(np.radians(angle)), 0, np.sin(np.radians(angle)),0], 
      [0,1,0,0], 
      [-np.sin(np.radians(angle)), 0,np.cos(np.radians(angle)),0],
      [0,0,0,1]])

def getScaleMatrix(x,y,z):
	return np.matrix([[x,0,0,0], 
							[0,y,0,0], 
							[0,0,z,0],
							[0,0,0,1]])
	
# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen
size = [512, 512]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Shape Drawing")
 
#Set needed variables
done = False
clock = pygame.time.Clock()
start = Point(0.0,0.0)
end = Point(0.0,0.0)
camera_x = 0
camera_y = 0
camera_z = 0
angle = 0
width = size[0]
height = size[1]
pushed_matrix = None

fov = 90
zoom_x = 1/np.tan(np.radians(fov/2))
zoom_y = zoom_x * size[0]/size[1]
f = 1000
n = 10

#Loop until the user clicks the close button.
while not done:
 
	# This limits the while loop to a max of 100 times per second.
	# Leave this out and we will use all CPU we can.
	clock.tick(100)

	# Clear the screen and set the screen background
	screen.fill(BLACK)

	#Controller Code#
	#####################################################################

	for event in pygame.event.get():
		if event.type == pygame.QUIT: # If user clicked close
			done=True
			
	pressed = pygame.key.get_pressed()

	if pressed[pygame.K_a]:
		print("a is pressed")
		camera_z += np.sin(np.radians(angle))
		camera_x += np.cos(np.radians(angle))

	if pressed[pygame.K_d]:
		print("d is pressed")
		camera_z -= np.sin(np.radians(angle))
		camera_x -= np.cos(np.radians(angle))
		
	if pressed[pygame.K_w]:
		camera_z -= np.sin(np.radians(angle + 90))
		camera_x -= np.cos(np.radians(angle + 90))
		print("w is pressed")

	if pressed[pygame.K_s]:
		camera_z += np.sin(np.radians(angle + 90))
		camera_x += np.cos(np.radians(angle + 90))
		print("s is pressed")

	if pressed[pygame.K_r]:
		camera_y -= 1
		print("r is pressed")

	if pressed[pygame.K_f]:
		camera_y += 1
		print("f is pressed")

	if pressed[pygame.K_e]:
		angle +=1
		camera_matrix = np.matmul(getTransformationMatrix(-camera_x, -camera_y, -camera_z), camera_matrix)
		print("e is pressed")

	if pressed[pygame.K_q]:
		angle -=1
		print("q is pressed")
	
	camera_matrix = getCameraMatrix(camera_x,camera_y,camera_z,angle)

	#Viewer Code#
	#####################################################################
	def drawObject(linelist):
		for s in linelist:
			start_vector = homogenize(s.start.x, s.start.y, s.start.z)
			end_vector = homogenize(s.end.x, s.end.y, s.end.z)

			start_Transformation_Matrix = np.matmul(camera_matrix, start_vector)
			end_Transformation_Matrix = np.matmul(camera_matrix, end_vector)

			clip_matrix = getClipMatrix()
			#BOGUS DRAWING PARAMETERS SO YOU CAN SEE THE HOUSE WHEN YOU START UP
			start_Transformation_Matrix = np.matmul(clip_matrix, start_Transformation_Matrix)
			end_Transformation_Matrix = np.matmul(clip_matrix, end_Transformation_Matrix)

			start_w = start_Transformation_Matrix[3,0]
			end_w = end_Transformation_Matrix[3,0]
			clip = False
			clip = clipTests(start_Transformation_Matrix,end_Transformation_Matrix, start_w, end_w)
			if not clip:
				start_Transformation_Matrix = deviceNormalize(start_Transformation_Matrix,start_w)
				end_Transformation_Matrix = deviceNormalize(end_Transformation_Matrix,end_w)

				start_Point = getPoint(start_Transformation_Matrix)
				end_Point = getPoint(end_Transformation_Matrix)
				pygame.draw.line(screen, BLUE, (start_Point.x, start_Point.y), (end_Point.x, end_Point.y))

	def drawStreet():
		for i in range(5):
			global camera_matrix
			if i != 0:
				transformation_matrix = np.matrix([[1,0,0,20], 
							[0,1,0,0], 
							[0,0,1,0],
							[0,0,0,1]])
				camera_matrix = np.matmul(camera_matrix, transformation_matrix)
			drawObject(loadHouse())

	pushed_matrix = np.copy(camera_matrix)
	drawStreet()
	#camera_matrix = np.copy(pushed_matrix)
	#camera_matrix = np.matmul(getScaleMatrix(1,1,-1),camera_matrix)
	camera_matrix = np.matmul(getTransformationMatrix(0,0,50),camera_matrix)
	#camera_matrix = np.copy(pushed_matrix)
	drawStreet()


	# Go ahead and update the screen with what we've drawn.
	# This MUST happen after all the other drawing commands.
	pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()