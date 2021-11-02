import pygame
import math
screenW, screenH = 1280, 720
screen = pygame.display.set_mode((screenW, screenH))
GRAVITATIONAL_CONSTANT = 6.67408e-11
DISTANCE_PIXEL_DEFAUT = 1000000000 #m
current_distance_pixel = DISTANCE_PIXEL_DEFAUT
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)

class CelestialBody:
    def __init__(self, id, mass, radius, ivx, ivy, posx, posy, img):
        self.name = id
        self.distance_pixel = DISTANCE_PIXEL_DEFAUT
        self.mass = mass
        self.radius = radius
        self.radius2D = 5#radius/self.distance_pixel
        self.initialVelocity = pygame.Vector2(ivx, ivy)
        self.currentVelocity = pygame.Vector2(ivx, ivy)
        self.position = pygame.Vector2(posx, posy)
        self.position2D =  pygame.Vector2(screenW/2 + posx/self.distance_pixel, screenH/2 - posy/self.distance_pixel)
        self.namesurface = myfont.render(self.name, False, (255, 255, 255))
        self.img = img
        self.distance_soleil = posy

    def updateVelocity(self, allBodies):
        """Newton's law of universal gravitation : F = G*((m1*m2)/r)"""
        for otherBodies in allBodies:
            if(otherBodies!=self):
                sqrDst = (otherBodies.position - self.position).magnitude()
                forceDir = (otherBodies.position - self.position).normalize()
                force = forceDir * GRAVITATIONAL_CONSTANT * (self.mass * otherBodies.mass / sqrDst**2)
                acceleration = force / self.mass
                self.currentVelocity += acceleration * (60*60*24)

    def updatePosition(self):
        self.position += self.currentVelocity * (60*60*24)
        self.position2D = pygame.Vector2(screenW/2 + self.position.x/self.distance_pixel, screenH/2 - self.position.y/self.distance_pixel)

    def zoomUp(self):
        self.distance_pixel *= 1.1
        # self.radius2D = self.radius/self.distance_pixel

    def zoomDown(self):
        self.distance_pixel /= 1.1
        # self.radius2D = self.radius/self.distance_pixel

    def getImage(self):
        return pygame.transform.scale(self.img, (10,10))

    def modif_body(self, input_boxes):
        for box in input_boxes:
            if box.boxfield == 'name' and box.isChanged == True:
                self.name = box.text
                self.namesurface = myfont.render(self.name, False, (255, 255, 255))
            if box.boxfield == 'mass' and box.isChanged == True:
                mass = box.text.split('e')
                ret_mass =((float(mass[0]))*(10**int(mass[1])))
                self.mass = ret_mass
            if box.boxfield == 'vitesse':
                self.initialVelocity = pygame.Vector2(float(box.text), 0)
                if self.currentVelocity.x > 0 :
                    self.currentVelocity.x = self.initialVelocity.x
                else:
                    self.currentVelocity.x = -self.initialVelocity.x
            if box.boxfield == 'distance' and box.isChanged == True:
                self.distance_soleil = float(box.text)*DISTANCE_PIXEL_DEFAUT
                self.position.y = float(box.text)*DISTANCE_PIXEL_DEFAUT
                self.position.x = 0
                self.currentVelocity = self.initialVelocity
     
            
            