import pygame, math
import numpy as np
import wireframe as wf
import basicShapes as shape

class WireframeViewer(wf.WireframeGroup):
    """ A group of wireframes which can be displayed on a Pygame screen """
    
    def __init__(self, width, height, name="Wireframe Viewer"):
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        
        self.wireframes = {}
        self.wireframe_colours = {}
        self.object_to_update = []
        
        self.displayNodes = False
        self.displayEdges = True
        self.displayFaces = True
        
        self.perspective = False
        self.eyeX = self.width/2
        self.eyeY = 100
        self.light_color = np.array([1,1,1])
        self.view_vector = np.array([0, 0, -1])        
        self.light_vector = np.array([0, 0, -1])  

        self.background = (10,10,50)
        self.nodeColour = (250,250,250)
        self.nodeRadius = 4
        
        self.control = 0
    
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
        #   If colour is set to None, then wireframe is not displayed
        self.wireframe_colours[name] = (250,250,250)
    
    def addWireframeGroup(self, wireframe_group):
        # Potential danger of overwriting names
        for name, wireframe in wireframe_group.wireframes.items():
            self.addWireframe(name, wireframe)

    def rotateY(self, angle):
        R1 = np.array([[math.cos(math.radians(angle)), 0, -math.sin(math.radians(angle)),0], 
              [0,1,0,0], 
              [math.sin(math.radians(angle)), 0,math.cos(math.radians(angle)),0],
              [0,0,0,1]])
        
        self.light_vector = np.matmul(R1, self.light_vector)
        return
    
    def rotateX(self, angle):
        R1 = np.array([[1,0,0,0],
                       [0,math.cos(np.radians(angle)),math.sin(np.radians(angle)),0],
                       [0,-math.sin(np.radians(angle)),math.cos(np.radians(angle)),0],
                       [0,0,0,1]])
        self.light_vector = np.matmul(R1, self.light_vector)
        return
    
    def rotateZ(self, angle):
        R1 = np.array([[math.cos(np.radians(angle)),math.sin(np.radians(angle)),0,0],
                       [-math.sin(np.radians(angle)),math.cos(np.radians(angle)),0,0],
                       [0,0,1,0],
                       [0,0,0,1]])
        self.light_vector = np.matmul(R1, self.light_vector)
        return

    
    def display(self):
        self.screen.fill(self.background)

        for name, wireframe in self.wireframes.items():
            nodes = wireframe.nodes
            
            if self.displayFaces:
                for (face, colour) in wireframe.sortedFaces():
                    v1 = (nodes[face[1]] - nodes[face[0]])[:3]
                    v2 = (nodes[face[2]] - nodes[face[0]])[:3]

                    normal = np.cross(v1, v2)
                    normal /= np.linalg.norm(normal)
                    towards_us = np.dot(normal, self.view_vector)

                    # Only draw faces that face us
                    if towards_us > 0:
                        m_ambient = 0.3
                        ambient = self.light_color * (m_ambient * colour)
                        

                        m_specular = 0.2
                        kGls = 4
                        reflection_vector = (2 * np.dot(self.light_vector,normal) * normal) - self.light_vector
                        specular = (self.light_color * (m_specular * colour) * ((np.dot(self.view_vector,reflection_vector)))**kGls)
                        

                        d_diffuse = 0.5
                        diffuse = d_diffuse * (self.light_color * colour) * (np.dot(normal,self.light_vector))
                        

                        if np.dot(self.light_vector,normal) < 0:
                            specular = [0,0,0]
                            diffuse = [0,0,0]
                        light_total = ambient + diffuse + specular
                        light_total = np.clip(light_total,0.0,255.0)

                        pygame.draw.polygon(self.screen, light_total, [(nodes[node][0], nodes[node][1]) for node in face], 0)

                if self.displayEdges:
                    for (n1, n2) in wireframe.edges:
                        if self.perspective:
                            if wireframe.nodes[n1][2] > -self.perspective and nodes[n2][2] > -self.perspective:
                                z1 = self.perspective/ (self.perspective + nodes[n1][2])
                                x1 = self.width/2  + z1*(nodes[n1][0] - self.width/2)
                                y1 = self.height/2 + z1*(nodes[n1][1] - self.height/2)
                    
                                z2 = self.perspective/ (self.perspective + nodes[n2][2])
                                x2 = self.width/2  + z2*(nodes[n2][0] - self.width/2)
                                y2 = self.height/2 + z2*(nodes[n2][1] - self.height/2)
                                
                                pygame.draw.aaline(self.screen, colour, (x1, y1), (x2, y2), 1)
                        else:
                            pygame.draw.aaline(self.screen, colour, (nodes[n1][0], nodes[n1][1]), (nodes[n2][0], nodes[n2][1]), 1)

            if self.displayNodes:
                for node in nodes:
                    pygame.draw.circle(self.screen, colour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
        
        pygame.display.flip()

    def keyEvent(self, key):
        
        #Your code here
        self.light_vector = np.hstack((self.light_vector,1))
        angle = 5
        if key == pygame.K_w:
            print("w is pressed")
            self.rotateX(angle)

        if key == pygame.K_s:
            print("s is pressed")
            self.rotateX(-angle)

        if key == pygame.K_a:
            print("a is pressed")
            self.rotateY(-angle)

        if key == pygame.K_d:
            print("d is pressed")
            self.rotateY(angle)

        if key == pygame.K_q:
            print("q is pressed")
            self.rotateZ(angle)

        if key == pygame.K_e:
            print("e is pressed")
            self.rotateZ(-angle)

        self.light_vector = self.light_vector[0], self.light_vector[1], self.light_vector[2]

        return

    def run(self):
        """ Display wireframe on screen and respond to keydown events """
        
        running = True
        key_down = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key_down = event.key
                elif event.type == pygame.KEYUP:
                    key_down = None
            
            if key_down:
                self.keyEvent(key_down)
            
            self.display()
            self.update()
            
        pygame.quit()

		
resolution = 52
viewer = WireframeViewer(600, 400)
viewer.addWireframe('sphere', shape.Spheroid((300,200, 20), (160,160,160), resolution=resolution))

# Colour ball
faces = viewer.wireframes['sphere'].faces
for i in range(int(resolution/4)):
	for j in range(resolution*2-4):
		f = i*(resolution*4-8) +j
		faces[f][1][1] = 0
		faces[f][1][2] = 0
	
viewer.displayEdges = False
viewer.run()